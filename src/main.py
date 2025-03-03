import os

from fastapi import FastAPI, Request
from api import project_router, user_router, tenent_router

app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")

app.include_router(user_router, prefix="/api")
app.include_router(project_router, prefix="/api")
app.include_router(tenent_router, prefix="/api")
app.include_router(auth_router, prefix="/api")