import os
import pdfplumber
import re
import shutil
from model.produtos_model.modules_produtos_model.get_env_email import get_dotenv_email
from datetime import datetime, date


def formatar_validade_para_mysql(validade_data):#facilita na hora de colocar no bando :)
    """
    Converte um valor de validade (string ou date) para o formato 'YYYY-MM-DD'
    esperado pelo MySQL ou retorna None se não for uma data válida/aplicável.
    """
    if isinstance(validade_data, date):
        return validade_data.strftime("%Y-%m-%d")
    elif isinstance(validade_data, str):
        try: 
            return datetime.strptime(validade_data, "%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            pass
        try: 
            return datetime.strptime(validade_data, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            pass
        if validade_data.lower() in ["indeterminada", "não aplicável", "não se aplica", "n/a", "na"]:
            return None
    return None

def extrair_dados_do_texto_pdf(text):
    #coisa chata do regex... mds, solicitei para o chat gpt fazer pra mim o rgx. 
    #Desculpe professor, não tive coragem de fazer essa parte, teria que ter estudado mais tempo
    #Assinado. Jhon Deyvid Quispe Mamani. Desertor do processo de aprendizado do rgx
    dados_extraidos = {} # Dicionário para armazenar os dados de um único PDF
    
    numero_nota = r'Número da Nota:\s*(.*?)(?:\n|\r|$)'
    match_numero_nota = re.search(numero_nota, text, re.IGNORECASE) # Adicionado IGNORECASE
    dados_extraidos['numero_nota_fiscal'] = match_numero_nota.group(1).strip() if match_numero_nota else None

    emitente_regex = r'(?:Emitente|Fornecedor):\s*(.*?)(?:\n|\r|$)'
    match_emitente = re.search(emitente_regex, text, re.IGNORECASE)
    dados_extraidos['emitente'] = match_emitente.group(1).strip() if match_emitente else None

    nome_produto_regex = r'(?:Nome do produto|Produto):\s*(.*?)(?:\n|\r|$)'
    match_nome_produto = re.search(nome_produto_regex, text, re.IGNORECASE)
    dados_extraidos['nome_produto'] = match_nome_produto.group(1).strip() if match_nome_produto else None

    descricao_produto_regex = r'Descrição:\s*(.*?)(?:\n|\r|$)'
    match_descricao_produto = re.search(descricao_produto_regex, text, re.IGNORECASE)
    dados_extraidos['descricao_produto'] = match_descricao_produto.group(1).strip() if match_descricao_produto else None

    qtde_produto_regex = r'Quantidade:\s*(\d+)(?:\n|\r|$)'
    match_qtde = re.search(qtde_produto_regex, text, re.IGNORECASE)
    dados_extraidos['qtde_produto'] = int(match_qtde.group(1).strip()) if match_qtde and match_qtde.group(1).strip().isdigit() else None

    preco_produto_regex = r'(?:Valor Unitário|Preço):\s*(?:R\$|\$)?\s*([\d\.,]+)(?:\n|\r|$)'
    match_valor = re.search(preco_produto_regex, text, re.IGNORECASE)
    if match_valor:
        string_preco_limpa = match_valor.group(1).replace('R$', '').replace('.', '').replace(',', '.').strip()
        try:
            dados_extraidos['preco_produto_float'] = float(string_preco_limpa)
        except ValueError:
            dados_extraidos['preco_produto_float'] = None
    else:
        dados_extraidos['preco_produto_float'] = None


    categoria_regex = r'Categoria:\s*(.*?)(?:\n|\r|$)'
    match_categoria = re.search(categoria_regex, text)
    dados_extraidos['categoria'] = match_categoria.group(1).strip() if match_categoria else None

    qtd_minima_regex = r'Quantidade Mínima:\s*(\d+)(?:\n|\r|$)'
    match_qtd_minima = re.search(qtd_minima_regex, text, re.IGNORECASE)
    dados_extraidos['qtd_minima_produto'] = int(match_qtd_minima.group(1).strip()) if match_qtd_minima and match_qtd_minima.group(1).strip().isdigit() else None

    validade_regex = r'Validade:\s*(\d{2}\/\d{2}\/\d{4}|Indeterminada|Não se aplica|N\/A|NA)(?:\n|\r|$)'
    match_validade = re.search(validade_regex, text, re.IGNORECASE)
    dados_extraidos['validade_produto'] = match_validade.group(1).strip() if match_validade else None

    return dados_extraidos

def read_pdf(): 
    #forma de obter config_data e msg do arquvio .env por meio da função "get_dotenv_email" criada no arquivo get_env_email
    config_data, msg = get_dotenv_email()
    diretorio = config_data["local_annex"]

    #Verifica se o diretório existe antes de tentar listar
    if not os.path.exists(diretorio):
        print(f"Diretório de anexos '{diretorio}' não encontrado.")
        return [] # Retorna uma lista vazia se o diretório não existir

    files = os.listdir(diretorio) #forma de listar arquivos

    diretorio_lidos = os.path.join(diretorio, "lidos")

    #lógica de criação de diretório
    if not os.path.exists(diretorio_lidos):
        os.makedirs(diretorio_lidos)
        print(f"Pasta '{diretorio_lidos}' criada com sucesso.")
    else:
        print(f"Pasta '{diretorio_lidos}' já existe.")

    #Lista para armazenar os dados de CADA PDF processado
    all_pdfs_data = []

    if files:
        for file in files:
            if not file.lower().endswith('.pdf'):
                print(f"Ignorando arquivo '{file}': não é um PDF.")
                continue

            text = ""
            file_path = os.path.join(diretorio, file)

            try:
                #forma de abrir o PDF com pdfplumber
                with pdfplumber.open(file_path) as pdf: 
                    for page in pdf.pages:
                        #Adicionado 'or ""' para evitar None em texto de página vazia
                        text += page.extract_text() or ""

                    #Chama a função auxiliar para extrair os dados do texto
                    extracted_data_for_current_pdf = extrair_dados_do_texto_pdf(text)

                    #Adiciona o nome do arquivo aos dados extraídos (útil para rastreamento)
                    extracted_data_for_current_pdf['nome_arquivo_pdf'] = file

                    #Adiciona os dados do PDF atual à lista de todos os PDFs
                    all_pdfs_data.append(extracted_data_for_current_pdf)


                #lógica de mover arquivos após a leitura
                #                                       |
                #                                       v
                #descomentar a movimentação de pdfs entre "lidos" e "não lidos"
                # destino_path = os.path.join(diretorio_lidos, file)
                # shutil.move(file_path, destino_path)
                # print(f"Arquivo '{file}' movido para '{diretorio_lidos}'.")


                #pdfPlumber salvando novamente XD
            except pdfplumber.exceptions.PDFSyntaxError as e:
                print(f"Erro de sintaxe no PDF '{file}': {e}. Este arquivo pode estar corrompido ou ter um formato inválido.")
            except Exception as e:
                #Mensagem de erro PARA caso haja algum erro no processamento do arquivo, retirada de dados
                print(f"Ocorreu um erro ao processar o arquivo '{file}': {e}")
                #Pode ser útil logar o erro e continuar para o próximo arquivo
            print("-" * 60) # Separador visual

        #Retorna a LISTA COMPLETA de dicionários (dados de todos os PDFs)
        return all_pdfs_data
    else:
        #Retorna uma lista vazia em vez de uma string
        print("Nenhum arquivo PDF encontrado no diretório para leitura.")
        return []

# print(read_pdf())
    





                


