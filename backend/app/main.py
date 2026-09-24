from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.foods.nutrition_router import router as nutrition_router
from app.foods.router import router as foods_router


def create_app() -> FastAPI:
    app = FastAPI(title="FitMeal AI API", version="0.1.0")
    app.include_router(foods_router)
    app.include_router(nutrition_router)

    @app.get("/healthz", tags=["ops"])
    async def healthz(session: Annotated[AsyncSession, Depends(get_session)]) -> dict[str, str]:
        await session.execute(text("SELECT 1"))
        return {"status": "ok"}

    return app


app = create_app()
