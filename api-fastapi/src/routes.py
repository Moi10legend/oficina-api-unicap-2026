from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from src.models import Equipamento
from src.database import get_session

# O APIRouter funciona como uma "mini aplicação" de rotas
router = APIRouter()

# Dados em memória para a oficina
inventario = [
    {"id": 1, "nome": "MacBook Air", "marca": "Apple", "patrimonio": "UNI-001"},
    {"id": 2, "nome": "Dell Latitude", "marca": "Dell", "patrimonio": "UNI-002"},
]

@router.get("/")
def home():
    return {"message": "API de Inventário de Hardware - Semana de TI UNICAP"}

# 1. Rota para LER todos
@router.get("/equipamentos")
def listar_equipamentos(session: Session = Depends(get_session)):
    # return inventario

    equipamentos = session.exec(select(Equipamento)).all()
    return equipamentos

# 2. Rota para CRIAR
@router.post("/equipamentos")
def criar_equipamento(equipamento: Equipamento, session: Session = Depends(get_session)):
    # novo_id = len(inventario) + 1
    # equipamento.id = novo_id
    # inventario.append(equipamento)
    # return equipamento

    session.add(equipamento)      # Adiciona o objeto na sessão
    session.commit()              # Salva de fato no banco (COMMIT)
    session.refresh(equipamento)  # Atualiza o objeto para pegar o ID gerado pelo banco
    return equipamento

# 3. Rota para DELETAR
@router.delete("/equipamentos/{equipamento_id}")
def deletar_equipamento(equipamento_id: int, session: Session = Depends(get_session)):
    # for i, item in enumerate(inventario):
    #     if item["id"] == equipamento_id:
    #         del inventario[i]  # Removemos o item da lista original diretamente!
    #         return {"message": f"Equipamento {equipamento_id} removido com sucesso"}
    
    # raise HTTPException(status_code=404, detail="Equipamento não encontrado")

    equipamento = session.get(Equipamento, equipamento_id)
    
    if not equipamento:
        raise HTTPException(status_code=404, detail="Equipamento não encontrado")
    
    session.delete(equipamento)
    session.commit()
    return {"message": f"Equipamento {equipamento_id} removido com sucesso"}