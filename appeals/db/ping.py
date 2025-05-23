from tortoise.transactions import in_transaction
from appeals.db.models import Ping


async def get_number() -> int:
    ping = await Ping.filter(id=1).first()
    return ping.number if ping else 0


async def set_number(value: int) -> None:
    async with in_transaction():
        ping = await Ping.filter(id=1).first()
        if ping:
            ping.number = value
            await ping.save()
        else:
            await Ping.create(id=1, number=value)


async def reset_number() -> None:
    await set_number(0)


if __name__ == "__main__":
    raise RuntimeError("This module should be imported, not run directly")

