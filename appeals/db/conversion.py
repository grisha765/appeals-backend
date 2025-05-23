from typing import List
from appeals.db.models import Conversion


async def create_conversion(
        user_id: int,
        head: str,
        text: str,
        status:
        str = "unviewed"
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


async def view_conversion(
        user_id: int,
        conversion_id: int
) -> str:
    conversion = await Conversion.filter(
        id=conversion_id,
        user_id=user_id
    ).first()
    if conversion:
        return conversion.text
    return ''


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
