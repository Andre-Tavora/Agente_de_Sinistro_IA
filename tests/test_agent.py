import pytest
from app.agent import processar_mensagem, decide_tool
from app.schemas import ToolResult


def test_consultar_apolice_sucesso():
    resultado = processar_mensagem("quero consultar a apolice AP001")
    assert isinstance(resultado, ToolResult)
    assert resultado.success is True
    assert resultado.data["segurado"] == "Carlos Tavora"


def test_consultar_apolice_inexistente():
    resultado = processar_mensagem("quero consultar a apolice AP999")
    assert resultado.success is False


def test_consultar_sinistro_sucesso():
    resultado = processar_mensagem("consultar sinistro SN002")
    assert resultado.success is True
    assert resultado.data["status"] == "em análise"


def test_consultar_vistoria_sucesso():
    resultado = processar_mensagem("consultar vistoria VT004")
    assert resultado.success is True
    assert resultado.data["status"] == "agendada"


def test_abrir_sinistro_sucesso():
    resultado = processar_mensagem("abrir sinistro AP003")
    assert resultado.success is True
    assert resultado.data["numero_apolice"] == "AP003"
    assert resultado.data["status"] == "aberto"


def test_mensagem_sem_tool_mapeada():
    with pytest.raises(ValueError):
        decide_tool("mensagem qualquer sem palavra-chave")
