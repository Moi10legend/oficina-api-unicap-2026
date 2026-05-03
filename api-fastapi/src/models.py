from sqlmodel import Field, SQLModel

class Equipamento(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    marca: str
    patrimonio: str = Field(unique=True, index=True)