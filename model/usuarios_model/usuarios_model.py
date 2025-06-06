from database.db_mysql import MySqlConnector
from database.db_model import DBModel
from mysql.connector import Error
from pydantic import BaseModel, ValidationError
from typing import Optional, Protocol

def cadastrar_usuario(EMAIL_USUARIO, SENHA_USUARIO):
    config = DBModel.get_dotenv()
    db = MySqlConnector(config)
    conn, msg = db.connection()
    try:
        cursor = conn.cursor()
        command = "CALL CADASTRAR_USUARIO(%s, %s)"
        values = ( EMAIL_USUARIO, SENHA_USUARIO)
        cursor.execute(command, values)
        conn.commit()
        return True
    except Exception as e:
        raise Exception(f"Erro ao cadastrar usuário: {e}")
    finally:
        if cursor:
            cursor.close()
        if db:
            conn.close()

def excluir_usuario_id(ID_USUARIO):
    config = DBModel.get_dotenv()
    db = MySqlConnector(config)
    conn, msg = db.connection()
    try:
        cursor = conn.cursor()
        command = "CALL EXCLUIR_USUARIO_ID(%s)"
        values = (ID_USUARIO,)
        cursor.execute(command, values)
        conn.commit()
        return {"message": "Usuário excluído com sucesso."}
    except Exception as e:
        return {"error": f"Erro ao excluir usuário: {e}"}
    finally:
        if cursor:
            cursor.close()
        if db:
            conn.close()

def alterar_usuario(ID_USUARIO, EMAIL_USUARIO, SENHA_USUARIO):
    config = DBModel.get_dotenv()
    db = MySqlConnector(config)
    conn, msg = db.connection()
    try:
        cursor = conn.cursor()
        command = "CALL ALTERAR_USUARIO(%s, %s, %s)"
        values = (ID_USUARIO, EMAIL_USUARIO, SENHA_USUARIO)
        cursor.execute(command, values)
        conn.commit()
        return {"message": "Usuário alterado com sucesso."}
    except Exception as e:
        return {"error": f"Erro ao alterar usuário: {e}"}
    finally:
        if cursor:
            cursor.fetchall()
            cursor.close()
        if conn:
            conn.close()

def listar_usuarios():
    config = DBModel.get_dotenv()
    db = MySqlConnector(config)
    conn, msg = db.connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.callproc("LISTAR_USUARIOS")
        
        usuarios = []
        for result in cursor.stored_results():
            usuarios.extend(result.fetchall())

        cursor.close()
        conn.close()
        return usuarios
    except Error as error:
        return []


def fazer_login(EMAIL_USUARIO, SENHA_USUARIO):
    config = DBModel.get_dotenv()
    db = MySqlConnector(config)
    conn, msg = db.connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("CALL FAZER_LOGIN(%s, %s)", (EMAIL_USUARIO, SENHA_USUARIO))
        result = cursor.fetchone()

        if result and result.get("MENSAGEM") == "Login realizado com sucesso!":
            return {
                "user": {
                    "id": result["ID_USUARIO"],
                    "email": result["EMAIL_USUARIO"]
                }
            }
        else:
            return None  # Login inválido

    except Exception as e:
        print(f"Erro ao fazer login: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if db:
            conn.close()

