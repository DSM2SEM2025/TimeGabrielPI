from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from datetime import date
from utils.auth import pegar_usuario
from controller.produtos_controller.produtos_controller import (
    insert_produto_controller,
    update_produto_controller,
    search_produto_controller,
    delete_produto_estoque_controller,
    list_produto_estoque,
    iniciar_coleta_email_controller
)

router = APIRouter()

class Produto(BaseModel):
    nome_produto: str
    preco_produto: float  
    desc_produto: str
    numero_nf_produto:str
    validade_produto: date
    fornecedor_produto: str
    qtd_minima_produto: int

class Estoque(BaseModel):
    id_estoque: int
    categoria_estoque: str
    qtde_estoque: int

class ProdutoUpdate(BaseModel):
    id_produto: int
    nome_produto: str
    preco_produto: float  
    desc_produto: str
    numero_nf_produto: str
    validade_produto: date
    fornecedor_produto: str
    qtd_minima_produto: int

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
            estoque.categoria_estoque,
            estoque.qtde_estoque,
            produto.numero_nf_produto,
            produto.validade_produto,
            produto.fornecedor_produto,
            produto.qtd_minima_produto
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
    result = delete_produto_estoque_controller(id)
    if result[0]:  # Excluído com sucesso
        return {"message": f"Produto com ID '{id}' excluído com sucesso."}
    else:
        raise HTTPException(status_code=404, detail=result[1])

@router.put("/produto")
#def atualizar_produto_router(produto: ProdutoUpdate):
def atualizar_produto_router(produto: ProdutoUpdate, estoque: Estoque, usuario=Depends(pegar_usuario)):
    update_produto_controller(
        estoque.id_estoque,
        estoque.categoria_estoque,
        estoque.qtde_estoque,        
        
        produto.id_produto,
        produto.nome_produto,
        produto.preco_produto,
        estoque.id_estoque,
        produto.desc_produto,
        produto.numero_nf_produto,
        produto.validade_produto,
        produto.fornecedor_produto,
        produto.qtd_minima_produto
    )
    return {"message": "Produto atualizado com sucesso."}

@router.get("/coleta-email", summary="Coleta dados de e-mails do Gmail com anexos PDF")
def coleta_email_router(usuario=Depends(pegar_usuario)):
    try:
        result = iniciar_coleta_email_controller()
        return {"message": "Coleta de e-mail concluída", "resultado": str(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na coleta de e-mails: {e}")