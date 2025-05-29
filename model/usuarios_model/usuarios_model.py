# models/usuario.py

import mysql.connector
from mysql.connector import Error

def conectar():
    return mysql.connector.connect(host='localhost', user='root', password='', database='db')

def cadastrar_usuario(NOME_USUARIO, EMAIL_USUARIO, SENHA_USUARIO, TIPO_CONTA):
    try:
        db = conectar()
        cursor = db.cursor()
        cursor.execute("CALL CADASTRAR_USUARIO(%s, %s, %s, %s)", 
                       (NOME_USUARIO, EMAIL_USUARIO, SENHA_USUARIO, TIPO_CONTA))
        db.commit()
        return True
    except Exception as e:
        raise Exception(f"Erro ao cadastrar usuário: {e}")
    finally:
        if db.is_connected():
            db.close()

def excluir_usuario_id(ID_USUARIO):
    try:
        db = conectar()
        cursor = db.cursor()
        cursor.execute("CALL EXCLUIR_USUARIO_ID(%s)", (ID_USUARIO,))
        db.commit()
        return {"message": "Usuário excluído com sucesso."}
    except Exception as e:
        return {"error": f"Erro ao excluir usuário: {e}"}
    finally:
        if db.is_connected():
            db.close()



def alterar_usuario(ID_USUARIO, NOME_USUARIO, EMAIL_USUARIO, SENHA_USUARIO):
    try:
        db = conectar()
        cursor = db.cursor()
        cursor.execute("CALL ALTERAR_USUARIO(%s, %s, %s, %s)",
                       (ID_USUARIO, NOME_USUARIO, EMAIL_USUARIO, SENHA_USUARIO))
        db.commit()
        return {"message": "Usuário alterado com sucesso."}
    except Exception as e:
        return {"error": f"Erro ao alterar usuário: {e}"}
    finally:
        if db.is_connected():
            db.close()

def listar_usuarios():
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.callproc("LISTAR_USUARIOS")
        
        usuarios = []
        for result in cursor.stored_results():
            usuarios.extend(result.fetchall())

        cursor.close()
        conn.close()
        return usuarios
    except mysql.connector.Error as error:
        return []


def fazer_login(EMAIL_USUARIO, SENHA_USUARIO):
    try:
        db = conectar()
        cursor = db.cursor(dictionary=True)
        cursor.execute("CALL FAZER_LOGIN(%s, %s)", (EMAIL_USUARIO, SENHA_USUARIO))
        result = cursor.fetchone()
        
        if result and result.get("MENSAGEM") == "LOGIN FEITO COM SUCESSO":
            return {
                "message": result["MENSAGEM"],
                "user": {
                    "id": result["ID_USUARIO"],
                    "nome": result["NOME_USUARIO"],
                    "email": result["EMAIL_USUARIO"],
                    "tipo_conta": result["TIPO_CONTA"]
                }
            }
        else:
            return {"error": "Credenciais inválidas."}

    except Exception as e:
        return {"error": f"Erro ao fazer login: {e}"}
    finally:
        if db.is_connected():
            db.close()


