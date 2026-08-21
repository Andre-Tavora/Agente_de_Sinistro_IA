import os
from dotenv import load_dotenv
from fastapi import Header, HTTPException

load_dotenv()
MOCK_TOKEN = os.getenv("MOCK_API_TOKEN")

def verify_token(authorization: str = Header(...)):
    if authorization != f"Bearer {MOCK_TOKEN}":
        raise HTTPException(status_code=401, detail="Token inválido")
