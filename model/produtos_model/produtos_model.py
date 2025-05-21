from database.db_mysql import MySqlConnector
from database.db_model import DBModel
from mysql.connector import Error

def criar_tabela():
    config = DBModel.get_dotenv()
    db = MySqlConnector(config)
    conn, msg = db.connection()

    if conn:
        print(msg)
        try:
            cursor = conn.cursor()
            cursor.execute('''
            create table IF NOT EXISTS PRODUTO(
            ID_PRODUTO INT AUTO_INCREMENT PRIMARY key,
            NOME_PRODUTO VARCHAR(255) NOT NULL,
            PRECO_PRODUTO FLOAT NOT NULL,
            FK_ID_ESTOQUE_PRODUTO INT DEFAULT NULL,
            DESC_PRODUTO VARCHAR(255) NULL,
            FOREIGN KEY (FK_ID_ESTOQUE_PRODUTO) REFERENCES ESTOQUE(ID_ESTOQUE) ON DELETE SET NULL
            );     
            ''')
            conn.commit()
            cursor.close()
            conn.close()
        finally:
            db.disconect()

criar_tabela()

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

# CADASTRAR_PRODUTO_ESTOQUE('uva', 10.50, 'Uva verde', 'uva', 100)
# conn, msg = CADASTRAR_PRODUTO_ESTOQUE('uva', 10.50, 'Uva verde', 'uva', 100)
# if conn:
#     print(msg)
# else:
#     print(msg)

def LISTAR_PRODUTOS():
    config = DBModel.get_dotenv()
    db = MySqlConnector(config)
    conn, msg = db.connection()

    if not conn:
        print(msg)
        return False, 'conexão falhou'

    try:
        cursor = conn.cursor()
        command = "CALL LISTAR_PRODUTOS()"
        cursor.execute(command)
        resultados = cursor.fetchall()
        return True, resultados
    except Exception as e:
        print(f"Erro ao listar produtos: {e}")
        return False, 'fracassado'
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        db.disconect()

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
        print(f"Erro ao procurar produto: {e}")
        return False, 'fracassado'
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        db.disconect()

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
