from database.db_mysql import MySqlConnector
from database.db_model import DBModel

# def conectar():
#     print('teste')
#     try:
#         print('teste2')
#         conn = connect(host='localhost', user='root', password='root',port = 3306, database='DEMO_DB')
#         return conn, f'sucessp'
#     except Error as err:
#         return conn, f'erro {err}'
# conn, msg =conectar()
# if conn: 
#     print(msg)
# else:
#     print(msg)

def main():
    config = DBModel.get_dotenv()
    db = MySqlConnector(config)
    conn, msg = db.connection()

    if conn:
        print(msg)
        try:
            cursor = conn.cursor()
            querry= "CALL CADASTRAR_PRODUTO_ESTOQUE(%s, %s, %s, %s, %s)"
            data = ('maça', 22.50, 'MAÇA MUITO SUCULENTA', 'maça', 400)
            cursor.execute(querry, data)
            conn.commit()
            cursor.close()
            db.disconnect()
        finally:
            db.disconect()

if __name__ == "__main__":
    main()


# def criar_tabela():
#     config = DBModel.get_dotenv()
#     db = MySqlConnector(config)
#     conn, msg = db.connection()

#     if conn:
#         print(msg)
#         try:
#             cursor = conn.cursor()
#             cursor.execute('''
#             create table IF NOT EXISTS PRODUTO(
#             ID_PRODUTO INT AUTO_INCREMENT PRIMARY key,
#             NOME_PRODUTO VARCHAR(255) NOT NULL,
#             PRECO_PRODUTO FLOAT NOT NULL,
#             FK_ID_ESTOQUE_PRODUTO INT DEFAULT NULL,
#             DESC_PRODUTO VARCHAR(255) NULL,
#             FOREIGN KEY (FK_ID_ESTOQUE_PRODUTO) REFERENCES ESTOQUE(ID_ESTOQUE) ON DELETE SET NULL
#             );     
#             ''')
#             conn.commit()
#             cursor.close()
#             conn.close()
#         finally:
#             db.disconect()

# criar_tabela()
# CADASTRAR_PRODUTO_ESTOQUE('uva', 10.50, 'Uva verde', 'uva', 100)
# conn, msg = CADASTRAR_PRODUTO_ESTOQUE('uva', 10.50, 'Uva verde', 'uva', 100)
# if conn:
#     print(msg)
# else:
#     print(msg)