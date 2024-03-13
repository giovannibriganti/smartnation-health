from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html

from nosql.app.app.config.database import init_db, close_db
from nosql.app.app.routes.patient_routes import router

app = FastAPI(title="SmartNation AI Hackathon API", version="0.1.0")

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html_github():
    return get_swagger_ui_html(
    openapi_url=app.openapi_url,
    title=f"{app.title} - Swagger UI",
    # swagger_ui_dark.css raw url
    swagger_css_url="https://raw.githubusercontent.com/Itz-fork/Fastapi-Swagger-UI-Dark/main/assets/swagger_ui_dark.min.css"
)

app.include_router(router)

@app.on_event("startup")
async def start_db():
    await init_db()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_db()