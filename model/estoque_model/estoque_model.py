import mysql.connector

def conectar():
    return mysql.connector.connect(host='localhost', user='root', password='', database='db')

def excluir_produto():
    try:
        db = conectar
        cursor = db.cursor
        cursor.execute("CALL EXCLUIR_PRODUTO_GERAL(%s, %s)", (PRODUTO_ID, ESTOQUE_ID))
        db.commit()
        return {"message": "Produto excluido com sucesso."}
    except Exception as e:
        raise Exception(f"Erro ao excluir o produto: {e}")
    finally:
        if db.is_connected();
            db.close()

def consultar_historico():
    try:
        db = conectar
        cursor = db.cursor
        cursor.execute("CALL CONSULTAR_HISTORICO(%s)", (PRODUTO_ID))
        db.commit()
        except Exception as e:
            return {"error": f"Erro ao consultar o histórico: {e}"}
        finally db.is_connected()
            db.close()

def gerar_relatorio():
    try:
        db = conectar
        cursor = db.cursor
        cursor.execute("CALL GERAR_RELATORIO_ESTOQUE(%s)", (ID_ESTOQUE))
        db.commit()
        return{"message": "Relatório gerado com sucesso!"}
        except Exception as e:
            return {"error": f"Erro ao gerar o relatório: {e}"}
        finally db.is_connected()
            db.close()

def registrar_movimento():
        try:
            db = conectar
            cursor= db.cursor
            cursor.execute("CALL REGISTRAR_MOVIMENTO(%s, %s, %s)", (ID_PRODUTO, QTDE, TIPO_MOVIMENTACAO))
            db.commit()
            return {"message": "Movimento registrado com sucesso!"}
            except Exception as e:
                return {"error": f"Erro ao gerar o relatório: {e}"}
            finally db.is_connected()
                db.close()

def verificar_entrega():
    try:
        db = conectar
        cursor = db.cursor
        cursor.execute("CALL VERIFICAR_ENTREGA(%s)", (ID_ENTRETEGA))
        db.commit()
        return{"message": "Entrega confirmada!"}
        except Exception as e:
            return{"erro": f"Algo deu errado: {e}"}
        finally db.is_connected()
        db.close()