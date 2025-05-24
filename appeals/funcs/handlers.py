from typing import List, Sequence
from fastapi import HTTPException, UploadFile, File
from fastapi.responses import Response
from appeals.db.ping import get_number, set_number
from appeals.core.schemas import (
    PingBody,
    PingResponse,
    ConversionCreateBody,
    ConversionStatusUpdateBody,
    ConversionBrief,
    ConversionDetail,
    ConversionText
)
from appeals.db.conversion import (
    create_conversion,
    add_files_to_conversion,
    get_all_conversions,
    get_conversions,
    view_conversion,
    set_status_conversion,
    del_conversion,
    get_conversion,
    get_conversion_file
)


async def ping_post_handler(
    body: PingBody
) -> PingResponse:
    number = await get_number()

    match body.op:
        case "plus":
            number += 1
        case "minus":
            number -= 1
        case "reset":
            number = 0
        case "set":
            assert body.value is not None
            number = body.value

    await set_number(number)
    return PingResponse(Pong=str(number))


async def ping_get_handler() -> PingResponse:
    number = await get_number()
    return PingResponse(Pong=str(number))


async def create_conversion_handler(body: ConversionCreateBody) -> List[ConversionDetail]:
    conv = await create_conversion(
        user_id=body.user_id,
        head=body.head,
        text=body.text,
        status=body.status.value,
    )
    return [ConversionDetail(**conv)]


async def pin_file_conversion_handler(
    user_id: int,
    conversion_id: int,
    files: Sequence[UploadFile] = File(..., description="One or more files"),
) -> List[ConversionText]:
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")

    files_payload = [
        {
            "filename": up.filename,
            "content_type": up.content_type or "application/octet-stream",
            "data": await up.read(),
        }
        for up in files
    ]

    success = await add_files_to_conversion(
        user_id=user_id,
        conversion_id=conversion_id,
        files=files_payload,
    )
    if not success:
        raise HTTPException(status_code=404, detail="Conversion not found")

    conv = await view_conversion(user_id, conversion_id)
    return [ConversionText(**conv)]


async def get_all_conversions_handler() -> List[ConversionDetail]:
    convs = await get_all_conversions()
    return [ConversionDetail(**conv) for conv in convs]


async def get_user_conversions_handler(user_id: int) -> List[ConversionBrief]:
    convs = await get_conversions(user_id)
    return [ConversionBrief(**conv) for conv in convs]


async def view_conversion_handler(
        user_id: int,
        conversion_id: int
) -> List[ConversionText]:
    conv = await view_conversion(user_id, conversion_id)
    if conv is None:
        raise HTTPException(status_code=404, detail="Conversion not found")
    return [ConversionText(**conv)]


async def download_conversion_file_handler(
    user_id: int,
    conversion_id: int,
    file_id: int,
):
    file = await get_conversion_file(user_id, conversion_id, file_id)
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")

    headers = {
        "Content-Disposition": f'attachment; filename="{file.filename}"'
    }
    return Response(
        content=file.data,
        media_type=file.content_type,
        headers=headers,
    )


async def set_status_conversion_handler(
    user_id: int,
    conversion_id: int,
    body: ConversionStatusUpdateBody,
) -> List[ConversionDetail]:
    updated = await set_status_conversion(
        user_id,
        conversion_id,
        body.status.value
    )
    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Conversion not found"
        )

    conv = await get_conversion(
        user_id,
        conversion_id
    )
    return [ConversionDetail(**conv)]


async def del_conversion_handler(
        user_id: int,
        conversion_id: int
):
    deleted = await del_conversion(
        user_id,
        conversion_id
    )
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Conversion not found"
        )
    return


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
