from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List
from model.estoque_model.estoque_model import(
    excluir_produto,
    consultar_historico,
    gerar_relatorio,
    registrar_movimento,
    verificar_entrega
)

router = APIRouter()

@router.delete("/estoque/{produto_id}/{estoque_id}")
def deletar_produto(produto_id: int, estoque_id: id):
    excluir_produto(produto_id, estoque_id)
    return {"menssagem": f"Produto com o ID {produtp_id} excluido com sucesso!"}

@router.get("/estoque/historico/{produto_id}")
def consultar(produto_id: int):
    retorno = consultar_historico(produto_id)
    return retorno

@router.get("/estoque/{estoque_id}")
def relatorio(estoque_id : int)
    retorno = gerar_relatorio(estoque_id)
    return retorno

@router.post("/produtos/movimento")
def registrar_movimento_produto(produto_id: int, qtde: int, tipo_movimentacao: str)
    retorno = registrar_movimento(produto_id, qtde, tipo_movimentacao)
    return retorno

@router.put("/produtos/entrega/{id_entrega}")
def entrega(id_entrega: int)
    retorno = verificar_entrega(id_entrega)
    return retorno