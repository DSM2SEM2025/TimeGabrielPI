from model.produtos_model.produtos_model import (
    CADASTRAR_PRODUTO_ESTOQUE,
    PROCURAR_PRODUTO_ID,
    ATUALIZAR_PRODUTO,
    EXCLUIR_PRODUTO_GERAL,
    LISTAR_PRODUTOS,
    coleta_de_dados_email
)

def insert_produto_controller(NOME_PRODUTO, PRECO_PRODUTO, DESC_PRODUTO,
                              NUMERO_NF_PRODUTO, VALIDADE_PRODUTO, FORNECEDOR_PRODUTO,
                              QTD_MINIMA_PRODUTO, CATEGORIA_ESTOQUE, QTDE_ESTOQUE):
    return CADASTRAR_PRODUTO_ESTOQUE(NOME_PRODUTO, PRECO_PRODUTO, DESC_PRODUTO,
                                     NUMERO_NF_PRODUTO, VALIDADE_PRODUTO, FORNECEDOR_PRODUTO,
                                     QTD_MINIMA_PRODUTO, CATEGORIA_ESTOQUE, QTDE_ESTOQUE)

def delete_produto_estoque_controller(id_estoque: int):
    # validation, resultado = PROCURAR_PRODUTO_ID(id_produto)
    # if validation:
    #     return EXCLUIR_PRODUTO_GERAL(id_produto)
    # else:
    #     return (False, resultado)
    return EXCLUIR_PRODUTO_GERAL(id_estoque)
    


def update_produto_controller(p_id_estoque_upd=None,p_categoria_estoque_upd=None,p_qtde_estoque_upd=None,     
        p_id_produto_upd=None,       
        p_nome_produto_upd=None,     
        p_preco_produto_upd=None,    
        p_fk_id_estoque_upd=None,    
        p_desc_produto_upd=None,     
        p_numero_nf_produto_upd=None,
        p_validade_produto_upd=None,
        p_fornecedor_produto_upd=None,
        p_qtd_minima_produto_upd=None
    ):    
    return ATUALIZAR_PRODUTO(p_id_estoque_upd,
            p_categoria_estoque_upd,
            p_qtde_estoque_upd,
            p_id_produto_upd,
            p_nome_produto_upd,
            p_preco_produto_upd,
            p_fk_id_estoque_upd,
            p_desc_produto_upd,
            p_numero_nf_produto_upd,
            p_validade_produto_upd,
            p_fornecedor_produto_upd,
            p_qtd_minima_produto_upd)

# print(update_produto_controller(2, "teste novo estoque", 2000))


def search_produto_controller(ID_PRODUTO):
    validation, resultado = PROCURAR_PRODUTO_ID(ID_PRODUTO)
    return resultado  # Não há necessidade de condicional se ambos os caminhos retornam o mesmo valor


def list_produto_estoque():
    return LISTAR_PRODUTOS()

# Exemplo de teste (descomente para usar)
# print(search_produto_controller(1))


def iniciar_coleta_email_controller():
    return coleta_de_dados_email()
