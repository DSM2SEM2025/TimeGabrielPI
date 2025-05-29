from model.produtos_model.produtos_model import CADASTRAR_PRODUTO_ESTOQUE, PROCURAR_PRODUTO_ID, ATUALIZAR_PRODUTO, EXCLUIR_PRODUTO_GERAL, LISTAR_PRODUTOS



def insert_produto_controller(NOME_PRODUTO, PRECO_PRODUTO, DESC_PRODUTO, TIPO_PRODUTO, QTDE_ESTOQUE):
    return CADASTRAR_PRODUTO_ESTOQUE(NOME_PRODUTO, PRECO_PRODUTO, DESC_PRODUTO, TIPO_PRODUTO, QTDE_ESTOQUE)


def delete_produto_controller(NOME_PRODUTO):
    
    return EXCLUIR_PRODUTO_GERAL(NOME_PRODUTO)

def update_produto_controller(NOME_PRODUTO, PRECO_PRODUTO, DESC_PRODUTO, TIPO_ESTOQUE, QTDE_ESTOQUE, TIPO_ATUALIZACAO):
    return ATUALIZAR_PRODUTO(NOME_PRODUTO, PRECO_PRODUTO, DESC_PRODUTO, TIPO_ESTOQUE, QTDE_ESTOQUE, TIPO_ATUALIZACAO)

def search_produto_controller(ID_PRODUTO):
    validation, resultado =PROCURAR_PRODUTO_ID(ID_PRODUTO)
    if validation:
        return resultado
    else:
        return resultado

def list_produto_estoque():
    produtos = LISTAR_PRODUTOS()         
    return produtos


# print(search_produto_estoque(1))
