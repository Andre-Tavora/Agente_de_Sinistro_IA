from fastapi import FastAPI

app = FastAPI(title="Agente de Sinistro IA")

@app.get("/")
def root():
    return {"status": "ok"}
