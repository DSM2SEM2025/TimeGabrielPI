from database.db_mysql import MySqlConnector  # Ferramenta que realmente faz a conexão com o MySQL.
from database.db_model import DBModel # Modelo que guarda as informações de conexão do banco.
from mysql.connector import Error # Para pegar e lidar com erros do MySQL.
# from pydantic import BaseModel, ValidationError
from typing import Optional, Protocol  # Para indicar que um valor pode ser opcional ou definir "contratos" (interfaces).

# Importa funções para ler PDFs e e-mails (extrair dados de notas fiscais).
from model.produtos_model.modules_produtos_model.pdf_reader import read_pdf
from model.produtos_model.modules_produtos_model.email_data_extractor import read_email_data, baixar_anexos_pdf
from model.produtos_model.modules_produtos_model.pdf_reader import read_pdf, formatar_validade_para_mysql


def CADASTRAR_PRODUTO_ESTOQUE(
    NOME_PRODUTO, 
    CATEGORIA_ESTOQUE, 
    DESC_PRODUTO, 
    QTDE_ESTOQUE, 
    PRECO_PRODUTO,
    QTD_MINIMA_PRODUTO, 
    VALIDADE_PRODUTO, 
    NUMERO_NF_PRODUTO, 
    FORNECEDOR_PRODUTO
    ):
    """
    Cadastra um novo produto no estoque do banco de dados.
    Ele usa um procedimento armazenado no MySQL para fazer o registro.
    Parâmetros:
    Todos os parâmetros são as informações detalhadas do produto (nome, categoria, descrição, quantidade, preço, etc.).
    """
    try:
        qtde_estoque_int = int(QTDE_ESTOQUE) # Tenta converter a quantidade para número.
    except ValueError:
        print(f"Valor inválido para QTDE_ESTOQUE: {QTDE_ESTOQUE}")
        return False, 'QTDE_ESTOQUE inválido'    
    
    """
    Pega as configurações do banco de um arquivo .env 
    Usando o método "get.dotenv" da classe localizada no arquivo "db_model" da pasta "database/db_model.py".
    """
    config = DBModel.get_dotenv() 
    db = MySqlConnector(config) # Cria um objeto para conectar ao MySQL.
    conn, msg = db.connection()  # Tenta fazer a conexão.
    try:
        cursor = conn.cursor()  # Prepara o "cursor" para enviar comandos SQL.

        # Chama um "procedimento de inserção"(procedure) no banco para cadastrar o produto.
        command = "CALL CADASTRAR_PRODUTO_ESTOQUE(%s, %s, %s, %s, %s, %s, %s, %s, %s)"

        #valores a serem aplicados nos locais "%s" ao chamar a procedure
        values = (NOME_PRODUTO, CATEGORIA_ESTOQUE, DESC_PRODUTO, QTDE_ESTOQUE, 
                              PRECO_PRODUTO, QTD_MINIMA_PRODUTO, VALIDADE_PRODUTO, NUMERO_NF_PRODUTO, 
                              FORNECEDOR_PRODUTO)
        print("Valores enviados para procedure:", values)
        cursor.execute(command, values) # Executa o comando.
        
        from model.produtos_model.produtos_model import inserir_atividade
        inserir_atividade(
            tipo="Adição",
            descricao=f"Produto '{NOME_PRODUTO}' cadastrado no estoque.",
            quantidade=QTDE_ESTOQUE
        )
        
        conn.commit() # Salva as mudanças no banco.
        return True, 'sucesso' # Retorna True e um menssagem de sucesso.
    except Exception as e:
        #Caso houver algum erro durante o cadastro
        print(f"Erro ao inserir produto: {e}")
        return False, 'fracassado'#devolve False e uma menssagem de fracasso
    finally:
        # Garante que o cursor e a conexão sejam fechados no final, evitando vazamentos.
        if cursor:
            cursor.close()
        if db:
            conn.close()


def LISTAR_PRODUTOS():
    """
    Busca e retorna a lista de todos os produtos cadastrados no banco de dados.
    """
    config = DBModel.get_dotenv() # Pega as configurações do banco
    db = MySqlConnector(config) # Cria o conector MySQL.
    conn, msg = db.connection() # Conecta ao banco.
    try:
        cursor = conn.cursor(dictionary=True) # Prepara o cursor para retornar resultados como dicionários.
        cursor.callproc("LISTAR_PRODUTOS") # Chama a procedure que lista os produtos.
        produtos = []
        for result in cursor.stored_results(): # Pega os resultados do procedimento.
            produtos.extend(result.fetchall()) # Adiciona todos os produtos encontrados à lista

        cursor.close() # Fecha o cursor.
        conn.close() # Fecha a conexão.
        return produtos # Retorna a lista de produtos.
    except Error as error:
        print(f"Erro ao listar produtos: {error}")
        return [] # Retorna uma lista vazia se houver erro.

