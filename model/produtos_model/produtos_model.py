from database.db_mysql import MySqlConnector
from database.db_model import DBModel
from mysql.connector import Error
from pydantic import BaseModel, ValidationError
from typing import Optional, Protocol
from model.produtos_model.modules_produtos_model.pdf_reader import read_pdf
from model.produtos_model.modules_produtos_model.email_data_extractor import read_email_data, baixar_anexos_pdf

def CADASTRAR_PRODUTO_ESTOQUE(NOME_PRODUTO, PRECO_PRODUTO, DESC_PRODUTO,
                              NUMERO_NF_PRODUTO, VALIDADE_PRODUTO, FORNECEDOR_PRODUTO,
                              QTD_MINIMA_PRODUTO, CATEGORIA_ESTOQUE, QTDE_ESTOQUE):
    config = DBModel.get_dotenv()
    db = MySqlConnector(config)
    conn, msg = db.connection()
    try:
        cursor = conn.cursor()
        command = "CALL CADASTRAR_PRODUTO_ESTOQUE(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (NOME_PRODUTO, PRECO_PRODUTO, DESC_PRODUTO,
                              NUMERO_NF_PRODUTO, VALIDADE_PRODUTO, FORNECEDOR_PRODUTO,
                              QTD_MINIMA_PRODUTO, CATEGORIA_ESTOQUE, QTDE_ESTOQUE)
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
        print(f"Erro ao listar produtos: {error}")
        return []
# print(LISTAR_PRODUTOS())

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


def ATUALIZAR_PRODUTO(
    #atualizar o estoque
    p_id_estoque_upd=None,p_categoria_estoque_upd=None,p_qtde_estoque_upd=None,     
    #parte para atualizar o produto
    p_id_produto_upd=None,       
    p_nome_produto_upd=None,     
    p_preco_produto_upd=None,    
    p_fk_id_estoque_upd=None,    
    p_desc_produto_upd=None,     
    p_numero_nf_produto_upd=None,
    p_validade_produto_upd=None,
    p_fornecedor_produto_upd=None,
    p_qtd_minima_produto_upd=None
):
    config = DBModel.get_dotenv()
    db = MySqlConnector(config)
    conn, msg = db.connection()
    if conn is None:
        print(f"Erro de conexão: {msg}")
        return False, f"Falha na conexão: {msg}"
    try:
        cursor = conn.cursor()
        command = "CALL ATUALIZAR_ESTOQUE_PRODUTO(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (
            p_id_estoque_upd,
            p_categoria_estoque_upd,
            p_qtde_estoque_upd,
            p_id_produto_upd,
            p_nome_produto_upd,
            p_preco_produto_upd,
            p_fk_id_estoque_upd,
            p_desc_produto_upd,
            p_numero_nf_produto_upd,
            p_validade_produto_upd,
            p_fornecedor_produto_upd,
            p_qtd_minima_produto_upd
        )
        cursor.execute(command, values)
        conn.commit()
        return True, 'sucesso'
    except Exception as e:
        print(f"Erro ao atualizar produto: {e}")
        return False, 'fracassado'

    finally:
        if cursor:
            try:
                cursor.fetchall()
            except Error as err:
                print(f"Erro ao tentar ler resultados do cursor (pode ser ignorado se não houver resultado): {err}")
            cursor.close()
        if conn:
            conn.close()


#area de teste
# sucesso, msg = ATUALIZAR_PRODUTO(
#     p_id_estoque_upd=2, # ID do estoque
#     # p_tipo_estoque_upd="Estoqe Principal Novo", 
#     p_tipo_estoque_upd="Estoque Principal Novo", 


#     p_qtde_estoque_upd=500 
# )
# # Todo os outros parâmetros de produto ficarão como None
# sucesso, msg = ATUALIZAR_PRODUTO(
#     p_id_produto_upd=2,# ID do produto que você quer atualizar
#     p_nome_produto_upd="Cadeira Gamer PRO",
#     p_preco_produto_upd=799.99,
#     p_desc_produto_upd="Cadeira ergonômica com ajuste total",
#     p_numero_nf_produto_upd="NF-CADEIRA-002"
# )
# print(f"Resultado atualização produto: {msg}")
# print(f"Resultado atualização estoque: {msg}")



def EXCLUIR_PRODUTO_GERAL(ID_ESTOQUE):
    config = DBModel.get_dotenv()
    db = MySqlConnector(config)
    conn, msg = db.connection()
    try:
        cursor = conn.cursor()
        command = "CALL EXCLUIR_ESTOQUE_PRODUTOS(%s)"
        values = (ID_ESTOQUE,)
        cursor.execute(command, values)
        conn.commit()
        print(f"ESTOQUE '{ID_ESTOQUE}' excluído com sucesso")
        return True, 'ESTOQUE excluído'
    
    except Exception as e:
        print(f"Erro ao remover ESTOQUE: {e}")
        return False, 'fracassado'
    finally:
        if cursor:
            cursor.close()
        if db:
            conn.close()



def coleta_de_dados_email():
    try:
        if read_email_data():
            emitente, nome_produto, tipo_produto, descricao_produto, qtde_produto, preco_produto_float, numero_nota = read_pdf()
            try:
                CADASTRAR_PRODUTO_ESTOQUE(nome_produto, preco_produto_float, descricao_produto, tipo_produto, qtde_produto, numero_nota )
            except Error as err:
                print(f'{err}')
        else:
            print('n')
    except:
        print("erro ao buscar no email")
        
