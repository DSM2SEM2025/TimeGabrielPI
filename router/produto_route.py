from pydantic import BaseModel
from typing import AbstractSet, Optional, List
from fastapi import APIRouter, HTTPException
from controller.produtos_controller.produtos_controller import insert_produto_controller, update_produto_controller, search_produto_controller, delete_produto_controller, list_produto_estoque

router = APIRouter()

class Produto(BaseModel):
    nome_produto: str
    preco_procuto: float
    desc_produto: str
class Estoque(BaseModel):
    tipo_estoque: str
    qtde_estoque: int


@router.post("/produto", status_code=201)
def cadastrar_produto_router(produto: Produto, estoque: Estoque):
    try:
        insert_produto_controller(
            produto.nome_produto,
            produto.preco_procuto,
            produto.desc_produto,
            estoque.tipo_estoque,
            estoque.qtde_estoque
        )
        return {"message": "Produto e estoque cadastrados com sucesso!"} # Retorne uma mensagem de sucesso
    except Exception as err:
        raise HTTPException(status_code=400, detail=str(err))
    

@router.get("/produto/{id}")
def search_produto_router(id:int):
    produto_data = search_produto_controller(id)
    if produto_data:
        return {"message": "Produto localizado", "data": produto_data}
    else:
        return {"message": "Nenhum produto encontrado com essa ID."}
    


@router.get("/produto", status_code=201, summary="Lista todos os produtos disponiveis")
def list_produto_router():
    produtos_data=list_produto_estoque()

    if produtos_data:
        return {"message": "Produtos listados com sucesso!", "data": produtos_data}
    else:
        return {"message": "Nenhum produto encontrado.", "data": []}

        

    