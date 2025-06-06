from model.usuarios_model.usuarios_model import (conectar, cadastrar_usuario, excluir_usuario_id, alterar_usuario, listar_usuarios, fazer_login)
from utils.auth import criar_token

def criar_usuario_controller(email_usuario, senha_usuario):
    return cadastrar_usuario(email_usuario, senha_usuario)

def listar_usuarios_controller():
    return listar_usuarios()

def deletar_usuario_controller(id_usuario):
    return excluir_usuario_id(id_usuario)

def atualizar_usuario_controller(id_usuario,email_usuario, senha_usuario):
    return alterar_usuario(id_usuario,email_usuario, senha_usuario)

def fazer_login_controller(email_usuario, senha_usuario):
    usuario = fazer_login(email_usuario, senha_usuario)
    
    if usuario and "user" in usuario:
        dados = {
            "sub": str(usuario["user"]["id"]),
            "email_usuario": usuario["user"]["email"]
        }
        token = criar_token(dados)
        return {
            "access_token": token,
            "token_type": "bearer",
            "usuario": dados
        }
    return None


