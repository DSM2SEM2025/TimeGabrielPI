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

