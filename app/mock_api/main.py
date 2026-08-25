import uuid

from fastapi import FastAPI, HTTPException

app = FastAPI(title="Mock API - Seguradora")


APOLICES = {
    "AP001": {"numero": "AP001", "segurado": "Carlos Tavora", "cobertura": "Roubo/Furto", "vigencia_inicio": "2026-01-01", "vigencia_fim": "2026-12-31"},
    "AP002": {"numero": "AP002", "segurado": "Mariana Souza", "cobertura": "Incêndio/Alagamento", "vigencia_inicio": "2026-03-15", "vigencia_fim": "2027-03-15"},
    "AP003": {"numero": "AP003", "segurado": "João Pedro Lima", "cobertura": "Roubo/Furto", "vigencia_inicio": "2025-09-30", "vigencia_fim": "2026-09-30"},
    "AP004": {"numero": "AP004", "segurado": "Fernanda Alves", "cobertura": "Vida", "vigencia_inicio": "2026-01-20", "vigencia_fim": "2027-01-20"},
    "AP005": {"numero": "AP005", "segurado": "Ricardo Nunes", "cobertura": "Colisão", "vigencia_inicio": "2025-11-05", "vigencia_fim": "2026-11-05"},
}

SINISTROS = {
    "SN001": {"id": "SN001", "numero_apolice": "AP001", "tipo": "Roubo/Furto", "descricao": "Colisão traseira", "status": "aberto"},
    "SN002": {"id": "SN002", "numero_apolice": "AP002", "tipo": "Alagamento", "descricao": "Vazamento causou dano estrutural", "status": "em análise"},
    "SN003": {"id": "SN003", "numero_apolice": "AP003", "tipo": "Roubo/Furto", "descricao": "Furto de rodas", "status": "encerrado"},
    "SN004": {"id": "SN004", "numero_apolice": "AP004", "tipo": "Vida", "descricao": "Documentação pendente", "status": "aberto"},
    "SN005": {"id": "SN005", "numero_apolice": "AP005", "tipo": "Colisão", "descricao": "Colisão lateral em cruzamento", "status": "em análise"},
}

VISTORIAS = {
    "VT001": {"id": "VT001", "sinistro_id": "SN001", "data_agendada": "2026-08-16", "endereco": "Rua A, 123 - Fortaleza", "status": "concluída"},
    "VT002": {"id": "VT002", "sinistro_id": "SN002", "data_agendada": "2026-07-05", "endereco": "Av. B, 456 - Fortaleza", "status": "concluída"},
    "VT003": {"id": "VT003", "sinistro_id": "SN003", "data_agendada": "2026-06-12", "endereco": "Rua C, 789 - Fortaleza", "status": "concluída"},
    "VT004": {"id": "VT004", "sinistro_id": "SN005", "data_agendada": "2026-08-19", "endereco": "Av. D, 321 - Fortaleza", "status": "agendada"},
}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/apolices/{numero_apolice}")
def get_apolice(numero_apolice: str):
    apolice = APOLICES.get(numero_apolice)
    if not apolice:
        raise HTTPException(status_code=404, detail=f"Apólice {numero_apolice} não encontrada")
    return apolice


@app.get("/sinistros/{sinistro_id}")
def get_sinistro(sinistro_id: str):
    sinistro = SINISTROS.get(sinistro_id)
    if not sinistro:
        raise HTTPException(status_code=404, detail=f"Sinistro {sinistro_id} não encontrado")
    return sinistro


@app.post("/sinistros", status_code=201)
def post_sinistro(payload: dict):
    numero_apolice = payload.get("numero_apolice")
    tipo = payload.get("tipo")
    descricao = payload.get("descricao")

    if not numero_apolice or not tipo or not descricao:
        raise HTTPException(status_code=422, detail="Campos obrigatórios ausentes: numero_apolice, tipo, descricao")

    if numero_apolice not in APOLICES:
        raise HTTPException(status_code=404, detail=f"Apólice {numero_apolice} não encontrada")

    novo_id = f"SN{str(uuid.uuid4().int)[:6]}"
    novo_sinistro = {
        "id": novo_id,
        "numero_apolice": numero_apolice,
        "tipo": tipo,
        "descricao": descricao,
        "status": "aberto",
    }
    SINISTROS[novo_id] = novo_sinistro
    return novo_sinistro


@app.get("/vistorias/{vistoria_id}")
def get_vistoria(vistoria_id: str):
    vistoria = VISTORIAS.get(vistoria_id)
    if not vistoria:
        raise HTTPException(status_code=404, detail=f"Vistoria {vistoria_id} não encontrada")
    return vistoria


@app.post("/vistorias", status_code=201)
def post_vistoria(payload: dict):
    sinistro_id = payload.get("sinistro_id")
    data_agendada = payload.get("data_agendada")
    endereco = payload.get("endereco")

    if not sinistro_id or not data_agendada or not endereco:
        raise HTTPException(status_code=422, detail="Campos obrigatórios ausentes: sinistro_id, data_agendada, endereco")

    if sinistro_id not in SINISTROS:
        raise HTTPException(status_code=404, detail=f"Sinistro {sinistro_id} não encontrado")

    novo_id = f"VT{str(uuid.uuid4().int)[:6]}"
    nova_vistoria = {
        "id": novo_id,
        "sinistro_id": sinistro_id,
        "data_agendada": data_agendada,
        "endereco": endereco,
        "status": "agendada",
    }
    VISTORIAS[novo_id] = nova_vistoria
    return nova_vistoria
