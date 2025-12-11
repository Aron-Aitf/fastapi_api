from fastapi import FastAPI

from config import config
from routers.meta_router import router as meta_router
from routers.add_router import router as add_router
from routers.query_router import router as query_router
from routers.delete_router import router as delete_router
from routers.update_router import router as update_router
from routers.debug_router import router as debug_router

app = FastAPI(
    swagger_ui_parameters={"tryItOutEnabled": True},
    title=config.docs.title,
    debug=config.app.debug,
    version=str(config.docs.version),
    description=config.docs.description,
)


@app.get("/", tags=["Meta"])
async def home() -> dict[str, str]:
    return {
        "title": config.docs.title,
        "description": config.docs.description,
        "version": str(config.docs.version),
    }


app.include_router(meta_router)
app.include_router(add_router)
app.include_router(query_router)
app.include_router(delete_router)
app.include_router(update_router)
app.include_router(debug_router)
