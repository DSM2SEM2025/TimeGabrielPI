from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from utils.auth import pegar_usuario
from controller.produtos_controller.produtos_controller import (
    insert_produto_controller,
    update_produto_controller,
    search_produto_controller,
    delete_produto_controller,
    list_produto_estoque
)

router = APIRouter()

class Produto(BaseModel):
    nome_produto: str
    preco_produto: float  
    desc_produto: str

class Estoque(BaseModel):
    tipo_estoque: str
    qtde_estoque: int

class ProdutoUpdate(BaseModel):
    nome_produto: str
    preco_produto: float  
    desc_produto: str
    tipo_estoque: str
    qtde_estoque: int
    tipo_atualizacao: int 

class ProdutoDelete(BaseModel):
    nome_produto: str

@router.post("/produto", status_code=201)
# def cadastrar_produto_router(produto: Produto, estoque: Estoque):
def cadastrar_produto_router(produto: Produto, estoque: Estoque, usuario=Depends(pegar_usuario)):
    try:
        insert_produto_controller(
            produto.nome_produto,
            produto.preco_produto,
            produto.desc_produto,
            estoque.tipo_estoque,
            estoque.qtde_estoque
        )
        return {"message": "Produto e estoque cadastrados com sucesso!"}
    except Exception as err:
        raise HTTPException(status_code=400, detail=str(err))

@router.get("/produto/{id}")
#def search_produto_router(id: int):
def search_produto_router(id: int, usuario=Depends(pegar_usuario)):
    produto_data = search_produto_controller(id)
    if produto_data:
        return {"message": "Produto localizado", "data": produto_data}
    else:
        raise HTTPException(status_code=404, detail="Nenhum produto encontrado com essa ID.")

@router.get("/produto", response_model=List[dict])
#def list_produto_router():
def list_produto_router(usuario=Depends(pegar_usuario)):
        return list_produto_estoque()


@router.delete("/produto/{id}", status_code=200, summary="Excluir produto pelo ID")
#def excluir_produto_router(id: int):
def excluir_produto_router(id: int, usuario=Depends(pegar_usuario)):
    result = delete_produto_controller(id)
    if result[0]:  # Excluído com sucesso
        return {"message": f"Produto com ID '{id}' excluído com sucesso."}
    else:
        raise HTTPException(status_code=404, detail=result[1])

@router.put("/produto")
#def atualizar_produto_router(produto: ProdutoUpdate):
def atualizar_produto_router(produto: ProdutoUpdate, usuario=Depends(pegar_usuario)):
    update_produto_controller(
        produto.nome_produto,
        produto.preco_produto,
        produto.desc_produto,
        produto.tipo_estoque,
        produto.qtde_estoque,
        produto.tipo_atualizacao
    )
    return {"message": "Produto atualizado com sucesso."}