1º Criação do projeto com poetry  
**poetry init**

2º Instalação do fast-api  
**poetry add "fastapi[standard]"**

3º Ativação do ambiente virtual no terminal e no compilador (ctrl + shift + p)
**poetry env activate**  
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
```python
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Inventário de hardware UNICAP", lifespan=lifespan)
```
6º criar as rotas
```python
from fastapi import APIRouter

router = APIRouter()

inventario = [
    {"id": 1, "nome": "MacBook Air", "marca": "Apple", "patrimonio": "UNI-001"},
    {"id": 2, "nome": "Dell Latitude", "marca": "Dell", "patrimonio": "UNI-002"},
]

@router.get("/")
def home():
    return {"message": "API de Inventário de Hardware - Semana de TI UNICAP"}

@router.get("/equipamentos")
def listar_equipamentos(session: Session = Depends(get_session)):
    return inventario

@router.post("/equipamentos")
def criar_equipamento(equipamento: Equipamento, session: Session = Depends(get_session)):
    novo_id = len(inventario) + 1
    equipamento.id = novo_id
    inventario.append(equipamento)
    return equipamento

@router.delete("/equipamentos/{equipamento_id}")
def deletar_equipamento(equipamento_id: int, session: Session = Depends(get_session)):
    for i, item in enumerate(inventario):
        if item["id"] == equipamento_id:
            del inventario[i]  # Removemos o item da lista original diretamente!
            return {"message": f"Equipamento {equipamento_id} removido com sucesso"}
    
    raise HTTPException(status_code=404, detail="Equipamento não encontrado")
```

7º Importar as rotas no main.py  
```python
from src.routes import router

app.include_router(router)
```
8º Rodar o servidor:  
uvicorn src.main:app --reload

9º Abrir a documentação da API e testar no Insomnia  
http://127.0.0.1:8000/docs

Equipamento para adicionar:  
```json
{"nome": "Roteador Wifi Mesh Pro", "marca": "Huawei", "patrimonio": "UNI-003"}
```

10º Instalar o SQLModel  
**poetry add sqlmodel**

11º Cria o arquivo models.py  
```python
from sqlmodel import Field, SQLModel

class Equipamento(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    marca: str
    patrimonio: str = Field(unique=True, index=True)
```
12º Criar o arquivo database.py  
```python
from sqlmodel import SQLModel, create_engine, Session

sqlite_file_name = "inventario.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# check_same_thread=False é uma exigência específica do SQLite no FastAPI
engine = create_engine(sqlite_url, echo=True, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
```

13º Adicionar a função create_db_and_tables ao main.py  
```python
from contextlib import asynccontextmanager
from src.database import create_db_and_tables
import src.models

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="Inventário de hardware UNICAP", lifespan=lifespan)
```

15º Modificar o arquivo routes  
```python
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from src.models import Equipamento
from src.database import get_session

@router.get("/equipamentos")
def listar_equipamentos(session: Session = Depends(get_session)):
equipamentos = session.exec(select(Equipamento)).all()
    return equipamentos

@router.post("/equipamentos")
def criar_equipamento(equipamento: Equipamento, session: Session = Depends(get_session)):
    session.add(equipamento)      # Adiciona o objeto na sessão
    session.commit()              # Salva de fato no banco (COMMIT)
    session.refresh(equipamento)  # Atualiza o objeto para pegar o ID gerado pelo banco
    return equipamento

@router.delete("/equipamentos/{equipamento_id}")
def deletar_equipamento(equipamento_id: int, session: Session = Depends(get_session)):
    equipamento = session.get(Equipamento, equipamento_id)
    
    if not equipamento:
        raise HTTPException(status_code=404, detail="Equipamento não encontrado")
    
    session.delete(equipamento)
    session.commit()
    return {"message": f"Equipamento {equipamento_id} removido com sucesso"}
```
16º Cadastrar os equipamentos:  
```json
{"nome": "MacBook Air", "marca": "Apple", "patrimonio": "UNI-001"},
{"nome": "Dell Latitude", "marca": "Dell", "patrimonio": "UNI-002"},
{"nome": "Roteador Wifi Mesh Pro", "marca": "Huawei", "patrimonio": "UNI-003"}
```

17º Colocar o cors no main.py para conectar ao front-end  
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Na vida real colocamos a URL certa, aqui liberamos para a oficina
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

18º Abrir o front-end e cadastrar os equipamentos