def PROCURAR_PRODUTO_NOME(NOME_PRODUTO):
    """
    Procura produtos no banco de dados pelo nome.
    """
    config = DBModel.get_dotenv() # Pega as configurações do banco
    db = MySqlConnector(config) # Cria o conector MySQL.
    conn, msg = db.connection() # Conecta ao banco.
    try:
        cursor = conn.cursor()
        # Chama o procedure para procurar produto por nome.
        command = "CALL PROCURAR_PRODUTO_NOME(%s)"
        values = (NOME_PRODUTO,)
        cursor.execute(command, values)
        resultados = cursor.fetchall()
        return True, resultados # Retorna sucesso e os resultados
    except Exception as e:
        return False, f"Erro ao procurar produto por nome: {e}"
    finally: 
        if cursor:
            cursor.close()
        if db:
            conn.close()



def ATUALIZAR_PRODUTO(
    p_id_estoque_upd=None, p_categoria_estoque_upd=None, p_qtde_estoque_upd=None,     
    p_id_produto_upd=None, p_nome_produto_upd=None, p_preco_produto_upd=None,    
    p_desc_produto_upd=None, p_numero_nf_produto_upd=None,
    p_validade_produto_upd=None, p_fornecedor_produto_upd=None,
    p_qtd_minima_produto_upd=None
):
    """
    Atualiza as informações de um produto ou de seu estoque no banco de dados.
    Você passa apenas os campos que quer atualizar.
    """
    config = DBModel.get_dotenv() # Pega as configurações do banco
    db = MySqlConnector(config) # Cria o conector MySQL.
    conn, msg = db.connection() # Conecta ao banco.
    if conn is None:
        print(f"Erro de conexão: {msg}")
        return False, f"Falha na conexão: {msg}"
    try:
        cursor = conn.cursor()
        # Chama a procedure para atualizar produto/estoque.
        command = "CALL ATUALIZAR_ESTOQUE_PRODUTO(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        # Todos os parâmetros para a procedure (muitos podem ser None se não forem atualizados).
        values = (
            p_id_estoque_upd,
            p_categoria_estoque_upd,
            p_qtde_estoque_upd,
            p_id_produto_upd,
            p_nome_produto_upd,
            p_preco_produto_upd,
            p_desc_produto_upd,
            p_numero_nf_produto_upd,
            p_validade_produto_upd,
            p_fornecedor_produto_upd,
            p_qtd_minima_produto_upd
        )
        cursor.execute(command, values)
        conn.commit()
        
        from model.produtos_model.produtos_model import inserir_atividade
        inserir_atividade(
            tipo="Atualização",
            descricao=f"Produto '{p_nome_produto_upd}' atualizado no estoque.",
            quantidade=p_qtde_estoque_upd if p_qtde_estoque_upd is not None else 0
        )
        
        return True, 'sucesso' #retorna True(Verdadeiro) se tiver sucesso ao aplicar atualização
    except Exception as e:
        print(f"Erro ao atualizar produto: {e}")
        return False, 'fracassado'
    finally:
        # Garante que o cursor e a conexão sejam fechados.
        if cursor:
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
    """
    Exclui um registro de estoque e os produtos relacionados a ele no banco de dados.
    """
    config = DBModel.get_dotenv() # Pega as configurações do banco
    db = MySqlConnector(config) # Cria o conector MySQL.
    conn, msg = db.connection() # Conecta ao banco.
    try:
        cursor = conn.cursor()
        # Chama a procedure para excluir estoque e produtos.
        command = "CALL EXCLUIR_ESTOQUE_PRODUTOS(%s)"
        values = (ID_ESTOQUE,)
        cursor.execute(command, values)
        conn.commit()
        print(f"ESTOQUE '{ID_ESTOQUE}' excluído com sucesso")
        return True, 'ESTOQUE excluído' #retorna True(Verdadeiro) se tiver sucesso ao aplicar o processo de exclusão
    except Exception as e:
        print(f"Erro ao remover ESTOQUE: {e}")
        return False, str(e)
    finally:
        # Garante que o cursor e a conexão sejam fechados.
        if cursor:
            cursor.close()
        if conn:
            conn.close()



def coleta_de_dados_email():
    """
    Tenta ler dados de e-mails e anexos PDF (notas fiscais)
    e, se conseguir, cadastra as informações do produto no estoque.
    """
    try:
        res=read_email_data()
        return True, res 
    except:
        print("Erro no processo de coleta de dados do email")
        return False


