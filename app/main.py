from fastapi import FastAPI
from starlette_exporter import PrometheusMiddleware, handle_metrics
from app.api.routes.clips import router as clips_router
from app.core.config import settings
from app.db.models import Base
from app.db.database import engine
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.add_middleware(
    PrometheusMiddleware,
    app_name="clips_service",
    group_paths=True,
    prefix="clips_api",
)

app.add_route("/metrics", handle_metrics)
app.include_router(
    clips_router,
    prefix=f"{settings.API_V1_STR}/clips",
    tags=["clips"]
)

@app.get("/")
def root():
    return {"message": "Welcome to the Clips API Service"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
