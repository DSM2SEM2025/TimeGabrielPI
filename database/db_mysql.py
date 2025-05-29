from .db_model import DataBaseConnector, DBModel
from typing import Optional
from mysql.connector import Error, connect, MySQLConnection



class MySqlConnector(DataBaseConnector):
    def __init__(self, db_config: DBModel):
        self.db_config = db_config
        self.conn = Optional[MySQLConnection] | None


    def connection(self):
        try:
            self.conn = connect(
                user = self.db_config.user,
                password = self.db_config.password,
                host = self.db_config.host,
                database = self.db_config.database,
                port = self.db_config.port,
            )
            return self.conn, f'Conexão com mysql bem-sucedida'
        except Error as err:
            print(f"Erro ao conectar ao MySQL: {err}")
            return None, f'Erro ao conectar {err}'      
    def disconnect(self):
        if self.conn and self.conn.is_connected():
            self.conn.close()
            return False, f'Conexão fechada com sucesso'