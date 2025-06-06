from database.db_mysql import MySqlConnector
from database.db_model import DBModel
from mysql.connector import Error
from pydantic import BaseModel, ValidationError
from typing import Optional, Protocol

def CADASTRAR_PRODUTO_ESTOQUE(NOME_PRODUTO, PRECO_PRODUTO, DESC_PRODUTO, TIPO_PRODUTO, QTDE_ESTOQUE):
    config = DBModel.get_dotenv()
    db = MySqlConnector(config)
    conn, msg = db.connection()
    try:
        cursor = conn.cursor()
        command = "CALL CADASTRAR_PRODUTO_ESTOQUE(%s, %s, %s, %s, %s)"
        values = (NOME_PRODUTO, PRECO_PRODUTO, DESC_PRODUTO, TIPO_PRODUTO, QTDE_ESTOQUE)
        cursor.execute(command, values)
        conn.commit()
        return True, 'sucesso'
    except Exception as e:
        print(f"Erro ao inserir produto: {e}")
        return False, 'fracassado'
    finally:
        if cursor:
            cursor.close()
        if db:
            conn.close()


def LISTAR_PRODUTOS():
    config = DBModel.get_dotenv()
    db = MySqlConnector(config)
    conn, msg = db.connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.callproc("LISTAR_PRODUTOS")   
        produtos = []
        for result in cursor.stored_results():
            produtos.extend(result.fetchall())

        cursor.close()
        conn.close()
        return produtos
    except Error as error:
        return []


def PROCURAR_PRODUTO_ID(ID_PRODUTO):
    config = DBModel.get_dotenv()
    db = MySqlConnector(config)
    conn, msg = db.connection()
    try:
        cursor = conn.cursor()
        command = "CALL PROCURAR_PRODUTO_ID(%s)"
        values = (ID_PRODUTO,)
        cursor.execute(command, values)
        resultados = cursor.fetchall()
        return True, resultados
    except Exception as e:
        return False, f"Erro ao procurar produto: {e}"
    finally:
        if cursor:
            cursor.close()
        if db:
            conn.close()


def ATUALIZAR_PRODUTO(NOME_PRODUTO, PRECO_PRODUTO, DESC_PRODUTO, TIPO_ESTOQUE, QTDE_ESTOQUE, TIPO_ATUALIZACAO):
    config = DBModel.get_dotenv()
    db = MySqlConnector(config)
    conn, msg = db.connection()
    try:
        cursor = conn.cursor()
        command = "CALL ATUALIZAR_PRODUTO(%s, %s, %s, %s, %s, %s)"
        values = (NOME_PRODUTO, PRECO_PRODUTO, DESC_PRODUTO, TIPO_ESTOQUE, QTDE_ESTOQUE, TIPO_ATUALIZACAO)
        cursor.execute(command, values)
        conn.commit()
        return True, 'sucesso'
    except Exception as e:
        print(f"Erro ao atualizar produto: {e}")
        return False, 'fracassado'

    finally:
        if cursor:
            cursor.fetchall()
            cursor.close()
        if conn:
            conn.close()

print(ATUALIZAR_PRODUTO('maça', 1000, 'UPDATE_TESTE', 'maça', 2000, 2))


def EXCLUIR_PRODUTO_GERAL(ID_PRODUTO):
    config = DBModel.get_dotenv()
    db = MySqlConnector(config)
    conn, msg = db.connection()
    try:
        cursor = conn.cursor()
        command = "CALL EXCLUIR_PRODUTO_GERAL(%s)"
        values = (ID_PRODUTO,)
        cursor.execute(command, values)
        conn.commit()
        print(f"Produto '{ID_PRODUTO}' excluído com sucesso")
        return True, 'produto excluído'
    
    except Exception as e:
        print(f"Erro ao remover produto: {e}")
        return False, 'fracassado'
    
    finally:
        if cursor:
            cursor.close()
        if db:
            conn.close()



def coleta_de_dados_pdf():
    return



