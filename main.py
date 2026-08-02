from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api import dashboard, history, malware, password, tips, url_scanner
from app.core.config import settings
from app.core.database import init_db
from app.utils.logger import get_logger

log = get_logger("main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    log.info("%s v%s ready (db=%s)", settings.app_name, settings.app_version, settings.database_url)
    yield


app = FastAPI(title=settings.app_name, version=settings.app_version, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(password.router)
app.include_router(url_scanner.router)
app.include_router(malware.router)
app.include_router(dashboard.router)
app.include_router(history.router)
app.include_router(tips.router)


@app.get("/api/health", tags=["Health"])
def health():
    return {"status": "ok", "app": settings.app_name, "version": settings.app_version}


# Serve the standalone frontend (index.html, dashboard.html, css/, js/, ...)
# for convenience during local development.
FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
