# db_setup.py (ou no próprio main.py, se preferir)

import mysql.connector
from mysql.connector import Error

def criar_banco_de_dados():
    try:
        connection = mysql.connector.connect(host='localhost', user='root', password='')

        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS db")
        print("Banco de dados criado ou já existente.")
    except Error as e:
        print(f"Erro ao criar banco de dados: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def criar_tabelas():
    try:
        connection = mysql.connector.connect(host='localhost', user='root', password='', database='db')
        cursor = connection.cursor()

        # Tabela de usuários
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS USUARIO(
            ID_USUARIO INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
            NOME_USUARIO VARCHAR(255),
            EMAIL_USUARIO VARCHAR(255) NOT NULL UNIQUE,
            SENHA_USUARIO VARCHAR(255) NOT NULL,
            TIPO_CONTA INT,
            DATA_CADASTRO DATE DEFAULT NULL,
            DATA_ATUALIZACAO DATE DEFAULT NULL,
            CONSTRAINT CHK_SENHA_TAMANHO CHECK (LENGTH(SENHA_USUARIO) >= 3),
            CONSTRAINT CHK_TIPO_CONTA CHECK (TIPO_CONTA IN (1, 2, 3))
        );
        ''')

        # ADICIONAR OUTRAS TABELAS AQUI

        # Procedure de cadastrar usuário
        cursor.execute('''
        CREATE PROCEDURE CADASTRAR_USUARIO(
        IN P_NOME_USUARIO VARCHAR(100),
        IN P_EMAIL_USUARIO VARCHAR(100),
        IN P_SENHA_USUARIO VARCHAR(100),
        IN P_TIPO_CONTA INT
        )
        BEGIN
        INSERT INTO USUARIO (NOME_USUARIO, EMAIL_USUARIO, SENHA_USUARIO, TIPO_CONTA)
        VALUES (P_NOME_USUARIO, P_EMAIL_USUARIO, P_SENHA_USUARIO, P_TIPO_CONTA);
        END
        ''')
        
        # Procedure de excluir usuários
        cursor.execute('''
        CREATE PROCEDURE EXCLUIR_USUARIO_ID( IN P_ID_USUARIO INT)
        BEGIN
        -- Verificar se o usuário existe
        IF NOT EXISTS (SELECT 1 FROM USUARIO WHERE ID_USUARIO = P_ID_USUARIO) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erro: Usuário não encontrado.';
        ELSE
        DELETE FROM USUARIO
        WHERE ID_USUARIO = P_ID_USUARIO;
        END IF;
        END
        ''')
        
        # Procedure de alterar usuário
        cursor.execute('''
        CREATE PROCEDURE alterar_usuario(
        IN P_ID_USUARIO INT,
        IN P_NOME_USUARIO VARCHAR(255),
        IN P_EMAIL_USUARIO VARCHAR(255),
        IN P_SENHA_USUARIO VARCHAR(255)
        )
        BEGIN
        -- Verificar se o usuário JA´ eXiste via ID
        IF NOT EXISTS (SELECT 1 FROM USUARIO WHERE ID_USUARIO = P_ID_USUARIO) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erro: Usuário não encontrado pelo ID.';
        ELSE
        -- Verificar se o usuário JA´ eXiste via email
        IF EXISTS (SELECT 1 FROM USUARIO WHERE EMAIL_USUARIO = P_EMAIL_USUARIO AND ID_USUARIO <> P_ID_USUARIO) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erro: O email informado já está cadastrado para outro usuário.';
        ELSE
        UPDATE USUARIO
        SET NOME_USUARIO = P_NOME_USUARIO,
        EMAIL_USUARIO = P_EMAIL_USUARIO,
        SENHA_USUARIO = P_SENHA_USUARIO
        WHERE ID_USUARIO = P_ID_USUARIO;
        END IF;
        END IF;
        END
        ''')        
        
        # Procedure de listar usuários
        cursor.execute('''
        CREATE PROCEDURE LISTAR_USUARIOS()
        BEGIN
        SELECT * FROM USUARIO;
        END

        ''')
        
        # Procedure de fazer login
        cursor.execute('''
        CREATE PROCEDURE FAZER_LOGIN(
	    IN P_EMAIL_USUARIO VARCHAR(255),
	    IN P_SENHA_USUARIO VARCHAR(255)
        )
        BEGIN
	    declare T_MENSAGEM VARCHAR(255);
	    IF EXISTS (SELECT 1 FROM USUARIO WHERE EMAIL_USUARIO = P_EMAIL_USUARIO AND SENHA_USUARIO = SHA2(P_SENHA_USUARIO, 256)
        ) THEN
        SELECT ID_USUARIO, NOME_USUARIO, EMAIL_USUARIO, TIPO_CONTA 
        FROM USUARIO
        WHERE EMAIL_USUARIO = P_EMAIL_USUARIO;
		SET T_MENSAGEM =  'LOGIN FEITO COM SUCESSO';
        ELSE
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erro: E-mail ou senha inválidos.';
        END IF;
        END 
        ''')

        # ADICIONAR OUTRAS PROCEDURES AQUI

        print("Tabelas e procedures criadas com sucesso.")
    except Error as e:
        print(f"Erro ao criar tabelas ou procedures: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
