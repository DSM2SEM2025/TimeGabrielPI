import imaplib
import ssl
import email 
import os
from email.header import decode_header #coletar dados do email
import re
from dotenv import load_dotenv

def baixar_anexos_pdf(msg, pasta_destino):
    #não é o bora bill! ok? coloquem outras palavras que sinalizem uma nf       
    termos_de_busca = ["nota fiscal", 'nf', 'fatura', 'recibo', 'comprovante', 'invoice', 'bill', 'payment']
    search_padrao = re.compile(r'\b(?:' + '|'.join(termos_de_busca) + r')\b', re.IGNORECASE)
    for part in msg.walk():
        if part.get_content_maintype()=='application' and part.get_content_subtype() == 'pdf':
            nome_arquivo = part.get_filename()
            if nome_arquivo:
                if search_padrao.search(nome_arquivo):
                    caminhi_completo = os.path.join(pasta_destino,nome_arquivo)
                    try:
                        with open(caminhi_completo, 'wb') as f:
                            f.write(part.get_payload(decode=True))
                        print(f"Anexo PDF: '{nome_arquivo}'\n (Nota Fiscal/Similar) salvo em: '{pasta_destino}'")
                    except Exception as err:
                        print(f'erro ao salvar anexo: {nome_arquivo}.\nErro: {err}')
                else:
                    print(f"anexo PDF '{nome_arquivo}' ignorado (não contém termos de Nota Fiscal/Similar).")
            else:
                print("Anexo PDF encontrado, mas sem nome de arquivo.")


def get_dotenv_email():
    try:
        dotenv_path="./model/produtos_model/modules_produtos_model/.env"
        if not os.path.exists(dotenv_path):
            raise FileNotFoundError(f"Arquivo .env não encontrado em: {dotenv_path}")
        load_dotenv(dotenv_path=dotenv_path)

        req_env_data = ["EMAIL","SENHA","SERVIDOR_IMAP","PORTA_IMAP","QUANTIDADE_EMAILS","PASTA_ANEXOS"]
        for var in req_env_data:
            if os.getenv(var) is None:
                raise ValueError(f"Variável de ambiente '{var}' não definida no arquivo .env")
        
        #isso deu mt dor de cabeça, mas vou deixar assim.... não quero ficar me envolvendo muito com o tratamento de erros
        try:
            qtde_email_val = int(os.getenv("QUANTIDADE_EMAILS"))
        except (ValueError, TypeError):
            raise ValueError("A variável de ambiente 'QUANTIDADE_EMAILS' deve ser um número inteiro válido.")
        
        email_config = {
            "email": os.getenv("EMAIL"),
            "password": os.getenv("SENHA"),
            "imap_server": os.getenv("SERVIDOR_IMAP"),
            "imap_port": os.getenv("PORTA_IMAP"),
            "qtde_email": qtde_email_val,
            "local_annex": os.getenv("PASTA_ANEXOS")
        }
        if not os.path.exists(email_config["local_annex"]):
            os.makedirs(email_config["local_annex"])
            print(f"Pasta '{email_config["local_annex"]}' criada para salvar anexos.")

        return email_config, 'Arquivo .env encontrado'
    except (FileNotFoundError, ValueError) as e: # Captura exceções específicas
        return None, f'Erro ao carregar configurações de e-mail: {e}'
    except Exception as e: # Captura qualquer outra exceção inesperada
        return None, f'Ocorreu um erro inesperado: {e}'


def read_email_data():
    config_data, msg = get_dotenv_email()
    if config_data:
        try:
            context_ssl = ssl.create_default_context()
            mail = imaplib.IMAP4_SSL(config_data["imap_server"], config_data["imap_port"], ssl_context=context_ssl)
            mail.login(config_data["email"], config_data["password"])
            mail.select("INBOX")

            status, dados_ids = mail.search(None, "ALL")
            lista_ids = dados_ids[0].split()
            lista_ids.reverse()
            

            print(f"\nSeus {min(config_data["qtde_email"], len(lista_ids))} e-mails mais recentes: ")

            for i, id_email in enumerate(lista_ids[:config_data["qtde_email"]]):
                status, dados_msg = mail.fetch(id_email, "(RFC822)")
                if status == "OK":
                    msg = email.message_from_bytes(dados_msg[0][1])
                    remtente_raw, codif_remtente=decode_header(msg["From"])[0]
                    remtente = remtente_raw
                    
                    if isinstance(remtente, bytes):
                        remtente = remtente.decode(codif_remtente or "utf-8", errors="ignore")
                    print(f'\nE-mail {i+1} - de: {remtente}')
                    
                    assunto_raw, codif_assunto = decode_header(msg["Subject"])[0]
                    assunto = assunto_raw
                    if isinstance(assunto, bytes):
                        assunto = assunto.decode(codif_assunto or "utd-8", errors="ignore")
                    print(f'\nAssunto: { assunto }')
                    print(f"\ndata: {msg['Date']}")
                    corpo_email = "Corpo do e-mail: Não foi possível extrair o conteúdo."
                    
                    if msg.is_multipart():
                        for part in msg.walk():
                            tipo_conteudo = part.get_content_type()
                            disposicao_cont = str(part.get("Content-Disposition"))
                            if tipo_conteudo == "text/plain" and "attachment" not in disposicao_cont:
                                try:
                                    corpo_email = part.get_payload(decode=True).decode(errors='ignore')
                                    break
                                except Exception:
                                    pass
                            elif tipo_conteudo == "text/html" and "attachment" not in disposicao_cont:
                                try:
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


                #parte para acionar função de baixar_pdf
                baixar_anexos_pdf(msg, config_data["local_annex"])
                print("-" * 50)

            mail.logout()       
            print(f"\nDesconectado do servidor IMAP.")
        except imaplib.IMAP4.error as e:
            print(f"\nERRO DE ACESSO OU LOGIN XD: {e}")
            print("Verifique seu e-mail, a SENHA DE APLICATIVO e se o IMAP está ativado no Gmail.")
        except ConnectionRefusedError:
            print("\nERRO DE CONEXÃO: O servidor recusou a conexão. Verifique se o endereço/porta estão corretos ou sua conexão com a internet.")
        except Exception as e:
            print(f"\nOCORREU UM ERRO INESPERADO XD: {e}")
    else:
        return f'fracasso ao coletar dados do arquivo env'
  
read_email_data()



   # config = DBModel.get_dotenv()

    # if not os.path.exists():