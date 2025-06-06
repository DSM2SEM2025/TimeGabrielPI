from model.produtos_model.produtos_model import (
    CADASTRAR_PRODUTO_ESTOQUE,
    PROCURAR_PRODUTO_ID,
    ATUALIZAR_PRODUTO,
    EXCLUIR_PRODUTO_GERAL,
    LISTAR_PRODUTOS
)

def insert_produto_controller(NOME_PRODUTO, PRECO_PRODUTO, DESC_PRODUTO, TIPO_PRODUTO, QTDE_ESTOQUE):
    return CADASTRAR_PRODUTO_ESTOQUE(NOME_PRODUTO, PRECO_PRODUTO, DESC_PRODUTO, TIPO_PRODUTO, QTDE_ESTOQUE)


def delete_produto_controller(id_produto: int):
    validation, resultado = PROCURAR_PRODUTO_ID(id_produto)
    if validation:
        return EXCLUIR_PRODUTO_GERAL(id_produto)
    else:
        return (False, resultado)


def update_produto_controller(NOME_PRODUTO, PRECO_PRODUTO, DESC_PRODUTO, TIPO_ESTOQUE, QTDE_ESTOQUE, TIPO_ATUALIZACAO):
    validation, _ = PROCURAR_PRODUTO_ID(NOME_PRODUTO)
    
    return ATUALIZAR_PRODUTO(NOME_PRODUTO, PRECO_PRODUTO, DESC_PRODUTO, TIPO_ESTOQUE, QTDE_ESTOQUE, TIPO_ATUALIZACAO)


def search_produto_controller(ID_PRODUTO):
    validation, resultado = PROCURAR_PRODUTO_ID(ID_PRODUTO)
    return resultado  # Não há necessidade de condicional se ambos os caminhos retornam o mesmo valor


def list_produto_estoque():
    return LISTAR_PRODUTOS()


# Exemplo de teste (descomente para usar)
# print(search_produto_controller(1))