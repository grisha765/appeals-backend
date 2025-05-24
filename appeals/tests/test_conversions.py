from appeals.config import logging_config
from fastapi.testclient import TestClient
from appeals.core.init import app
from appeals.core.schemas import ConversionStatus

client = TestClient(app)


def create_conversion(logger):
    """
    Test #1 (POST /conversions)
    """
    new_conversion_body = {
        "user_id": 1,
        "head": "Sample conversion",
        "text": "The text of the conversion",
        "status": "unviewed"
    }
    try:
        response = client.post("/conversions", json=new_conversion_body)
        assert response.status_code == 200, "Expected status 200 on /conversions POST."
        created_items = response.json()
        assert len(created_items) == 1, "Expected one created item."
        created_item = created_items[0]
        assert created_item["user_id"] == 1, "User ID mismatch."
        assert created_item["status"] == "unviewed", "Status mismatch."
        logger.info("Test passed! #1 (create conversion)")

        return created_item["id"]
    except AssertionError as e:
        logger.error(f"Test failed! #1 (create conversion): {e}")
        raise


def get_user_conversions(logger, conversion_id):
    """
    Test #2 (GET /users/1/conversions)
    """
    try:
        response = client.get("/users/1/conversions")
        assert response.status_code == 200, "Expected status 200 on /users/1/conversions GET."
        user_conversions = response.json()
        assert any(conv["id"] == conversion_id for conv in user_conversions), \
            "Created conversion not found in user list."
        logger.info("Test passed! #2 (get user conversions)")
    except AssertionError as e:
        logger.error(f"Test failed! #2 (get user conversions): {e}")
        raise


def update_conversion_status(logger, conversion_id):
    """
    Test #3 (PATCH /users/1/conversions/{conversion_id}/status)
    """
    try:
        update_body = {"status": ConversionStatus.accepted.value}
        response = client.patch(f"/users/1/conversions/{conversion_id}/status", json=update_body)
        assert response.status_code == 200, "Expected status 200 on status PATCH."
        updated_items = response.json()
        assert len(updated_items) == 1, "Expected one updated item."
        updated_item = updated_items[0]
        assert updated_item["id"] == conversion_id, "Expected the same conversion ID."
        assert updated_item["status"] == "accepted", "Expected status to be 'accepted'."
        logger.info("Test passed! #3 (update conversion status)")
    except AssertionError as e:
        logger.error(f"Test failed! #3 (update conversion status): {e}")
        raise


def view_conversion(logger, conversion_id):
    """
    Test #4 (GET /users/1/conversions/{conversion_id})
    """
    try:
        response = client.get(f"/users/1/conversions/{conversion_id}")
        assert response.status_code == 200, "Expected status 200 on /users/1/conversions/{id} GET."
        detail = response.json()
        assert len(detail) == 1, "Expected to get text in a list."
        assert detail[0]["text"] == "The text of the conversion", "Text mismatch."
        logger.info("Test passed! #4 (view conversion)")
    except AssertionError as e:
        logger.error(f"Test failed! #4 (view conversion): {e}")
        raise


def delete_conversion(logger, conversion_id):
    """
    Test #5 (DELETE /users/1/conversions/{conversion_id})
    """
    try:
        response = client.delete(f"/users/1/conversions/{conversion_id}")
        assert response.status_code == 204, "Expected status 204 on DELETE."
        logger.info("Test passed! #5 (delete conversion)")
    except AssertionError as e:
        logger.error(f"Test failed! #5 (delete conversion): {e}")
        raise


def test_conversions():
    logger = logging_config.setup_logging(__name__)

    conversion_id = create_conversion(logger)
    get_user_conversions(logger, conversion_id)
    update_conversion_status(logger, conversion_id)
    view_conversion(logger, conversion_id)
    delete_conversion(logger, conversion_id)

    logger.info("All conversions tests passed!")


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