def data_pdf_extractor():
    processed_count = 0 #Contador para produtos cadastrados com sucesso
    failed_count = 0   #Contador para produtos que falharam no cadastro

    try:
        # Chama read_pdf do arquivo pdf_reader.py
        # E espera que ela retorne uma lista de dicionários.
        all_products_data = read_pdf()

        if all_products_data:
            print(f"\n{len(all_products_data)} PDF(s) processado(s) e dados extraídos com sucesso!")
            
            #Loop para iterar sobre cada dicionário de dados extraídos
            for produto_data in all_products_data:
                print(f"\nTentando cadastrar produto do PDF: {produto_data.get('nome_arquivo_pdf', 'N/A')}")
                
                #Formata a validade para o formato MySQL antes de passar
                validade_para_mysql = formatar_validade_para_mysql(produto_data.get('validade_produto'))

                # Chama a função de cadastro no banco de dados
                # Mapeando os campos do dicionário para os parâmetros da função CADASTRAR_PRODUTO_ESTOQUE
                success, message = CADASTRAR_PRODUTO_ESTOQUE(
                    NOME_PRODUTO=produto_data.get('nome_produto'),
                    CATEGORIA_ESTOQUE=produto_data.get('categoria'),
                    DESC_PRODUTO=produto_data.get('descricao_produto'),
                    QTDE_ESTOQUE=produto_data.get('qtde_produto'),
                    PRECO_PRODUTO=produto_data.get('preco_produto_float'),
                    QTD_MINIMA_PRODUTO=produto_data.get('qtd_minima_produto'),
                    VALIDADE_PRODUTO=validade_para_mysql,
                    NUMERO_NF_PRODUTO=produto_data.get('numero_nota_fiscal'),
                    FORNECEDOR_PRODUTO=produto_data.get('emitente') 
                )

                if success:
                    print(f"Produto '{produto_data.get('nome_produto')}' do PDF '{produto_data.get('nome_arquivo_pdf')}' cadastrado com sucesso! Mensagem: {message}")
                    processed_count += 1
                else:
                    print(f"Falha ao cadastrar produto '{produto_data.get('nome_produto')}' do PDF '{produto_data.get('nome_arquivo_pdf')}'. Mensagem: {message}")
                    failed_count += 1
                print("-" * 50) # Separador para cada produto

            print(f"\n--- Resumo do Cadastro ---")
            print(f"Total de PDFs processados: {len(all_products_data)}")
            print(f"Produtos cadastrados com sucesso: {processed_count}")
            print(f"Produtos com falha no cadastro: {failed_count}")

            # Retorna a LISTA COMPLETA de dicionários, salva tempo
            return all_products_data
        else:
            print(f'Nenhum dado de produto encontrado nos PDFs disponíveis ou diretório vazio. Nenhum cadastro realizado.')
            return [] # Retorna uma lista vazia se nada for encontrado

    except Exception as e:
        print(f'Erro geral na execução de data_pdf_extractor: {e}')
        return [] # Retorna uma lista vazia em caso de erro

# print(data_pdf_extractor())

"""
CADASTRAR_PRODUTO_ESTOQUE(
    NOME_PRODUTO, 
    CATEGORIA_ESTOQUE, 
    DESC_PRODUTO, 
    QTDE_ESTOQUE, 
    PRECO_PRODUTO,
    QTD_MINIMA_PRODUTO, 
    VALIDADE_PRODUTO, 
    NUMERO_NF_PRODUTO, 
    FORNECEDOR_PRODUTO
    ):

    command = "CALL CADASTRAR_PRODUTO_ESTOQUE(%s, %s, %s, %s, %s, %s, %s, %s, %s)"

        #valores a serem aplicados nos locais "%s" ao chamar a procedure
        values = (NOME_PRODUTO, CATEGORIA_ESTOQUE, DESC_PRODUTO, QTDE_ESTOQUE, 
                              PRECO_PRODUTO, QTD_MINIMA_PRODUTO, VALIDADE_PRODUTO, NUMERO_NF_PRODUTO, 
                              FORNECEDOR_PRODUTO)
"""
        


