
	--	#PROCEDURES
        
	#PROCEDURES DA TABELA USUARIO
    #CADASTRAR USUARIO
DELIMITER //

CREATE PROCEDURE CADASTRAR_USUARIO(
    IN P_EMAIL_USUARIO VARCHAR(100),
    IN P_SENHA_USUARIO VARCHAR(100)
)
BEGIN
    INSERT INTO USUARIO (EMAIL_USUARIO, SENHA_USUARIO)
    VALUES (P_EMAIL_USUARIO, P_SENHA_USUARIO);
END //

DELIMITER ;


	#EXCLUIR USUARIO
DELIMITER //
CREATE PROCEDURE EXCLUIR_USUARIO_ID(
    IN P_ID_USUARIO INT
)
BEGIN
    -- Verificar se o usuário existe
    IF NOT EXISTS (SELECT 1 FROM USUARIO WHERE ID_USUARIO = P_ID_USUARIO) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erro: Usuário não encontrado.';
    ELSE
        DELETE FROM USUARIO
        WHERE ID_USUARIO = P_ID_USUARIO;
    END IF;
END //
DELIMITER ;

#TESTE
CALL EXCLUIR_USUARIO_ID(3);

	#ALTERAR USUARIO
DELIMITER //
CREATE PROCEDURE alterar_usuario(
    IN P_ID_USUARIO INT
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
            SET EMAIL_USUARIO = P_EMAIL_USUARIO,
                SENHA_USUARIO = P_SENHA_USUARIO
            WHERE ID_USUARIO = P_ID_USUARIO;
        END IF;
    END IF;
END //
DELIMITER ;

	#LISTAR USUARIO
DELIMITER //

CREATE PROCEDURE LISTAR_USUARIOS()
BEGIN
    SELECT * FROM USUARIO;
END //

DELIMITER ;

#TESTE
CALL LISTAR_USUARIOS();
SELECT *FROM USUARIO;


	#FAZER LOGIN
    
DELIMITER //

CREATE PROCEDURE FAZER_LOGIN(
    IN P_EMAIL_USUARIO VARCHAR(255),
    IN P_SENHA_USUARIO VARCHAR(255)
) 
BEGIN
    IF EXISTS (
        SELECT 1 FROM USUARIO 
        WHERE EMAIL_USUARIO = P_EMAIL_USUARIO 
        AND SENHA_USUARIO = P_SENHA_USUARIO
    ) THEN
        SELECT
            ID_USUARIO,
            EMAIL_USUARIO,
            'Login realizado com sucesso!' AS MENSAGEM
        FROM USUARIO
        WHERE EMAIL_USUARIO = P_EMAIL_USUARIO;
    ELSE
        SELECT NULL AS ID_USUARIO
               NULL AS EMAIL_USUARIO,
               'Credenciais inválidas.' AS MENSAGEM;
    END IF;
END //

DELIMITER ;


	#PROCEDURES DA TABELA ESTOQUE. JUNTEI COM OUTRA FUNÇÃO DE PRODUTOS: ALTERAR ESTOQUE MANUAL
    


    -- REMOVER PRODUTO
DELIMITER //

DROP PROCEDURE IF EXISTS EXCLUIR_PRODUTO_GERAL;
DELIMITER //

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
END //

DELIMITER ;

CALL EXCLUIR_PRODUTO_GERAL('UVA');


    -- PROCURAR PRODUTO
DELIMITER //
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
            p.NUMERO_NF_PRODUTO,
            p.VALIDADE_PRODUTO,
            p.FORNECEDOR_PRODUTO,
            p.QTD_MINIMA_PRODUTO,
			e.ID_ESTOQUE,
			e.CATEGORIA_ESTOQUE,
            e.QTDE_ESTOQUE
		FROM PRODUTOS p JOIN ESTOQUE e ON p.FK_ID_ESTOQUE = e.ID_ESTOQUE WHERE p.ID_PRODUTO = P_ID_PRODUTO;
    ELSE
		SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Erro: Estoque não encontrado.';
    END IF;
END //
DELIMITER ;

call PROCURAR_PRODUTO_ID(1);




# CONSULTAR HISTORICO


###
DELIMITER //
CREATE PROCEDURE CONSULTAR_HISTORICO(
    IN P_ID_PRODUTO INT
)
BEGIN
    SELECT m.*, p.NOME_PRODUTO AS nome_produto
    FROM MOVIMENTACAO m
    JOIN PRODUTOS p ON m.FK_ID_PRODUTO = p.ID_PRODUTO
    WHERE m.FK_ID_PRODUTO = P_ID_PRODUTO
    ORDER BY m.DATA_MOVIMENTACAO DESC;
END //
DELIMITER ;
CALL CONSULTAR_HISTORICO(2);


	#PROCEDURE GERAR RELATORIO
    
    
DELIMITER //
CREATE PROCEDURE GERAR_RELATORIO_ESTOQUE(
    IN p_id_estoque INT
)
BEGIN
    SELECT p.ID_PRODUTO, p.NOME_PRODUTO, p.PRECO_PRODUTO, ep.QTDE, 
    (p.PRECO_PRODUTO * ep.QTDE) AS ValorTotal FROM ESTOQUE_PRODUTO ep
    
    JOIN PRODUTO p ON ep.FK_ID_PRODUTO = p.ID_PRODUTO
    WHERE ep.FK_ID_ESTOQUE = p_id_estoque
    ORDER BY p.NOME_PRODUTO;
END //
DELIMITER ;

CALL GERAR_RELATORIO_ESTOQUE(2);


#PROCEDURE 
#	CONFIRMAR_ENTREGA 
	#NÃO FEITO PQ NÃO SEI SE DEVIA TER OUTRA TABELA CHAMADA ENTREGA COM CHAVES DE PRODUTO E MOVIMENTACAO. 
    #NESSA NOVA TABELA TERIA UM ATRIBUTO CHAMADO: STATUS, NO QUAL EU FARIA A PROCEDURE
	# ESPERO RESPOSTA
    
#REGISTRAR SAIDA SERIA NA TABELA ENTREGA OU DEVE REGISTRAR TODAS AS SAIDAS DA TABELA, TANTO ENTREGAS E EXCLUSÓES FEITAS PELO USUARIO??

# ATUALIZAR ESTOQUE:
	# FAZER VIA EMAIL PELO BANCO, EU ACHO QUE NÃO DÁ.... ACREDITO QUE DEVE FAZER A FUNÇÃO PELO BACK-END MSM
    


DELIMITER //
CREATE PROCEDURE REGISTRAR_MOVIMENTO(
    IN p_fk_id_produto INT,
    IN p_qtde INT,
    IN p_tipo_movimentacao VARCHAR(255)
)
BEGIN
    IF NOT EXISTS (SELECT 1 FROM PRODUTO WHERE ID_PRODUTO = p_fk_id_produto) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erro: ID de produto inválido ou produto não associado a um estoque.';
    ELSEIF p_qtde = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erro: A quantidade movimentada não pode ser zero.';
    ELSEIF p_tipo_movimentacao NOT IN ('entrada', 'saida', 'ajuste') THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erro: Tipo de movimentação inválido (deve ser "entrada", "saida" ou "ajuste").';
    ELSE
        -- Insere o registro na tabela MOVIMENTACAO
        INSERT INTO MOVIMENTACAO (FK_ID_PRODUTO, QTDE, TIPO_MOVIMENTACAO, DATA_MOVIMENTACAO)
        VALUES (p_fk_id_produto, p_qtde, p_tipo_movimentacao, CURDATE());
        
        -- Obtém a quantidade atual do estoque
        SELECT QTDE_ESTOQUE INTO v_qtde_atual_estoque
        FROM ESTOQUE
        WHERE ID_ESTOQUE = v_id_estoque;

        -- Atualiza a quantidade na tabela ESTOQUE
        IF p_tipo_movimentacao = 'entrada' THEN
            UPDATE ESTOQUE
            SET QTDE_ESTOQUE = QTDE_ESTOQUE + p_qtde
            WHERE ID_ESTOQUE = v_id_estoque;

        ELSEIF p_tipo_movimentacao = 'saida' THEN
            IF v_qtde_atual_estoque < p_qtde THEN
                SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Erro: Quantidade insuficiente em estoque para realizar a saída.';
            ELSE
                UPDATE ESTOQUE
                SET QTDE_ESTOQUE = QTDE_ESTOQUE - p_qtde
                WHERE ID_ESTOQUE = v_id_estoque;
            END IF;
        ELSEIF p_tipo_movimentacao = 'ajuste' THEN
            -- Para ajuste, estamos adicionando a quantidade. Se for um ajuste para baixo, p_qtde deve ser negativo.
            UPDATE ESTOQUE
            SET QTDE_ESTOQUE = QTDE_ESTOQUE + p_qtde
            WHERE ID_ESTOQUE = v_id_estoque;
        END IF;
    END IF;
END //
DELIMITER ;

CALL REGISTRAR_MOVIMENTO(
2, -- p_fk_id_produto
3, -- p_qtde
'entrada' -- p_tipo_movimentacao
);


SELECT *FROM PRODUTO;
SELECT *FROM ESTOQUE_PRODUTO;
SELECT *FROM ESTOQUE;
SELECT *FROM MOVIMENTACAO;



DELIMITER //
CREATE PROCEDURE VERIFICAR_ENTREGA(
	IN P_ID_ENTREGA INT 
)
BEGIN 
	IF exists (SELECT 1 FROM PEDIDO_ENTREGA WHERE ID_ENTREGA = P_ID_ENTREGA) THEN
		UPDATE PEDIDO_ENTREGA SET STATUS_ENTREGA = TRUE WHERE ID_ENTREGA = P_ID_ENTREGA;
    ELSE 
		SET message_text = 'PRODUTO NÃO ENCONTRADO';
    END IF;
END //
DELIMITER ;


    --- PROCEDURES PARA FAZER

	#CADASTRAR PRODUTO
DELIMITER //
CREATE PROCEDURE CADASTRAR_PRODUTO_ESTOQUE(
    IN P_NOME_PRODUTO VARCHAR(255),
    IN P_PRECO_PRODUTO FLOAT,
    IN P_DESC_PRODUTO VARCHAR(255),
    IN P_NUMERO_NF_PRODUTO VARCHAR(255),
    IN P_VALIDADE_PRODUTO DATE,
    IN P_FORNECEDOR_PRODUTO VARCHAR(255),
    IN P_QTD_MINIMA_PRODUTO INT,
    IN P_CATEGORIA_ESTOQUE VARCHAR(50),
    IN P_QTDE_ESTOQUE INT
)
BEGIN
    DECLARE V_ID_PRODUTO INT;
    DECLARE V_ID_ESTOQUE INT;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

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
        WHERE CATEGORIA_ESTOQUE = LOWER(P_CATEGORIA_ESTOQUE); 

        IF V_ID_ESTOQUE IS NOT NULL THEN
            UPDATE ESTOQUE
            SET QTDE_ESTOQUE = QTDE_ESTOQUE + P_QTDE_ESTOQUE
            WHERE ID_ESTOQUE = V_ID_ESTOQUE;

            INSERT INTO PRODUTOS(NOME_PRODUTO, PRECO_PRODUTO, FK_ID_ESTOQUE, DESC_PRODUTO, NUMERO_NF_PRODUTO, VALIDADE_PRODUTO, FORNECEDOR_PRODUTO, QTD_MINIMA_PRODUTO) 
            VALUES(P_NOME_PRODUTO, P_PRECO_PRODUTO, V_ID_ESTOQUE, P_DESC_PRODUTO, P_NUMERO_NF_PRODUTO, P_VALIDADE_PRODUTO, P_FORNECEDOR_PRODUTO, P_QTD_MINIMA_PRODUTO);

        ELSE
            INSERT INTO ESTOQUE(CATEGORIA_ESTOQUE, QTDE_ESTOQUE)
            VALUES(P_CATEGORIA_ESTOQUE, P_QTDE_ESTOQUE);
            
            SET V_ID_ESTOQUE = LAST_INSERT_ID();

            INSERT INTO PRODUTOS(NOME_PRODUTO, PRECO_PRODUTO, FK_ID_ESTOQUE, DESC_PRODUTO, NUMERO_NF_PRODUTO, VALIDADE_PRODUTO, FORNECEDOR_PRODUTO, QTD_MINIMA_PRODUTO) 
            VALUES(P_NOME_PRODUTO, P_PRECO_PRODUTO, V_ID_ESTOQUE, P_DESC_PRODUTO, P_NUMERO_NF_PRODUTO, P_VALIDADE_PRODUTO, P_FORNECEDOR_PRODUTO, P_QTD_MINIMA_PRODUTO);
        END IF;
    END IF;

    COMMIT; -- Confirma a transação
END//
DELIMITER ;
CALL CADASTRAR_PRODUTO_ESTOQUE(
    'Teclado Mecânico',   -- P_NOME_PRODUTO (produto existente)
    250.00,               -- P_PRECO_PRODUTO (este valor não é usado na atualização do produto existente)
    'Teclado RGB com switches azuis', -- P_DESC_PRODUTO (este valor não é usado na atualização do produto existente)
    'Eletrônicos',        -- P_TIPO_ESTOQUE (usado para encontrar o estoque se o produto fosse novo)
    20,                   -- P_QTDE_ESTOQUE (adiciona 20 à quantidade atual do estoque)
    'NF-XXXX-00000'       -- P_NUMERO_NF_PRODUTO (este valor não é usado na atualização do produto existente)
);
CALL CADASTRAR_PRODUTO_ESTOQUE(
    'Mouse Gamer',        -- P_NOME_PRODUTO (novo produto)
    120.00,               -- P_PRECO_PRODUTO
    'Mouse óptico com 6 botões programáveis', -- P_DESC_PRODUTO
    'Eletrônicos',        -- P_TIPO_ESTOQUE (estoque existente)
    100,                  -- P_QTDE_ESTOQUE (adiciona a quantidade ao estoque existente)
    'NF-2025-00124'       -- P_NUMERO_NF_PRODUTO (novo)
);



	#LISTAR PRODUTOS
DELIMITER //

CREATE PROCEDURE LISTAR_PRODUTOS()
BEGIN
    SELECT * FROM PRODUTOS;
END //

DELIMITER ;

#TESTE
CALL LISTAR_PRODUTOS();
SELECT *FROM PRODUTOS;


    # NOTIFICAÇÃO DE FALTA DE PRODUTO
DELIMITER //

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
END //

DELIMITER ;
call NOTIFICACAO_FALTA_PRODUTO('MAÇA', 500, 5000)

---    #ATUALIZAR PRODUTO

delimiter //

CREATE PROCEDURE ATUALIZAR_ESTOQUE_PRODUTO(
-- Parâmetros para ESTOQUE (opcionais)
IN p_id_estoque_upd INT,
IN p_categoria_estoque_upd VARCHAR(50),
IN p_qtde_estoque_upd INT,

-- Parâmetros para PRODUTOS (opcionais)
IN p_id_produto_upd INT,
IN p_nome_produto_upd VARCHAR(255),
IN p_preco_produto_upd FLOAT,
IN p_fk_id_estoque_upd INT,
IN p_desc_produto_upd VARCHAR(255),
IN p_numero_nf_produto_upd VARCHAR(255),
IN p_validade_produto_upd DATE,
IN p_fornecedor_produto_upd VARCHAR(255),
IN p_qtd_minima_produto_upd INT
)
BEGIN
-- Handler de erro para reverter transação em caso de exceção SQL
DECLARE EXIT HANDLER FOR SQLEXCEPTION
BEGIN
ROLLBACK; 
RESIGNAL; 
END;

START TRANSACTION;

IF p_id_estoque_upd IS NOT NULL THEN
UPDATE ESTOQUE
SET
    CATEGORIA_ESTOQUE = COALESCE(p_categoria_estoque_upd, CATEGORIA_ESTOQUE), 
    QTDE_ESTOQUE = COALESCE(p_qtde_estoque_upd, QTDE_ESTOQUE)
WHERE ID_ESTOQUE = p_id_estoque_upd;
END IF;

-- Atualiza o PRODUTO se um ID de produto for fornecido
IF p_id_produto_upd IS NOT NULL THEN
UPDATE PRODUTOS
SET
    NOME_PRODUTO = COALESCE(p_nome_produto_upd, NOME_PRODUTO),
    PRECO_PRODUTO = COALESCE(p_preco_produto_upd, PRECO_PRODUTO),
    FK_ID_ESTOQUE = COALESCE(p_fk_id_estoque_upd, FK_ID_ESTOQUE),
    DESC_PRODUTO = COALESCE(p_desc_produto_upd, DESC_PRODUTO),
    NUMERO_NF_PRODUTO = COALESCE(p_numero_nf_produto_upd, NUMERO_NF_PRODUTO),
    VALIDADE_PRODUTO = COALESCE(p_validade_produto_upd, VALIDADE_PRODUTO),
    FORNECEDOR_PRODUTO = COALESCE(p_fornecedor_produto_upd, FORNECEDOR_PRODUTO),
    QTD_MINIMA_PRODUTO = COALESCE(p_qtd_minima_produto_upd, QTD_MINIMA_PRODUTO)
WHERE ID_PRODUTO = p_id_produto_upd;
END IF;

COMMIT;

END  //
DELIMITER ;

select *from produto;


CALL ATUALIZAR_ESTOQUE_PRODUTO(
    NULL, NULL, NULL, -- Parâmetros do estoque como NULL
    101,                      -- p_id_produto_upd (ID do Produto)
    'Monitor Gamer 27"',     -- p_nome_produto_upd
    1599.99,                  -- p_preco_produto_upd
    5,                        -- p_fk_id_estoque_upd (ID de um estoque existente, ou NULL)
    'QHD, 144Hz, Freesync',   -- p_desc_produto_upd
    'NF-MONITOR-001'          -- p_numero_nf_produto_upd
);


CALL ATUALIZAR_ESTOQUE_PRODUTO(
    1,                         -- p_id_estoque_upd
    'Novo Tipo Estoque X',     -- p_tipo_estoque_upd
    1500,                      -- p_qtde_estoque_upd
    101,                       -- p_id_produto_upd
    'Cadeira Gamer Pro',       -- p_nome_produto_upd
    799.99,                    -- p_preco_produto_upd
    1,                         -- p_fk_id_estoque_upd (vinculando ao estoque atualizado, por exemplo)
    'Cadeira ergonômica com ajuste total', -- p_desc_produto_upd
    'NF-CADEIRA-002'           -- p_numero_nf_produto_upd
);