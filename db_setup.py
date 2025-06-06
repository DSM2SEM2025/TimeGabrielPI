# db_setup.py (ou no próprio main.py, se preferir)

import mysql.connector
from mysql.connector import Error

def criar_banco_de_dados():
    try:
        connection = mysql.connector.connect(host='localhost', user='root', password='962266514')

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
        connection = mysql.connector.connect(host='localhost', user='root', password='962266514', database='db')
        cursor = connection.cursor()

        #CRIAÇÃO DE TABELAS

        # Tabela de usuários
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS USUARIO(
            ID_USUARIO INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
            EMAIL_USUARIO VARCHAR(255) NOT NULL UNIQUE,
            SENHA_USUARIO VARCHAR(255) NOT NULL,
            DATA_CADASTRO DATE DEFAULT NULL,
            DATA_ATUALIZACAO DATE DEFAULT NULL,
            CONSTRAINT CHK_SENHA_TAMANHO CHECK (LENGTH(SENHA_USUARIO) >= 3)
        );
        ''')
        
        # Tabela de estoque
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS ESTOQUE(
	    ID_ESTOQUE INT AUTO_INCREMENT PRIMARY KEY,
    	TIPO_ESTOQUE VARCHAR(255) NOT NULL UNIQUE,
	    QTDE_ESTOQUE INT
        );
        ''')
        
        #Tabela de produtos
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS PRODUTOS(
	    ID_PRODUTO INT AUTO_INCREMENT PRIMARY key,
        NOME_PRODUTO VARCHAR(255) NOT NULL UNIQUE,
        PRECO_PRODUTO FLOAT NOT NULL,
        FK_ID_ESTOQUE INT DEFAULT NULL,
	    DESC_PRODUTO VARCHAR(255) NULL,
        FOREIGN KEY (FK_ID_ESTOQUE) REFERENCES ESTOQUE(ID_ESTOQUE) ON DELETE SET NULL
        );               
        ''')
        
        #Tabela de movimentação
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS MOVIMENTACAO(
	    ID_MOVIMENTACAO INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
	    FK_ID_PRODUTO INT NOT NULL,
        QTDE INT NOT NULL, 
        TIPO_MOVIMENTACAO VARCHAR(255) NOT NULL,
        DATA_MOVIMENTACAO DATE NOT NULL,
        FOREIGN KEY (FK_ID_PRODUTO) REFERENCES PRODUTOS(ID_PRODUTO)
        );              
        ''')
        
        #tabela de pedido entrega
        cursor.execute('''
        create table IF NOT EXISTS PEDIDO_ENTREGA (
	    id_entrega int auto_increment primary key not null,
	    status_entrega boolean default FALSE,
        fk_id_produto int, 
        fk_ID_MOVIMENTACAO int, 
        foreign key (fk_id_produto) references PRODUTOS(ID_PRODUTO),
        foreign key (fk_ID_MOVIMENTACAO) references MOVIMENTACAO(ID_MOVIMENTACAO)
    
        );               
        ''')

        # Procedure de cadastrar usuário
        cursor.execute('''
        CREATE PROCEDURE CADASTRAR_USUARIO(
        IN P_EMAIL_USUARIO VARCHAR(100),
        IN P_SENHA_USUARIO VARCHAR(100)
        )
        BEGIN
        INSERT INTO USUARIO (EMAIL_USUARIO, SENHA_USUARIO)
        VALUES (P_EMAIL_USUARIO, P_SENHA_USUARIO);
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
        UPDATE USUARIO SET
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
        
        #procedure cadastrar produto no estoque
        cursor.execute('''
        CREATE PROCEDURE CADASTRAR_PRODUTO_ESTOQUE(
        IN P_NOME_PRODUTO VARCHAR(255),
        IN P_PRECO_PRODUTO FLOAT,
        IN P_DESC_PRODUTO VARCHAR(255),
        IN P_TIPO_ESTOQUE VARCHAR(255),
        IN P_QTDE_ESTOQUE INT
        )
        BEGIN
        DECLARE V_ID_PRODUTO INT;
        DECLARE V_ID_ESTOQUE INT;

        START TRANSACTION;

        SELECT ID_PRODUTO, FK_ID_ESTOQUE INTO V_ID_PRODUTO, V_ID_ESTOQUE
        FROM PRODUTOS
        WHERE NOME_PRODUTO = P_NOME_PRODUTO;

        IF V_ID_PRODUTO IS NOT NULL THEN
        UPDATE ESTOQUE
        SET QTDE_ESTOQUE = QTDE_ESTOQUE + P_QTDE_ESTOQUE
        WHERE ID_ESTOQUE = V_ID_ESTOQUE;
        ELSE
        SELECT ID_ESTOQUE INTO V_ID_ESTOQUE
        FROM ESTOQUE
        WHERE TIPO_ESTOQUE = LOWER(P_TIPO_ESTOQUE);

        IF V_ID_ESTOQUE IS NOT NULL THEN
        UPDATE ESTOQUE
        SET QTDE_ESTOQUE = QTDE_ESTOQUE + P_QTDE_ESTOQUE
        WHERE ID_ESTOQUE = V_ID_ESTOQUE;

        INSERT INTO PRODUTOS(NOME_PRODUTO, PRECO_PRODUTO, FK_ID_ESTOQUE, DESC_PRODUTO)
        VALUES(P_NOME_PRODUTO, P_PRECO_PRODUTO, V_ID_ESTOQUE, P_DESC_PRODUTO);
        ELSE
        INSERT INTO ESTOQUE(TIPO_ESTOQUE, QTDE_ESTOQUE)
        VALUES(P_TIPO_ESTOQUE, P_QTDE_ESTOQUE);
        SET V_ID_ESTOQUE = LAST_INSERT_ID();

        INSERT INTO PRODUTOS(NOME_PRODUTO, PRECO_PRODUTO, FK_ID_ESTOQUE, DESC_PRODUTO)
        VALUES(P_NOME_PRODUTO, P_PRECO_PRODUTO, V_ID_ESTOQUE, P_DESC_PRODUTO);
        END IF;
        END IF;

        COMMIT;
        END
        ''')
        
        #procedure de atualizar produto
        cursor.execute('''
        CREATE PROCEDURE ATUALIZAR_PRODUTO(
            IN P_NOME_PRODUTO VARCHAR(255),
            IN P_PRECO_PRODUTO FLOAT,
            IN P_DESC_PRODUTO VARCHAR(255),
            IN P_TIPO_ESTOQUE VARCHAR(255),
            IN P_QTDE_ESTOQUE INT,
            IN TIPO_ATUALIZACAO INT
        )
        BEGIN
            DECLARE MSG_RES VARCHAR(100);
            DECLARE V_ID_ESTOQUE INT;
            DECLARE V_ID_PRODUTO INT;
            
            SELECT ID_PRODUTO INTO V_ID_PRODUTO FROM PRODUTOS WHERE NOME_PRODUTO = P_NOME_PRODUTO;
            
            IF V_ID_PRODUTO IS NULL THEN
                SET MSG_RES = 'PRODUTO NÃO ENCONTRADO';
            ELSE 
                SELECT ID_ESTOQUE INTO V_ID_ESTOQUE FROM ESTOQUE WHERE TIPO_ESTOQUE = P_TIPO_ESTOQUE;
                IF V_ID_ESTOQUE IS NULL AND TIPO_ATUALIZACAO = 1 THEN
                    SET MSG_RES = 'TIPO DE ESTOQUE NÃO ENCONTRADO';
                ELSEIF TIPO_ATUALIZACAO = 1 THEN
                    START TRANSACTION;
                    UPDATE ESTOQUE 
                    SET 
                        TIPO_ESTOQUE = P_TIPO_ESTOQUE, 
                        QTDE_ESTOQUE = P_QTDE_ESTOQUE WHERE ID_ESTOQUE = V_ID_ESTOQUE;
                        
                    UPDATE PRODUTOS
                    SET 
                        NOME_PRODUTO = P_NOME_PRODUTO,
                        PRECO_PRODUTO = P_PRECO_PRODUTO,
                        DESC_PRODUTO =  P_DESC_PRODUTO WHERE ID_PRODUTO = V_ID_PRODUTO;
                        
                    SET MSG_RES = 'ALTERAÇÃO FEITA COM SUCESSO NO PRODUTO E SEU ESTOQUE.';
                    COMMIT;
                ELSEIF TIPO_ATUALIZACAO = 2 THEN
                        UPDATE PRODUTOS SET 
                            NOME_PRODUTO = P_NOME_PRODUTO,
                            PRECO_PRODUTO = P_PRECO_PRODUTO,
                            DESC_PRODUTO =  P_DESC_PRODUTO WHERE ID_PRODUTO = V_ID_PRODUTO;
                    SET MSG_RES = 'ALTERAÇÃO FEITA COM SUCESSO NO PRODUTO.';
                    COMMIT;
                ELSE
                    SET MSG_RES = 'OPÇÃO INVALIDA';
                END IF;
            END IF;
            SELECT MSG_RES;
        END
        ''')
        
        #Procedure de listar produtos
        cursor.execute('''
        CREATE PROCEDURE LISTAR_PRODUTOS()
        BEGIN
        SELECT * FROM PRODUTOS;
        END
        ''')
        
        # Procedure de fazer login
        cursor.execute('''
        CREATE PROCEDURE FAZER_LOGIN(
	    IN P_EMAIL_USUARIO VARCHAR(255),
	    IN P_SENHA_USUARIO VARCHAR(255)
        ) 
        BEGIN
        IF EXISTS (
        SELECT 1 FROM USUARIO 
        WHERE EMAIL_USUARIO = P_EMAIL_USUARIO 
        AND SENHA_USUARIO = P_SENHA_USUARIO)  
        THEN
        SELECT
        ID_USUARIO,
        EMAIL_USUARIO,
        'Login realizado com sucesso!' AS MENSAGEM
        FROM USUARIO
        WHERE EMAIL_USUARIO = P_EMAIL_USUARIO;
        ELSE
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erro: Email ou senha inválidos.';
        END IF;
        END
        ''')
        
        #Procedure exluir produto geral
        cursor.execute('''
        CREATE PROCEDURE EXCLUIR_PRODUTO_GERAL(
        IN P_ID_PRODUTO INT
        )
        BEGIN
        DECLARE estoque_id INT;

        START TRANSACTION;

        SELECT FK_ID_ESTOQUE INTO estoque_id
        FROM PRODUTOS
        WHERE ID_PRODUTO = P_ID_PRODUTO;

        IF estoque_id IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erro: Produto não encontrado.';
        ROLLBACK;
        ELSE
        DELETE FROM PRODUTOS
        WHERE ID_PRODUTO = P_ID_PRODUTO;

        DELETE FROM ESTOQUE
        WHERE ID_ESTOQUE = estoque_id;

        COMMIT;
        END IF;
        END               
        ''')
        
        # Procedure de procurar produto por ID
        cursor.execute('''
        CREATE PROCEDURE PROCURAR_PRODUTO_ID(
	    IN P_ID_PRODUTO INT
        )
        BEGIN
	    IF exists (SELECT 1 FROM PRODUTOS WHERE ID_PRODUTO = P_ID_PRODUTO) THEN
		SELECT
		p.ID_PRODUTO,
		p.NOME_PRODUTO,
		p.PRECO_PRODUTO,
		p.DESC_PRODUTO,
		e.ID_ESTOQUE,
		e.TIPO_ESTOQUE
		FROM PRODUTOS p JOIN ESTOQUE e ON p.FK_ID_ESTOQUE = e.ID_ESTOQUE WHERE p.ID_PRODUTO = P_ID_PRODUTO;
        ELSE
		SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Erro: Estoque não encontrado.';
        END IF;
        END               
        ''')

        #Procedure de consultar histórico
        cursor.execute('''
        CREATE PROCEDURE CONSULTAR_HISTORICO(
        IN P_ID_PRODUTO INT
        #p_produto_id 
        )
        BEGIN
        SELECT m.*, p.NOME_PRODUTO AS nome_produto
        FROM MOVIMENTACAO m
        JOIN PRODUTOS p ON m.FK_ID_PRODUTO = p.ID_PRODUTO
        WHERE m.FK_ID_PRODUTO = P_ID_PRODUTO
        ORDER BY m.DATA_MOVIMENTACAO DESC;
        END               
        ''')
        
        #procedure de gerar relatório
        cursor.execute('''
        CREATE PROCEDURE GERAR_RELATORIO_ESTOQUE(
        IN p_id_estoque INT
        )
        BEGIN
        SELECT p.ID_PRODUTO, p.NOME_PRODUTO, p.PRECO_PRODUTO, ep.QTDE, 
        (p.PRECO_PRODUTO * ep.QTDE) AS ValorTotal FROM ESTOQUE_PRODUTO ep
    
        JOIN PRODUTOS p ON ep.FK_ID_PRODUTO = p.ID_PRODUTO
        WHERE ep.FK_ID_ESTOQUE = p_id_estoque
        ORDER BY p.NOME_PRODUTO;
        END               
        ''')
        
        #Procedure de registrar movimento
        cursor.execute('''
        CREATE PROCEDURE REGISTRAR_MOVIMENTO(
        IN p_fk_id_produto INT,
        IN p_qtde INT,
        IN p_tipo_movimentacao VARCHAR(255)
        )
        BEGIN
        IF NOT EXISTS (SELECT 1 FROM PRODUTOS WHERE ID_PRODUTO = p_fk_id_produto) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erro: ID de produto inválido.';
        ELSEIF p_qtde = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erro: A quantidade movimentada não pode ser zero.';
        ELSEIF p_tipo_movimentacao NOT IN ('entrada', 'saida', 'ajuste') THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erro: Tipo de movimentação inválido (deve ser "entrada", "saida" ou "ajuste").';
        ELSE
        INSERT INTO MOVIMENTACAO (FK_ID_PRODUTO, QTDE, TIPO_MOVIMENTACAO, DATA_MOVIMENTACAO)
        VALUES (p_fk_id_produto, p_qtde, p_tipo_movimentacao, CURDATE());
        
        IF p_tipo_movimentacao = 'entrada' THEN
        UPDATE ESTOQUE_PRODUTO
        SET QTDE = QTDE + p_qtde
        WHERE FK_ID_PRODUTO = p_fk_id_produto;

        ELSEIF p_tipo_movimentacao = 'saida' THEN
        UPDATE ESTOQUE_PRODUTO
        SET QTDE = QTDE - p_qtde
        WHERE FK_ID_PRODUTO = p_fk_id_produto AND QTDE >= p_qtde;
        IF ROW_COUNT() = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erro: Quantidade insuficiente em estoque para realizar a saída.';
        END IF;
        ELSEIF p_tipo_movimentacao = 'ajuste' THEN
        UPDATE ESTOQUE_PRODUTO
        SET QTDE = QTDE + p_qtde
		WHERE FK_ID_PRODUTO = p_fk_id_produto;
        END IF;
        END IF;
        END               
        ''')
        
        #procedure de verificar entrega
        cursor.execute('''
        CREATE PROCEDURE VERIFICAR_ENTREGA(
	    IN P_ID_ENTREGA INT 
        )
        BEGIN 
	    IF exists (SELECT 1 FROM PEDIDO_ENTREGA WHERE ID_ENTREGA = P_ID_ENTREGA) THEN
		UPDATE PEDIDO_ENTREGA SET STATUS_ENTREGA = TRUE WHERE ID_ENTREGA = P_ID_ENTREGA;
        ELSE 
		SET message_text = 'PRODUTO NÃO ENCONTRADO';
        END IF;
        END               
        ''')
        
        #procedure de notificação de falta de produto
        cursor.execute('''
        CREATE PROCEDURE NOTIFICACAO_FALTA_PRODUTO(
	    IN P_NOME_PRODUTO VARCHAR(255), 
	    IN limite_baixo INT, 
	    IN limite_alto INT
        )
        BEGIN
        DECLARE V_QTDE_ESTOQUE INT;
        SELECT ESTOQUE.QTDE_ESTOQUE INTO V_QTDE_ESTOQUE
        FROM PRODUTOS
        JOIN ESTOQUE ON PRODUTO.FK_ID_ESTOQUE = ESTOQUE.ID_ESTOQUE
        WHERE PRODUTO.NOME_PRODUTO = P_NOME_PRODUTO;

        IF V_QTDE_ESTOQUE IS NULL THEN
        SELECT CONCAT('Produto "', P_NOME_PRODUTO, '" não encontrado no estoque.') AS Notificação;
        ELSEIF V_QTDE_ESTOQUE = 0 THEN
        SELECT CONCAT('ALERTA: Produto "', P_NOME_PRODUTO, '" está esgotado!') AS Notificação;
        ELSEIF V_QTDE_ESTOQUE <= limite_baixo THEN
        SELECT CONCAT('ATENÇÃO: Produto "', P_NOME_PRODUTO, '" com estoque baixo (', V_QTDE_ESTOQUE, ' unidades).') AS Notificação;
        ELSE
        SELECT CONCAT('Produto "', P_NOME_PRODUTO, '" com estoque normal (', V_QTDE_ESTOQUE, ' unidades).') AS Notificação;
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
