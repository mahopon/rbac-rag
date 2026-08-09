from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic here
    yield
    # Shutdown logic here


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    from src.router import router

    app.include_router(router)
    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
