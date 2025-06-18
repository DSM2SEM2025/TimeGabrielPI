import imaplib # Módulo para interagir com servidores IMAP (Internet Message Access Protocol)
import ssl # Módulo para operações de socket seguras (SSL/TLS)
import email  # Módulo para analisar e manipular mensagens de e-mail
import os # Módulo para interagir com o sistema operacional 
from email.header import decode_header # Função para decodificar cabeçalhos de e-mail
import re # Módulo para expressões regulares, usado para buscar padrões em strings
from dotenv import load_dotenv # Função para carregar variáveis de ambiente de um arquivo .env
from model.produtos_model.modules_produtos_model.get_env_email import get_dotenv_email # Função para obter configurações de e-mail



def baixar_anexos_pdf(msg, pasta_destino):

    """
    Baixa anexos PDF de uma mensagem de e-mail, filtrando por termos específicos no nome do arquivo.

    Parâmetros:
    - msg (email.message.Message): O objeto da mensagem de e-mail.
    - pasta_destino (str): O caminho da pasta onde os PDFs serão salvos.

    Retorna:
    - int: A quantidade de arquivos PDF baixados que correspondem aos termos de busca.
    """

    #não é o bora bill! ok? coloquem outras palavras que sinalizem uma nf       
    arquivos_baixados_count = 0
    termos_de_busca = ["nota fiscal", 'nf', 'fatura', 'recibo', 'comprovante', 'invoice', 'bill', 'payment'] # Termos de busca para identificar arquivos PDF de nota fiscal/documentos similares
    
    # Compila uma expressão regular para buscar qualquer um dos termos de busca no nome do arquivo,
    # ignorando maiúsculas/minúsculas
    search_padrao = re.compile(r'\b(?:' + '|'.join(termos_de_busca) + r')\b', re.IGNORECASE)


    # Percorre todas as partes da mensagem de e-mail, tmb os arquyvos presentes no corpo
    for part in msg.walk():
        # Verifica se a parte é um anexo do tipo 'application' e subtipo 'pdf'
        if part.get_content_maintype()=='application' and part.get_content_subtype() == 'pdf':
            nome_arquivo = part.get_filename()
            if nome_arquivo:
                # Verifica se o nome do arquivo contém algum dos termos de busca definidos
                if search_padrao.search(nome_arquivo):

                    # Constrói o caminho completo para salvar o arquivo
                    caminhi_completo = os.path.join(pasta_destino,nome_arquivo)
                    try:
                        # Abre o arquivo em modo de escrita binária ('wb') e salva o conteúdo do anexo
                        with open(caminhi_completo, 'wb') as f:
                            f.write(part.get_payload(decode=True))
                        #mensagem do arquvo sendo salvo na pasta
                        print(f"Anexo PDF: '{nome_arquivo}'\n (Nota Fiscal/Similar) salvo em: '{pasta_destino}'")
                        arquivos_baixados_count += 1

                    except Exception as err:
                        print(f'erro ao salvar anexo: {nome_arquivo}.\nErro: {err}')
                else:
                    print(f"anexo PDF '{nome_arquivo}' ignorado (não contém termos de Nota Fiscal/Similar).")
            else:
                print("Anexo PDF encontrado, mas sem nome de arquivo.")
    return arquivos_baixados_count # Retorna a quantidade de arquivos baixados

######


