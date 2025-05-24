from typing import List
from fastapi.responses import Response
from appeals.funcs.handlers import ping_post_handler, ping_get_handler
from appeals.core.schemas import (
    PingResponse,
    ConversionBrief,
    ConversionDetail,
    ConversionText
)
from appeals.funcs.handlers import (
    create_conversion_handler,
    pin_file_conversion_handler,
    get_all_conversions_handler,
    get_user_conversions_handler,
    view_conversion_handler,
    download_conversion_file_handler,
    set_status_conversion_handler,
    del_conversion_handler,
)


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
        {
            "path": "/conversions",
            "endpoint": create_conversion_handler,
            "methods": ["POST"],
            "summary": "Create a new conversion",
            "response_model": List[ConversionDetail],
        },
        {
            "path": "/users/{user_id}/conversions/{conversion_id}/files",
            "endpoint": pin_file_conversion_handler,
            "methods": ["POST"],
            "summary": "Attach one or more files to an existing conversion",
            "response_model": List[ConversionText],
        },
        {
            "path": "/conversions",
            "endpoint": get_all_conversions_handler,
            "methods": ["GET"],
            "summary": "Get ALL conversions (admin view)",
            "response_model": List[ConversionDetail],
        },
        {
            "path": "/users/{user_id}/conversions",
            "endpoint": get_user_conversions_handler,
            "methods": ["GET"],
            "summary": "List conversions for one user (id, head, status)",
            "response_model": List[ConversionBrief],
        },
        {
            "path": "/users/{user_id}/conversions/{conversion_id}",
            "endpoint": view_conversion_handler,
            "methods": ["GET"],
            "summary": "Get the full text of a conversion",
            "response_model": List[ConversionText],
        },
        {
            "path": "/users/{user_id}/conversions/{conversion_id}/files/{file_id}",
            "endpoint": download_conversion_file_handler,
            "methods": ["GET"],
            "summary": "Download attached file",
            "response_class": Response,
        },
        {
            "path": "/users/{user_id}/conversions/{conversion_id}/status",
            "endpoint": set_status_conversion_handler,
            "methods": ["PATCH"],
            "summary": "Update the status of a conversion",
            "response_model": List[ConversionDetail],
        },
        {
            "path": "/users/{user_id}/conversions/{conversion_id}",
            "endpoint": del_conversion_handler,
            "methods": ["DELETE"],
            "summary": "Delete a conversion",
            "status_code": 204,
            "response_model": None,
        },
    ]

    for cfg in routes_cfg:
        app.add_api_route(**cfg)


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
