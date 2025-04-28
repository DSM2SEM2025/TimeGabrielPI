class db():
    def __init__(self, db_nome):
        self.db_nome = db_nome  
        self.data = []

    def conecta(self):
        print(f"Conectado com {self.db_name}")

    def desconecta(self):
        print(f"desconectado do {self.db_name}")

    def inserir(self, record):
        self.data.append(record)
        print(f"Inserido dado: {record}")

    def fetch_all(self):
        return self.data