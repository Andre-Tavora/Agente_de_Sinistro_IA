import re
import logging
from app.schemas import ToolCall, ToolResult
from app.services.apolice_client import consultar_apolice
from app.services.sinistro_client import consultar_sinistro, abrir_sinistro
from app.services.vistoria_client import consultar_vistoria, agendar_vistoria

logger = logging.getLogger("agent")
logging.basicConfig(level=logging.INFO)

TOOLS = {
    "consultar_apolice": consultar_apolice,
    "consultar_sinistro": consultar_sinistro,
    "abrir_sinistro": abrir_sinistro,
    "consultar_vistoria": consultar_vistoria,
    "agendar_vistoria": agendar_vistoria,
}


def decide_tool(mensagem: str) -> ToolCall:
    mensagem_lower = mensagem.lower()

    if "abrir sinistro" in mensagem_lower or "abrir um sinistro" in mensagem_lower:
        numero_apolice = _extrair_codigo(mensagem, prefixo="AP")
        return ToolCall(
            tool_name="abrir_sinistro",
            payload={
                "numero_apolice": numero_apolice,
                "tipo": "não especificado",
                "descricao": mensagem,
            },
        )

    if "agendar vistoria" in mensagem_lower:
        sinistro_id = _extrair_codigo(mensagem, prefixo="SN")
        return ToolCall(
            tool_name="agendar_vistoria",
            payload={
                "sinistro_id": sinistro_id,
                "data_agendada": "não especificada",
                "endereco": "não especificado",
            },
        )

    if "sinistro" in mensagem_lower:
        sinistro_id = _extrair_codigo(mensagem, prefixo="SN")
        return ToolCall(tool_name="consultar_sinistro", payload={"sinistro_id": sinistro_id})

    if "vistoria" in mensagem_lower:
        vistoria_id = _extrair_codigo(mensagem, prefixo="VT")
        return ToolCall(tool_name="consultar_vistoria", payload={"vistoria_id": vistoria_id})

    if "apolice" in mensagem_lower or "apólice" in mensagem_lower:
        numero_apolice = _extrair_codigo(mensagem, prefixo="AP")
        return ToolCall(tool_name="consultar_apolice", payload={"numero_apolice": numero_apolice})

    raise ValueError(f"Nenhuma tool mapeada para a mensagem: '{mensagem}'")


def _extrair_codigo(mensagem: str, prefixo: str) -> str:
    palavras = mensagem.upper().split()
    padrao = re.compile(rf"^{prefixo}\d+$")
    for palavra in palavras:
        if padrao.match(palavra):
            return palavra
    raise ValueError(f"Código com prefixo {prefixo} não encontrado na mensagem")


def execute_tool(tool_call: ToolCall) -> ToolResult:
    logger.info(f"Tool escolhida: {tool_call.tool_name} | payload: {tool_call.payload}")

    tool_fn = TOOLS.get(tool_call.tool_name)
    if tool_fn is None:
        logger.error(f"Tool desconhecida: {tool_call.tool_name}")
        return ToolResult(tool_name=tool_call.tool_name, success=False, data=None)

    try:
        resultado = tool_fn(**tool_call.payload)
        data = resultado.model_dump() if hasattr(resultado, "model_dump") else resultado
        logger.info(f"Resposta da tool {tool_call.tool_name}: {data}")
        return ToolResult(tool_name=tool_call.tool_name, success=True, data=data)
    except Exception as e:
        logger.error(f"Erro ao executar tool {tool_call.tool_name}: {e}")
        return ToolResult(tool_name=tool_call.tool_name, success=False, data=str(e))


def processar_mensagem(mensagem: str) -> ToolResult:
    logger.info(f"Mensagem recebida: '{mensagem}'")
    tool_call = decide_tool(mensagem)
    return execute_tool(tool_call)
