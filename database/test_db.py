from db_mysql import MySqlConnector
from db_model import DBModel
from mysql.connector import Error

def main():
    config = DBModel.get_dotenv()
    db = MySqlConnector(config)
    conn, msg = db.connection()

    if conn:
        print(msg)
        try:
            cursor = conn.cursor()

            query = "CALL CADASTRAR_PRODUTO_ESTOQUE(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            data = (
                'maçã',                # P_NOME_PRODUTO
                22.50,                 # P_PRECO_PRODUTO
                'Maçã muito suculenta',# P_DESC_PRODUTO
                'NF-001122',           # P_NUMERO_NF_PRODUTO
                '2025-12-31',          # P_VALIDADE_PRODUTO
                'Fornecedor X',        # P_FORNECEDOR_PRODUTO
                10,                    # P_QTD_MINIMA_PRODUTO
                'Alimentos',           # P_CATEGORIA_ESTOQUE (ENUM válido)
                400                    # P_QTDE_ESTOQUE
            )

            cursor.execute(query, data)
            conn.commit()
            cursor.close()

        except Error as e:
            print("Erro ao executar procedure:", e)

        finally:
            db.disconnect()
