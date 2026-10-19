from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, Field


class Mensagem(BaseModel):
    """O que o chefe envia a um agente."""
    id: str = Field(default_factory=lambda: uuid4().hex[:8])
    de: str
    para: str
    tarefa: str
    contexto: dict[str, Any] = {}


class Resposta(BaseModel):
    """O que o agente devolve ao chefe."""
    id: str
    de: str
    status: Literal["ok", "erro", "precisa_aprovacao"]
    resultado: dict[str, Any] = {}
    motivo: str = ""