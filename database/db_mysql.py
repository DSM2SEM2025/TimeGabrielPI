import os
from dotenv import load_dotenv
from mysql.connector import connect, Error

load_dotenv()

hostDB = 'localhost'
usernameDB = 'c##atividadeDB'
passwordDB = 'c##atividadeDB'
portDB = 3306
databaseDB = 'recriandoProcedures'

def mysql_conn():
    try:
        conn = connect(
            host = hostDB,
            username=usernameDB,
            password = passwordDB,
            port = portDB,
            database = databaseDB
        )
        return True, f'Sucesso ao conectar no banco', conn
    except Error as err:
        return False, f'Erro ao conectar no banco: {err}', conn
    
# validation, msg, conn = mysql_conn()
# if conn:
#     print(msg)
# else:
#     print(msg)

