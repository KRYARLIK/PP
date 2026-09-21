from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.api.routes import router
from app.db.database import Base, engine
from app.settings import settings

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    description="Backend for parking occupancy detection with YOLO + configurable parking polygons.",
    version="1.0.0",
)

app.include_router(router)
app.mount("/output", StaticFiles(directory=str(settings.output_dir)), name="output")


@app.get("/", response_class=HTMLResponse)
def index():
    return FileResponse("app/static/index.html")
