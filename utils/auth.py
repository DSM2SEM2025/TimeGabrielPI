from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import FastAPI, Depends, HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.status import HTTP_403_FORBIDDEN, HTTP_401_UNAUTHORIZED

secret_key = "chave_secreta"
algorithm = "HS256"
expire_days = 7

app = FastAPI()

security = HTTPBearer()  # Define o esquema Bearer token

def criar_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=expire_days)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return token

def verificar_token(token: str):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload
    except JWTError:
        return None

# Função para extrair e validar o token do header Authorization
def pegar_usuario(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials  # token puro extraído do header
    payload = verificar_token(token)
    if payload is None:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload
