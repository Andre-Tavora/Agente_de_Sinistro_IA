def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_get_apolice(client, auth_header):
    response = client.get("/apolice/AP001", headers=auth_header)
    assert response.status_code == 200
    assert response.json()["numero"] == "AP001"

def test_get_apolice_nao_existe(client, auth_header):
    response = client.get("/apolice/AP999", headers=auth_header)
    assert response.status_code == 404

def test_get_apolice_sem_token(client):
    response = client.get("/apolice/AP001")
    assert response.status_code == 401

def test_get_sinistro(client, auth_header):
    response = client.get("/sinistro/SN001", headers=auth_header)
    assert response.status_code == 200
    assert response.json()["id"] == "SN001"

def test_get_sinistro_nao_existe(client, auth_header):
    response = client.get("/sinistro/SN999", headers=auth_header)
    assert response.status_code == 404

def test_get_sinistro_sem_token(client):
    response = client.get("/sinistro/SN001")
    assert response.status_code == 401

def test_get_vistoria(client, auth_header):
    response = client.get("/vistoria/VT001", headers=auth_header)
    assert response.status_code == 200
    assert response.json()["id"] == "VT001"

def test_get_vistoria_nao_existe(client, auth_header):
    response = client.get("/vistoria/VT999", headers=auth_header)
    assert response.status_code == 404

def test_get_vistoria_sem_token(client):
    response = client.get("/vistoria/VT001")
    assert response.status_code == 401
