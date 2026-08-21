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