def diminuir_estoque(produto_id: int, quantidade: int):
    """
    Diminui a quantidade de um produto específico no estoque e registra a movimentação.
    """
    config = DBModel.get_dotenv()  # Pega as configurações do banco
    db = MySqlConnector(config)    # Cria o conector MySQL.
    conn, msg = db.connection()   # Conecta ao banco.
    
    try:
        cursor = conn.cursor()

        # Atualiza o estoque
        command = """
            UPDATE ESTOQUE 
            SET QTDE_ESTOQUE = QTDE_ESTOQUE - %s 
            WHERE ID_ESTOQUE = (
                SELECT FK_ID_ESTOQUE FROM PRODUTOS WHERE ID_PRODUTO = %s
            )
        """
        cursor.execute(command, (quantidade, produto_id))
        
        # Registra a movimentação do tipo 'SAIDA'
        insert_mov = """
            INSERT INTO MOVIMENTACAO (FK_ID_PRODUTO, QTDE, TIPO_MOVIMENTACAO, DATA_MOVIMENTACAO)
            VALUES (%s, %s, %s, CURDATE())
        """
        cursor.execute(insert_mov, (produto_id, quantidade, "SAIDA"))

        conn.commit()  # Confirma tudo

        return True, "Estoque atualizado e movimentação registrada."

    except Exception as e:
        return False, f"Erro ao atualizar estoque: {e}"

    finally:
        cursor.close()
        conn.close()


def CONTAR_TOTAL_PRODUTOS():
    config = DBModel.get_dotenv()
    db = MySqlConnector(config)
    conn, msg = db.connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM PRODUTOS")
        resultado = cursor.fetchone()
        return True, resultado[0]
    except Exception as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()


def CONTAR_PRODUTOS_BAIXO_ESTOQUE():
    config = DBModel.get_dotenv()
    db = MySqlConnector(config)
    conn, msg = db.connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) 
            FROM ESTOQUE E
            JOIN PRODUTOS P ON E.ID_ESTOQUE = P.ID_PRODUTO
            WHERE E.QTDE_ESTOQUE < P.QTD_MINIMA_PRODUTO
        """)
        resultado = cursor.fetchone()
        return True, resultado[0]
    except Exception as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

def CONTAR_SAIDAS_PRODUTOS():
    config = DBModel.get_dotenv()
    db = MySqlConnector(config)
    conn, msg = db.connection()
    
    if not conn:
        return False, f"Erro na conexão: {msg}"
    
    try:
        cursor = conn.cursor()
        
        # Query para somar a quantidade total das saídas
        query = """
            SELECT COALESCE(SUM(QTDE), 0) FROM MOVIMENTACAO
            WHERE TIPO_MOVIMENTACAO = 'Saída'
        """
        
        cursor.execute(query)
        resultado = cursor.fetchone()
        total_saida = resultado[0] if resultado else 0
        
        return True, total_saida
    
    except Exception as e:
        return False, f"Erro ao contar saídas: {e}"
    
    finally:
        cursor.close()
        conn.close()

def inserir_atividade(tipo, descricao, quantidade):
    """
    Insere uma nova atividade no banco de dados.
    """
    config = DBModel.get_dotenv()
    db = MySqlConnector(config)
    conn, msg = db.connection()
    
    if not conn:
        return False, f"Erro na conexão: {msg}"
    
    try:
        cursor = conn.cursor()
        verificar_na_tabela = "select 1 from ATIVIDADES where tipo = %s and descricao = %s and quantidade = %s"
        values=(tipo, descricao, quantidade)
        cursor.execute(verificar_na_tabela, values)
        res = cursor.fetchone()
        #fetchone
        #fetchall
        if res:
            return False, 'Atividade já inserida'
        else:
            command = "INSERT INTO ATIVIDADES (TIPO, DESCRICAO, QUANTIDADE) VALUES (%s, %s, %s)"
            values = (tipo, descricao, quantidade)
            cursor.execute(command, values)
            conn.commit()
            return True, "Atividade inserida com sucesso"
    
    except Exception as e:
        return False, f"Erro ao inserir atividade: {e}"
    
    finally:
        cursor.close()
        conn.close()
print(inserir_atividade('adição',"Produto 'Queijo Minas Frescal' cadastrado no estoque.",3))   


def buscar_atividades_recentes(limit=100):
    """
    Busca as atividades mais recentes do banco de dados.
    """
    config = DBModel.get_dotenv()
    db = MySqlConnector(config)
    conn, msg = db.connection()
    
    if not conn:
        return False, f"Erro na conexão: {msg}"
    
    try:
        cursor = conn.cursor(dictionary=True)
        command = """
            SELECT id, tipo, descricao, quantidade AS value, 
                DATE_FORMAT(data_hora, '%Y-%m-%d %H:%i:%s') AS time 
            FROM atividades 
            ORDER BY data_hora DESC 
            LIMIT 100
        """
        cursor.execute(command)

        atividades = cursor.fetchall()
        return True, atividades
    
    except Exception as e:
        return False, f"Erro ao buscar atividades: {e}"
    
    finally:
        cursor.close()
        conn.close()

        conn.close()