from pydantic import BaseModel, ConfigDict
from typing import Optional

class ClienteResponseSchema(BaseModel):
    id: int
    nome: Optional[str]
    email: Optional[str]
    telefone: Optional[str]
    cpf: Optional[str]

    model_config = ConfigDict(from_attributes=True)