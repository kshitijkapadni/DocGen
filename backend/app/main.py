from fastapi import FastAPI
from app.routes import docgen

app = FastAPI(title="DocGen MVP")

app.include_router(docgen.router, prefix="/docgen", tags=["Documentation"])
