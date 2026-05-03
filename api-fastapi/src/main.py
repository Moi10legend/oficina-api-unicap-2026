from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from src.routes import router
from src.database import create_db_and_tables
from fastapi.middleware.cors import CORSMiddleware
import src.models

#Lifespan: Código que roda quando a API liga
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="Inventário de hardware UNICAP", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Na vida real colocamos a URL certa, aqui liberamos para a oficina
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)