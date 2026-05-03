1º Criação do projeto com poetry
poetry init

2º Instalação do fast-api
poetry add "fastapi[standard]"

3º Ativação do ambiente virtual no terminal
poetry env activate
(colar comando para ativar)

4º Criar arquitetura:
inventario-hardware-api/
│
├── pyproject.toml         # Arquivo de configuração do Poetry (dependências)
├── poetry.lock            # Arquivo de lock gerado pelo Poetry
│
└── src/                   # Pasta onde fica todo o código da nossa API
    ├── main.py            # Ponto de entrada: inicializa o FastAPI e junta tudo
    ├── database.py        # Configuração da conexão com o Banco de Dados
    ├── models.py          # Onde definimos a estrutura do Equipamento (Tabelas e Validações)
    └── routes.py          # Onde criamos as rotas (GET, POST, DELETE)

5º Criar o main.py
6º criar as rotas
7º Importar as rotas no main.py
8º Rodar o servidor:
uvicorn src.main:app --reload

9º Abrir a documentação da API
http://127.0.0.1:8000/docs

10º Instalar o SQLModel
poetry add sqlmodel

11º Cria o arquivo models.py
from sqlmodel import Field, SQLModel

class Equipamento(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    marca: str
    patrimonio: str = Field(unique=True, index=True)

12º Criar o arquivo database.py
from sqlmodel import SQLModel, create_engine

sqlite_file_name = "inventario.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# check_same_thread=False é uma exigência específica do SQLite no FastAPI
engine = create_engine(sqlite_url, echo=True, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

13º Adicionar a função create_db_and_tables ao main.py
from contextlib import asynccontextmanager
from src.database import create_db_and_tables
import src.models

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="Inventário de hardware UNICAP", lifespan=lifespan)

14º Adicionar Session ao arquivo database.py
from sqlmodel import SQLModel, create_engine, Session

def get_session():
    with Session(engine) as session:
        yield session

15º Modificar o arquivo routes
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from src.models import Equipamento
from src.database import get_session

16º Colocar o cors
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Na vida real colocamos a URL certa, aqui liberamos para a oficina
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)