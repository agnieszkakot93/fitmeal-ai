from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.router import router as auth_router
from app.core.db import get_session
from app.foods.nutrition_router import router as nutrition_router
from app.foods.router import router as foods_router
from app.importjobs.router import router as imports_router
from app.plans.router import router as plans_router
from app.recipes.router import router as recipes_router
from app.users.router import router as users_router

# One router per feature. A feature adds its import above and one line here;
# keep it the only change a feature makes to this file.
ROUTERS = [
    foods_router,
    nutrition_router,
    recipes_router,
    auth_router,
    users_router,
    plans_router,
    imports_router,
]


def create_app() -> FastAPI:
    app = FastAPI(title="Donut API", version="0.1.0")
    for router in ROUTERS:
        app.include_router(router)

    @app.get("/healthz", tags=["ops"])
    async def healthz(session: Annotated[AsyncSession, Depends(get_session)]) -> dict[str, str]:
        await session.execute(text("SELECT 1"))
        return {"status": "ok"}

    return app


app = create_app()
