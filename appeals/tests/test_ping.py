from appeals.config import logging_config


def ping_reset(logger, client):
    """
    Test #1 (POST /ping with {"op": "reset"})
    """
    try:
        response = client.post("/ping", json={"op": "reset"})
        assert response.status_code == 200, "Expected status 200 on /ping POST (reset)."
        body = response.json()
        assert body.get("Pong") == "0", "Expected 'Pong' == '0' after reset."
        logger.info("Test passed! #1 (ping reset)")
    except AssertionError as e:
        logger.error(f"Test failed! #1 (ping reset): {e}")
        raise


def ping_plus(logger, client):
    """
    Test #2 (POST /ping with {"op": "plus"})
    """
    try:
        response = client.post("/ping", json={"op": "plus"})
        assert response.status_code == 200, "Expected status 200 on /ping POST (plus)."
        body = response.json()
        assert body.get("Pong") == "1", "Expected 'Pong' == '1' after plus."
        logger.info("Test passed! #2 (ping plus)")
    except AssertionError as e:
        logger.error(f"Test failed! #2 (ping plus): {e}")
        raise


def ping_minus(logger, client):
    """
    Test #3 (POST /ping with {"op": "minus"})
    """
    try:
        response = client.post("/ping", json={"op": "minus"})
        assert response.status_code == 200, "Expected status 200 on /ping POST (minus)."
        body = response.json()
        assert body.get("Pong") == "0", "Expected 'Pong' == '0' after minus."
        logger.info("Test passed! #3 (ping minus)")
    except AssertionError as e:
        logger.error(f"Test failed! #3 (ping minus): {e}")
        raise


def ping_set(logger, client):
    """
    Test #4 (POST /ping with {"op": "set", "value": 42})
    """
    try:
        response = client.post("/ping", json={"op": "set", "value": 42})
        assert response.status_code == 200, "Expected status 200 on /ping POST (set)."
        body = response.json()
        assert body.get("Pong") == "42", "Expected 'Pong' == '42' after set=42."
        logger.info("Test passed! #4 (ping set)")
    except AssertionError as e:
        logger.error(f"Test failed! #4 (ping set): {e}")
        raise


def ping_get(logger, client):
    """
    Test #5 (GET /ping)
    """
    try:
        response = client.get("/ping")
        assert response.status_code == 200, "Expected status 200 on /ping GET."
        body = response.json()
        assert body.get("Pong") == "42", "Expected 'Pong' == '42' after get."
        logger.info("Test passed! #5 (ping get)")
    except AssertionError as e:
        logger.error(f"Test failed! #5 (ping get): {e}")
        raise


def test_ping(client):
    logger = logging_config.setup_logging(__name__)

    ping_reset(logger, client)
    ping_plus(logger, client)
    ping_minus(logger, client)
    ping_set(logger, client)
    ping_get(logger, client)

    logger.info("All ping tests passed!")


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")

