
from mysql.connector import Error, connect
def conectar():
    print('teste')
    try:
        print('teste2')
        conn = connect(host='localhost', user='root', password='root',port = 3306, database='DEMO_DB')
        return conn, f'sucessp'
    except Error as err:
        return conn, f'erro {err}'
conn, msg =conectar()
if conn: 
    print(msg)
else:
    print(msg)
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
    cursor.close()
    db.close()

def CADASTRAR_PRODUTO_ESTOQUE(NOME_PRODUTO, PRECO_PRODUTO, DESC_PRODUTO, TIPO_PRODUTO, QTDE_ESTOQUE):
    try:
        db = conectar()
        cursor = db.cursor()
        command="CALL CADASTRAR_PRODUTO_ESTOQUE('%s', '%s', '%s', '%s', '%s')"
        values=(NOME_PRODUTO, PRECO_PRODUTO, DESC_PRODUTO, TIPO_PRODUTO, QTDE_ESTOQUE)
        cursor.execute(command, values)
        db.commit()
        return True, F'sucesso'
    except Exception as e:
        print(f"Erro ao inserir produto: {e}")
        return False, f'fracassado'
    finally:
        if db.is_connected():
            cursor.close()
            db.close()

# CADASTRAR_PRODUTO_ESTOQUE('uva', 10.50, 'Uva verde', 'uva', 100)
# conn, msg = CADASTRAR_PRODUTO_ESTOQUE('uva', 10.50, 'Uva verde', 'uva', 100)
# if conn:
#     print(msg)
# else:
#     print(msg)

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
            cursor.close()
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
            cursor.close()
            db.close()

def ATUALIZAR_PRODUTO(NOME_PRODUTO, PRECO_PRODUTO, DESC_PRODUTO, TIPO_ESTOQUE, QTDE_ESTOQUE, TIPO_ATUALIZACAO):
    try:
        db = conectar()
        cursor = db.cursor()
        command="CALL ATUALIZAR_PRODUTO('%s', '%s', '%s', '%s', '%s', '%s')"
        values=(NOME_PRODUTO, PRECO_PRODUTO, DESC_PRODUTO, TIPO_ESTOQUE, QTDE_ESTOQUE, TIPO_ATUALIZACAO)
        cursor.execute(command, values)
        db.commit()
        return {"message": "Produto atualizado com sucesso."}
    except Exception as e:
        return {"error": f"Erro ao atualizar usuário: {e}"}
    finally:
        if db.is_connected():
            cursor.close()
            db.close()

def EXCLUIR_PRODUTO_GERAL(NOME_PRODUTO):
    try:
        db = conectar()
        cursor = db.cursor()
        command="CALL EXCLUIR_PRODUTO_GERAL('%s')"
        values=(NOME_PRODUTO,)
        cursor.execute(command, values)
        db.commit()
        print(f"Produto '{NOME_PRODUTO}' excluído com sucesso")
    except Exception as e:
        print(f"Erro ao remover produto: {e}")
    finally:
        if db.is_connected():
            cursor.close()
            db.close()
