from fastapi import APIRouter

router = APIRouter(
    prefix="/meta",
    tags=["Meta"],
)


@router.get("/test")
async def test() -> dict[str, bool]:
    return {"working": True}
