from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List
from fastapi import Depends
from utils.auth import pegar_usuario
from controller.usuarios_controller.usuarios_controller import (
    criar_usuario_controller,
    listar_usuarios_controller,
    deletar_usuario_controller,
    atualizar_usuario_controller,
    fazer_login_controller
)

router = APIRouter()

class Usuario(BaseModel):
    email_usuario: EmailStr
    senha_usuario: str

class UsuarioUpdate(BaseModel):
    id_usuario: int
    email_usuario: EmailStr
    senha_usuario: str

class Login(BaseModel):
    email_usuario: EmailStr
    senha_usuario: str

@router.post("/usuarios", status_code=201)
def criar_usuario(usuario: Usuario):
    try:
        criar_usuario_controller(
            usuario.email_usuario,
            usuario.senha_usuario
        )
        return {"mensagem": "Usuário cadastrado com sucesso."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/usuarios", response_model=List[dict])
def listar():
    return listar_usuarios_controller()

@router.delete("/usuarios/{id}")
def deletar_usuario(id: int):
    deletar_usuario_controller(id)
    return {"mensagem": f"Usuário com ID {id} excluído com sucesso."}

@router.put("/usuarios")
def atualizar(usuario: UsuarioUpdate):
    atualizar_usuario_controller(
        usuario.id_usuario,
        usuario.email_usuario,
        usuario.senha_usuario
    )
    return {"mensagem": f"Usuário com ID {usuario.id_usuario} atualizado com sucesso."}

@router.post("/login")
def login(dados: Login):
    usuario = fazer_login_controller(dados.email_usuario, dados.senha_usuario)
    if usuario:
        return usuario
    raise HTTPException(status_code=401, detail="Credenciais inválidas.")