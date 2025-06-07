import os
import pdfplumber
import re
from model.produtos_model.modules_produtos_model.get_env_email import get_dotenv_email


def read_pdf():
    config_data, msg = get_dotenv_email()
    diretorio = config_data["local_annex"]
    files = os.listdir(config_data["local_annex"])
    print(config_data)
    print(diretorio, files)

    for file in files:
        text = ""
        try:
            with pdfplumber.open(diretorio+"/"+file) as pdf:
                for page in pdf.pages:
                    text+=page.extract_text()
                numero_nota= r'Número da Nota:\s*(.*?)\n'
                match_numero_nota=re.search(numero_nota, text)
                numero_nota = match_numero_nota.group(1).strip()

                emitente = r'Emitente:\s*(.*?)\n'
                match_emitente = re.search(emitente, text)
                emitente = match_emitente.group(1).strip()

                nome_produto = r'Nome do produto:\s*(.*?)\n'
                match_nome_produto = re.search(nome_produto, text)
                nome_produto = match_nome_produto.group(1).strip()
                tipo_produto = nome_produto

                descricao_produto = r'Descrição:\s*(.*?)\n'
                match_descricao_produto = re.search(descricao_produto, text)
                descricao_produto = match_descricao_produto.group(1)

                qtde_produto = r'Quantidade:\s*(.*?)\n'
                match_qtde = re.search(qtde_produto, text)
                qtde_produto = match_qtde.group(1).strip()

                
                preco_produto = r'Valor Unitário:\s*(.*?)\n'
                match_valor = re.search(preco_produto, text)
                preco_produto = match_valor.group(1).strip()
                string_preco_limpa = preco_produto.replace('R$', '').replace(',', '.').strip()
                preco_produto_float = float(string_preco_limpa)

        except pdfplumber.exceptions.PDFSyntaxError as e:
                    print(f"Erro de sintaxe no PDF '{file}': {e}. Este arquivo pode estar corrompido ou ter um formato inválido.")
        except Exception as e:
            print(f"Ocorreu um erro inesperado ao processar o arquivo '{file}': {e}")
        print("-" * 60) # Separador visual entre os arquivos processados
    return emitente, nome_produto, tipo_produto, descricao_produto, qtde_produto, preco_produto_float, numero_nota
    # print(emitente, nome_produto, tipo_produto, descricao_produto, qtde_produto, preco_produto_float, numero_nota)



                


