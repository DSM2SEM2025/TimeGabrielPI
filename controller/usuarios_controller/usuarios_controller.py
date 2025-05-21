from model.usuarios_model import (cadastrar_usuario, excluir_usuario_id, alterar_usuario, listar_usuarios, fazer_login)

def criar_usuario_controller(nome_usuario, emial_usuario, senha_usuario, tipo_conta):
    return cadastrar_usuario(nome_usuario, emial_usuario, senha_usuario, tipo_conta)

def listar_usuarios_controller():
    return listar_usuarios()

def deletar_usuario_controller(id_usuario):
    return excluir_usuario_id(id_usuario)

def atualizar_usuario_controller(id_usuario, nome_usuario, email_usuario, senha_usuario):
    return alterar_usuario(id_usuario, nome_usuario, email_usuario, senha_usuario)

def login_controller(email_usuario, senha_usuario):
    return fazer_login(email_usuario, senha_usuario)