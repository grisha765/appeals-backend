from typing import List
from typing import List, Sequence
from tortoise.transactions import in_transaction
from appeals.db.models import Conversion, ConversionFile


async def create_conversion(
        user_id: int,
        head: str,
        text: str,
        status: str = "unviewed"
) -> dict:
    conversion = await Conversion.create(
        user_id=user_id,
        head=head,
        text=text,
        status=status
    )
    conversion_data = {
        "id": conversion.id,
        "user_id": conversion.user_id,
        "head": conversion.head,
        "text": conversion.text,
        "status": conversion.status,
    }
    return conversion_data


async def add_files_to_conversion(
    user_id: int,
    conversion_id: int,
    files: Sequence[dict],
) -> bool:
    conversion = await Conversion.filter(
        id=conversion_id,
        user_id=user_id
    ).first()

    if not conversion:
        return False

    async with in_transaction() as tx:
        for f in files:
            await ConversionFile.create(
                conversion=conversion,
                filename=f["filename"],
                content_type=f["content_type"],
                data=f["data"],
                using_db=tx,
            )
    return True


async def get_all_conversions() -> List[dict]:
    return await Conversion.all().values(
        "id",
        "user_id",
        "head",
        "text",
        "status"
    )


async def get_conversions(user_id: int) -> List[dict]:
    return await Conversion.filter(user_id=user_id).values(
        "id",
        "head",
        "status"
    )


async def get_conversion(
        user_id: int,
        conversion_id: int
) -> dict:
    return await Conversion.filter(
        id=conversion_id,
        user_id=user_id
    ).first().values(
        "id",
        "user_id",
        "head",
        "text",
        "status"
    )


async def get_conversion_file(
    user_id: int,
    conversion_id: int,
    file_id: int,
) -> ConversionFile | None:
    return await ConversionFile.filter(
        id=file_id,
        conversion_id=conversion_id,
        conversion__user_id=user_id
    ).first()


async def view_conversion(
        user_id: int,
        conversion_id: int
) -> dict:
    conversion = await Conversion.filter(
        id=conversion_id,
        user_id=user_id
    ).prefetch_related("files").first()

    if not conversion:
        return {}

    file_meta = [
        {
            "id": f.id,
            "filename": f.filename,
            "content_type": f.content_type,
            "download_url": f"/users/{user_id}/conversions/{conversion_id}/files/{f.id}",
        }
        for f in conversion.files
    ]

    return {
        "text": conversion.text,
        "files": file_meta or None,
    }


async def set_status_conversion(
        user_id: int,
        conversion_id: int,
        status: str
) -> bool:
    updated_count = await Conversion.filter(
        id=conversion_id,
        user_id=user_id
    ).update(status=status)
    return updated_count > 0


async def del_conversion(
        user_id: int,
        conversion_id: int
) -> bool:
    deleted_count = await Conversion.filter(
        id=conversion_id,
        user_id=user_id
    ).delete()
    return deleted_count > 0


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
