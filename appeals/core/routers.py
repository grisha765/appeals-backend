from appeals.funcs.handlers import ping_post_handler, ping_get_handler
from appeals.core.schemas import PingResponse


def init_app(app):
    routes_cfg = [
        {
            "path": "/ping",
            "endpoint": ping_post_handler,
            "methods": ["POST"],
            "summary": "Set the current counter value",
            "response_model": PingResponse,
        },
        {
            "path": "/ping",
            "endpoint": ping_get_handler,
            "methods": ["GET"],
            "summary": "Get the current counter value",
            "response_model": PingResponse,
        },
    ]

    for cfg in routes_cfg:
        app.add_api_route(**cfg)


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
