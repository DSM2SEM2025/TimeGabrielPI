from fastapi import FastAPI
from router.usuarios_router import router as usuario_router
from router.produto_route import router as produto_router

from db_setup import criar_banco_de_dados, criar_tabelas

app = FastAPI()

@app.on_event("startup")
async def startup():
    # Cria o banco de dados, se não existir
    criar_banco_de_dados()
    
    # Cria as tabelas e procedures
    criar_tabelas()

# Inclui a router de usuários
app.include_router(usuario_router, prefix="/usuarios", tags=["Usuários"])


@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Produtos!"}

app.include_router(produto_router, prefix="/produtos", tags=["Produtos"]) # Mantive o prefixo para consistência

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
