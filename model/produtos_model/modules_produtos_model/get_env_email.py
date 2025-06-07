import re
from dotenv import load_dotenv
import os

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