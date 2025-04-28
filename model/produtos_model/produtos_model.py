import mysql.connector

def conectar():
    return mysql.connector.connect(host='localhost', user='root', password='', database='db')

def criar_tabela():
    db = conectar()
    cursor = db.cursor()
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
    db.commit()
    db.close()

def CADASTRAR_PRODUTO_ESTOQUE(TIPO_ESTOQUE, NOME_PRODUTO, PRECO_PRODUTO, DESC_PRODUTO, QTD_ESTOQUE):
    try:
        db = conectar()
        cursor = db.cursor()
        command="CALL CADASTRAR_PRODUTO_ESTOQUE('%s', '%s', '%s', '%s', '%s')"
        values=(TIPO_ESTOQUE, NOME_PRODUTO, PRECO_PRODUTO, DESC_PRODUTO, QTD_ESTOQUE)
        cursor.execute(command, values)
        db.commit()
    except Exception as e:
        print(f"Erro ao inserir produto: {e}")
    finally:
        if db.is_connected():
            db.close()

def LISTAR_PRODUTOS():
    try:
        db = conectar()
        cursor = db.cursor()
        command="CALL LISTAR_PRODUTOS()"
        values=()
        cursor.execute(command, values)
        db.commit()
    except Exception as e:
        print(f"Erro ao listar produtos: {e}")
    finally:
        if db.is_connected():
            db.close()

def PROCURAR_PRODUTO_ID(ID_PRODUTO):
    try:
        db = conectar()
        cursor = db.cursor()
        command="CALL PROCURAR_PRODUTO_ID('%s')"
        values=(ID_PRODUTO,)
        cursor.execute(command, values)
        db.commit()
    except Exception as e:
        print(f"Erro ao procurar produto: {e}")
    finally:
        if db.is_connected():
            db.close()

def REMOVER_PRODUTO_ID(ID_PRODUTO):
    try:
        db = conectar()
        cursor = db.cursor()
        command="CALL REMOVER_PRODUTO_ID('%s')"
        values=(ID_PRODUTO,)
        cursor.execute(command, values)
        db.commit()
    except Exception as e:
        print(f"Erro ao remover produto: {e}")
    finally:
        if db.is_connected():
            db.close()
