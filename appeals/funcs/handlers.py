from appeals.db.ping import get_number, set_number
from appeals.core.schemas import PingBody, PingResponse


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


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
