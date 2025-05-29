from appeals.config import logging_config
from appeals.core.schemas import ConversionStatus


def create_conversion(logger, client):
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


def get_all_conversions(logger, client, conversion_id):
    """
    Test #2 (GET /users/1/conversions)
    """
    try:
        response = client.get(
            "/conversions",
            auth=("admin", "admin")
        )
        assert response.status_code == 200, "Expected status 200 on /conversions GET."
        user_conversions = response.json()
        assert any(conv["id"] == conversion_id for conv in user_conversions), \
            "Created conversion not found in user list."
        logger.info("Test passed! #2 (get all conversions)")
    except AssertionError as e:
        logger.error(f"Test failed! #2 (get all conversions): {e}")
        raise


def get_user_conversions(logger, client, conversion_id):
    """
    Test #2 (GET /users/1/conversions)
    """
    try:
        response = client.get("/users/1/conversions")
        assert response.status_code == 200, "Expected status 200 on /users/1/conversions GET."
        user_conversions = response.json()
        assert any(conv["id"] == conversion_id for conv in user_conversions), \
            "Created conversion not found in user list."
        logger.info("Test passed! #3 (get user conversions)")
    except AssertionError as e:
        logger.error(f"Test failed! #3 (get user conversions): {e}")
        raise


def update_conversion_status(logger, client, conversion_id):
    """
    Test #3 (PATCH /users/1/conversions/{conversion_id}/status)
    """
    try:
        update_body = {"status": ConversionStatus.accepted.value}
        response = client.patch(
            f"/users/1/conversions/{conversion_id}/status",
            json=update_body,
            auth=("admin", "admin")
        )
        assert response.status_code == 200, "Expected status 200 on status PATCH."
        updated_items = response.json()
        assert len(updated_items) == 1, "Expected one updated item."
        updated_item = updated_items[0]
        assert updated_item["id"] == conversion_id, "Expected the same conversion ID."
        assert updated_item["status"] == "accepted", "Expected status to be 'accepted'."
        logger.info("Test passed! #4 (update conversion status)")
    except AssertionError as e:
        logger.error(f"Test failed! #4 (update conversion status): {e}")
        raise


def view_conversion(logger, client, conversion_id):
    """
    Test #4 (GET /users/1/conversions/{conversion_id})
    """
    try:
        response = client.get(f"/users/1/conversions/{conversion_id}")
        assert response.status_code == 200, "Expected status 200 on /users/1/conversions/{id} GET."
        detail = response.json()
        assert len(detail) == 1, "Expected to get text in a list."
        assert detail[0]["text"] == "The text of the conversion", "Text mismatch."
        logger.info("Test passed! #5 (view conversion)")
    except AssertionError as e:
        logger.error(f"Test failed! #5 (view conversion): {e}")
        raise


def attach_file_to_conversion(logger, client, conversion_id):
    """
    Test #6 (POST /users/1/conversions/{conversion_id}/files)
    """
    try:
        files = {
            "files": ("test.txt", b"Hello, world!", "text/plain")
        }
        response = client.post(f"/users/1/conversions/{conversion_id}/files", files=files)
        assert response.status_code == 200, "Expected status 200 on /files POST."
        data = response.json()
        assert len(data) == 1, "Expected a single ConversionText item."
        conv_text = data[0]
        assert conv_text["text"] == "The text of the conversion", "Conversion text mismatch."
        assert "files" in conv_text, "Expected 'files' in response."
        assert len(conv_text["files"]) == 1, "Expected exactly one file attached."
        file_meta = conv_text["files"][0]
        assert file_meta["filename"] == "test.txt", "Filename mismatch."
        assert file_meta["content_type"] == "text/plain", "Content type mismatch."
        logger.info("Test passed! #6 (attach file)")
        return file_meta["id"]
    except AssertionError as e:
        logger.error(f"Test failed! #6 (attach file): {e}")
        raise


def download_conversion_file(logger, client, conversion_id, file_id):
    """
    Test #7 (GET /users/1/conversions/{conversion_id}/files/{file_id})
    """
    try:
        response = client.get(f"/users/1/conversions/{conversion_id}/files/{file_id}")
        assert response.status_code == 200, "Expected status 200 on /files GET."
        assert response.content == b"Hello, world!", "File content mismatch."

        content_type_header = response.headers["Content-Type"]
        assert content_type_header.startswith("text/plain"), \
            f"Content-Type mismatch: {content_type_header}"

        disposition = response.headers["Content-Disposition"]
        assert 'filename="test.txt"' in disposition, "Content-Disposition filename mismatch."
        logger.info("Test passed! #7 (download file)")
    except AssertionError as e:
        logger.error(f"Test failed! #7 (download file): {e}")
        raise


def delete_conversion(logger, client, conversion_id):
    """
    Test #5 (DELETE /users/1/conversions/{conversion_id})
    """
    try:
        response = client.delete(
            f"/users/1/conversions/{conversion_id}",
            auth=("admin", "admin")
        )
        assert response.status_code == 204, "Expected status 204 on DELETE."
        logger.info("Test passed! #8 (delete conversion)")
    except AssertionError as e:
        logger.error(f"Test failed! #8 (delete conversion): {e}")
        raise


def test_conversions(client):
    logger = logging_config.setup_logging(__name__)

    conversion_id = create_conversion(logger, client)
    get_all_conversions(logger, client, conversion_id)
    get_user_conversions(logger, client, conversion_id)
    update_conversion_status(logger, client, conversion_id)
    view_conversion(logger, client, conversion_id)
    file_id = attach_file_to_conversion(logger, client, conversion_id)
    download_conversion_file(logger, client, conversion_id, file_id)
    delete_conversion(logger, client, conversion_id)

    logger.info("All conversions tests passed!")


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