def read_email_data():
    """
    Conecta-se a um servidor IMAP, lê os e-mails mais recentes e baixa anexos PDF relevantes.

    Retorna:
    - int: A quantidade total de anexos PDF baixados, ou False em caso de erro.
    """

    # Tenta obter as configurações de e-mail e a mensagem de erro (se houver)
    config_data, msg = get_dotenv_email()
    if config_data:
        try:
            # Cria um contexto SSL padrão para uma conexão segura
            context_ssl = ssl.create_default_context()
            # Conecta ao servidor IMAP usando SSL
            mail = imaplib.IMAP4_SSL(config_data["imap_server"], config_data["imap_port"], ssl_context=context_ssl)
            # Faz login na conta de e-mail
            #obs: isso me lembra entrar no mysql XD, mas é diferente
            mail.login(config_data["email"], config_data["password"])
            #entra na pagina do imbox dos email
            mail.select("INBOX")


            # Busca por todos os e-mails e obtém seus IDs
            status, dados_ids = mail.search(None, "ALL")
            lista_ids = dados_ids[0].split()
            lista_ids.reverse()
            
            # Imprime uma mensagem sobre a quantidade de e-mails que serão exibidos
            print(f"\nSeus {min(config_data['qtde_email'], len(lista_ids))} e-mails mais recentes: ")
            # Itera sobre os IDs dos e-mails, limitando à quantidade configurada
            for i, id_email in enumerate(lista_ids[:config_data["qtde_email"]]):
                # Busca o conteúdo completo do e-mail (RFC822)
                status, dados_msg = mail.fetch(id_email, "(RFC822)")
                if status == "OK": # Se a busca foi bem-sucedida
                    # Analisa os dados brutos do e-mail para criar um objeto Message
                    msg = email.message_from_bytes(dados_msg[0][1])
                    remtente_raw, codif_remtente=decode_header(msg["From"])[0]
                    remtente = remtente_raw
                    
                    # Se o remetente estiver em bytes, decodifica para string
                    if isinstance(remtente, bytes):
                        remtente = remtente.decode(codif_remtente or "utf-8", errors="ignore")
                    print(f'\nE-mail {i+1} - de: {remtente}')
                    
                    # Decodifica o cabeçalho 'Subject' (Assunto)
                    assunto_raw, codif_assunto = decode_header(msg["Subject"])[0]
                    assunto = assunto_raw
                    if isinstance(assunto, bytes):
                        assunto = assunto.decode(codif_assunto or "utd-8", errors="ignore")
                    print(f'\nAssunto: { assunto }')
                    print(f"\ndata: {msg['Date']}")
                    corpo_email = "Corpo do e-mail: Não foi possível extrair o conteúdo."
                    
                    # Verifica se o e-mail é multipart (contém várias partes, como texto e anexos)
                    if msg.is_multipart():
                        for part in msg.walk():
                            tipo_conteudo = part.get_content_type()
                            disposicao_cont = str(part.get("Content-Disposition"))
                            # Se for texto puro e não for um anexo
                            if tipo_conteudo == "text/plain" and "attachment" not in disposicao_cont:
                                try:
                                    corpo_email = part.get_payload(decode=True).decode(errors='ignore')
                                    break
                                except Exception:
                                    pass
                            # Se for HTML e não for um anexo
                            elif tipo_conteudo == "text/html" and "attachment" not in disposicao_cont:
                                try:
                                    # Decodifica o payload para obter o corpo do e-mail (HTML)
                                    corpo_email = part.get_payload(decode=True).decode(errors='ignore')
                                except Exception:
                                    pass
                    else:
                        try:
                            corpo_email = msg.get_payload(decode=True).decode(errors='ignore')
                        except Exception:
                            pass

                print("\nCorpo E-mail (trecho):")
                print(f"{corpo_email[:300]}...") 


                #parte para chamar função de baixar_pdf
                qtd_baixados  = baixar_anexos_pdf(msg, config_data["local_annex"])
                print("-" * 50) #espaçamento 

            mail.logout()       
            print(f"\nDesconectado do servidor IMAP.")
            return qtd_baixados
        

        except imaplib.IMAP4.error as e:
            print(f"\nERRO DE ACESSO OU LOGIN XD: {e}")
            print("Verifique seu e-mail, a SENHA DE APLICATIVO e se o IMAP está ativado no Gmail.")
            return False
        except ConnectionRefusedError:
            print("\nERRO DE CONEXÃO: O servidor recusou a conexão. Verifique se o endereço/porta estão corretos ou sua conexão com a internet.")
            return False
        except Exception as e:
            print(f"\nOCORREU UM ERRO INESPERADO XD: {e}")
            return False
    else:
        print(f'fracasso ao coletar dados do arquivo env')
        return False

