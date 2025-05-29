from database.db_mysql import MySqlConnector
from database.db_model import DBModel
from mysql.connector import Error, connect



def CADASTRAR_PRODUTO_ESTOQUE(NOME_PRODUTO, PRECO_PRODUTO, DESC_PRODUTO, TIPO_PRODUTO, QTDE_ESTOQUE):
    config = DBModel.get_dotenv()
    db = MySqlConnector(config)
    conn, msg = db.connection()

    if not conn:
        print(msg)
        return False, 'conexão falhou'

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
        if conn:
            conn.close()
        db.disconect()


def LISTAR_PRODUTOS():
    config = DBModel.get_dotenv()
    db = MySqlConnector(config)
    conn, msg = db.connection()
    if not conn:
        print(msg)
        return False
    try:
        cursor = conn.cursor()
        cursor.callproc("listar_produtos")
        results = cursor.stored_results()
        for res in results:
            produtos = res.fetchall()
            return produtos

    except Error as err:
        return False, f'Erro ao buscar: {err}'
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()



def PROCURAR_PRODUTO_ID(ID_PRODUTO):
    config = DBModel.get_dotenv()
    db = MySqlConnector(config)
    conn, msg = db.connection()

    if not conn:
        print(msg)
        return False, 'conexão falhou'

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
        if conn:
            conn.close()
        db.disconect()

# res, msg = PROCURAR_PRODUTO_ID(1)

# if res:
#     print(msg)
# else:
#     print(msg)

def ATUALIZAR_PRODUTO(NOME_PRODUTO, PRECO_PRODUTO, DESC_PRODUTO, TIPO_ESTOQUE, QTDE_ESTOQUE, TIPO_ATUALIZACAO):
    config = DBModel.get_dotenv()
    db = MySqlConnector(config)
    conn, msg = db.connection()

    if not conn:
        print(msg)
        return False, 'conexão falhou'

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
            cursor.close()
        if conn:
            conn.close()
        db.disconect()

def EXCLUIR_PRODUTO_GERAL(NOME_PRODUTO):
    config = DBModel.get_dotenv()
    db = MySqlConnector(config)
    conn, msg = db.connection()

    if not conn:
        print(msg)
        return False, 'conexão falhou'

    try:
        cursor = conn.cursor()
        command = "CALL EXCLUIR_PRODUTO_GERAL(%s)"
        values = (NOME_PRODUTO,)
        cursor.execute(command, values)
        conn.commit()
        print(f"Produto '{NOME_PRODUTO}' excluído com sucesso")
        return True, 'produto excluído'
    
    except Exception as e:
        print(f"Erro ao remover produto: {e}")
        return False, 'fracassado'
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        db.disconect()
