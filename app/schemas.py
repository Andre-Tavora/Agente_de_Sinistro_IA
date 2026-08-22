from pydantic import BaseModel


class Apolice(BaseModel):
    numero: str
    segurado: str
    cobertura: str
    vigencia_inicio: str
    vigencia_fim: str


class Sinistro(BaseModel):
    id: str
    numero_apolice: str
    tipo: str
    descricao: str
    status: str


class Vistoria(BaseModel):
    id: str
    sinistro_id: str
    data_agendada: str
    endereco: str
    status: str


class ToolCall(BaseModel):
    tool_name: str
    payload: dict


class ToolResult(BaseModel):
    tool_name: str
    success: bool
    data: dict | str | None
