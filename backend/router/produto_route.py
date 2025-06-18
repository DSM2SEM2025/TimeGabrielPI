from fastapi import APIRouter, HTTPException, Depends,status # Ferramentas do FastAPI para criar rotas, lidar com erros HTTP e gerenciar dependências.
from fastapi.responses import JSONResponse # Para retornar respostas JSON explícitas
from pydantic import BaseModel, Field # Pydantic para criar modelos de dados e validar informações.
from typing import List, Optional # Para definir tipos como listas ou valores que podem ser vazios.
from datetime import date # Para lidar com datas.
from utils.auth import pegar_usuario # Função para pegar o usuário autenticado (segurança).


# Importa as funções de "controller" de produtos, que interagem com a lógica de negócio e o banco.

from controller.produtos_controller.produtos_controller import (
    insert_produto_controller,
    update_produto_controller,
    search_produto_name_controller,
    delete_produto_estoque_controller,
    list_produto_estoque,
    iniciar_coleta_email_controller,
    iniciar_coleta_dados_pdf
)
from model.produtos_model.produtos_model import diminuir_estoque

# Cria um roteador do FastAPI. Ele agrupa rotas relacionadas.
router = APIRouter()

class Produto(BaseModel):
    """
    Modelo: Representa os dados de um produto.
    Atributos:
        nome_produto (str): O nome do produto.
        preco_produto (float): O preço do produto.
        desc_produto (str): Uma descrição detalhada do produto.
        numero_nf_produto (str): O número da nota fiscal do produto.
        validade_produto (date): A data de validade do produto.
        fornecedor_produto (str): O nome do fornecedor do produto.
        qtd_minima_produto (int): Quantidade mínima em estoque antes de alertar.
    """
    nome_produto: str
    preco_produto: float  
    desc_produto: str
    numero_nf_produto:str
    validade_produto: date
    fornecedor_produto: str
    qtd_minima_produto: int

class Estoque(BaseModel):
    """
    Modelo: Representa os dados de estoque de um produto.
    Atributos:
        id_estoque (Optional[int]): ID do estoque (opcional, pode ser gerado automaticamente).
        categoria_estoque (str): Categoria à qual o estoque pertence.
        qtde_estoque (int): A quantidade atual do produto em estoque.
    """
    id_estoque: Optional[int] = None
    categoria_estoque: str
    qtde_estoque: int
    
class ProdutoEstoque(BaseModel):
    """
    Modelo: Combina os modelos Produto e Estoque para operações de cadastro.
    Atributos:
        produto (Produto): Um objeto do tipo Produto.
        estoque (Estoque): Um objeto do tipo Estoque.
    """
    produto: Produto
    estoque: Estoque    

class ProdutoUpdate(BaseModel):
    """
    Modelo: Representa os dados de um produto para atualização (ID obrigatório, outros com padrão).
    Atributos:
        id_produto (int): O ID do produto a ser atualizado (obrigatório).
        nome_produto (str): Novo nome do produto.
        preco_produto (float): Novo preço do produto (padrão 0.0 se não informado).
        desc_produto (str): Nova descrição do produto (padrão vazio se não informado).
        numero_nf_produto (str): Novo número da nota fiscal (padrão vazio se não informado).
        validade_produto (date): Nova data de validade.
        fornecedor_produto (str): Novo fornecedor.
        qtd_minima_produto (int): Nova quantidade mínima.
    """
    id_produto: int
    nome_produto: str
    preco_produto: float = Field(default=0.0)
    desc_produto: str = Field(default="")
    numero_nf_produto: str = Field(default="")
    validade_produto: date
    fornecedor_produto: str
    qtd_minima_produto: int

class EstoqueUpdate(BaseModel):
    """
    Modelo: Representa os dados de estoque para atualização (ID obrigatório).
    Atributos:
        id_estoque (int): O ID do estoque a ser atualizado.
        qtde_estoque (int): Nova quantidade em estoque.
        categoria_estoque (str): Nova categoria do estoque.
    """
    id_estoque: int
    qtde_estoque: int
    categoria_estoque: str
    
class EstoqueCheckout(BaseModel):
    """
    Modelo: Representa os dados para dar baixa no estoque de um produto.
    Atributos:
        id_produto (int): O ID do produto para dar baixa.
        qtde_estoque (int): A quantidade a ser removida do estoque.
    """
    id_produto: int
    qtde_estoque: int

class ProdutoEstoqueUpdate(BaseModel):
    """
    Modelo: Combina os modelos ProdutoUpdate e EstoqueUpdate para operações de atualização.
    Atributos:
        produto (ProdutoUpdate): Um objeto do tipo ProdutoUpdate.
        estoque (EstoqueUpdate): Um objeto do tipo EstoqueUpdate.
    """
    produto: ProdutoUpdate
    estoque: EstoqueUpdate

class ProdutoDelete(BaseModel):
    """
    Modelo: Representa os dados para exclusão de um produto (apenas pelo nome, embora o router use ID).
    Nota: Este modelo parece ser um resquício ou para outro propósito, pois o router 'delete' usa 'id'.
    Atributos:
        nome_produto (str): O nome do produto a ser excluído.
    """
    nome_produto: str

@router.post("/produto", status_code=201)
def cadastrar_produto_router(dados: ProdutoEstoque, usuario=Depends(pegar_usuario)):
    """
    Função: Cadastra um novo produto no estoque.
    Recebe parâmetros:
        dados (ProdutoEstoque): Contém todas as informações do produto e do estoque.
        usuario (Depends): Dependência de segurança para garantir que o usuário está logado.
    Detalhes:
    - Verifica se o produto já existe para evitar duplicatas, mesmo tendo um valor unique no banco.
    - Chama a função `insert_produto_controller` para salvar no banco.
    - Retorna uma mensagem de sucesso ou erro.
    """
    try:
        # Verifica se o produto já existe no sistema para evitar cadastros duplicados.
        produtos = list_produto_estoque()
        if any(p['NOME_PRODUTO'].lower() == dados.produto.nome_produto.lower() for p in produtos):
            raise HTTPException(
                status_code=400,
                detail="Produto já cadastrado. Use a função de atualização para modificar."
            )
        # Chama o controlador para inserir o produto no banco de dados.
        success, message = insert_produto_controller(
            dados.produto.nome_produto,
            dados.estoque.categoria_estoque,
            dados.produto.desc_produto,
            dados.estoque.qtde_estoque,
            dados.produto.preco_produto,
            dados.produto.qtd_minima_produto,
            dados.produto.validade_produto,
            dados.produto.numero_nf_produto,
            dados.produto.fornecedor_produto,
        )
        
        if not success:
            # Se o controlador retornar falha, levanta uma exceção HTTP.
            raise HTTPException(status_code=400, detail=message)
            
        return {"message": "Produto cadastrado com sucesso!"}
    except HTTPException:
        # Propaga exceções HTTPException já levantadas.
        raise
    except Exception as err:
        # Captura qualquer outro erro inesperado e retorna um erro HTTP 400.
        raise HTTPException(status_code=400, detail=str(err))

@router.get("/produto/nome/{nome}")
def search_produto_nome_router(nome: str, usuario=Depends(pegar_usuario)):
    """
    Função: Busca produtos pelo nome.
    Recebe parâmetros:
        nome (str): O nome (ou parte do nome) do produto a ser buscado.
        usuario (Depends): Dependência de segurança.
    Detalhes:
    - Chama `search_produto_name_controller` para buscar no banco.
    - Retorna os produtos encontrados ou um erro 404 se nenhum for achado.
    """
    produto_data = search_produto_name_controller(nome)
    # Se encontrar produtos, retorna uma mensagem de sucesso e os dados.
    if produto_data:
        return {
            "message": "Produtos encontrados",
            "data": produto_data 
        }
    else:
        raise HTTPException(status_code=404, detail="Nenhum produto encontrado com esse nome.")

@router.get("/produto", response_model=List[dict])
#def list_produto_router():
def list_produto_router(usuario=Depends(pegar_usuario)):
    """
    Função: Lista todos os produtos no estoque.
    Recebe parâmetros:
        usuario (Depends): Dependência de segurança.
    Detalhes:
    - Retorna uma lista de dicionários, representando cada produto e seu estoque.
    """
    return list_produto_estoque() # Delega a listagem para a função do controller.


@router.delete("/produto/{id}", status_code=200, summary="Excluir produto pelo ID")
def excluir_produto_router(id: int, usuario=Depends(pegar_usuario)):
    """
    Função: Exclui um produto do estoque pelo seu ID.
    Recebe parâmetros:
        id (int): O ID do produto a ser excluído.
        usuario (Depends): Dependência de segurança.
    Detalhes:
    - Chama `delete_produto_estoque_controller` para realizar a exclusão.
    - Retorna sucesso ou um erro 404 se o produto não for encontrado ou não puder ser excluído.
    """
    result = delete_produto_estoque_controller(id) # Tenta excluir o produto.
    if result[0]:  # result[0] é o status de sucesso (True/False)
        return {"message": f"Produto com ID '{id}' excluído com sucesso."}
    else:
        # Se houver um erro, levanta uma exceção HTTP 404 com a mensagem de erro.
        raise HTTPException(status_code=404, detail=result[1])

@router.put("/produto")
def atualizar_produto_router(dados: ProdutoEstoqueUpdate, usuario=Depends(pegar_usuario)):
    """
    Função: Atualiza as informações de um produto e/ou seu estoque.
    Recebe parâmetros:
        dados (ProdutoEstoqueUpdate): Contém os IDs e os novos dados do produto e estoque.
        usuario (Depends): Dependência de segurança.
    Detalhes:
    - Recebe dados do produto e estoque para atualização.
    - Chama `update_produto_controller` para aplicar as mudanças no banco.
    - Retorna uma mensagem de sucesso ou erro.
    """
    try:
        # Chama a função controladora para atualizar o produto e estoque.
        success, message = update_produto_controller(
            dados.estoque.id_estoque,
            dados.estoque.categoria_estoque,
            dados.estoque.qtde_estoque,
            dados.produto.id_produto,
            dados.produto.nome_produto,
            dados.produto.preco_produto,
            dados.produto.desc_produto,
            dados.produto.numero_nf_produto,
            dados.produto.validade_produto,
            dados.produto.fornecedor_produto,
            dados.produto.qtd_minima_produto
        )
        
        if not success:
            # Se a atualização não for bem-sucedida, levanta uma exceção HTTP.
            raise HTTPException(status_code=400, detail=message)
            
        return {"message": "Produto atualizado com sucesso."}
    except Exception as err:
        # Captura qualquer erro e retorna um erro HTTP 400.
        raise HTTPException(status_code=400, detail=str(err))

# @router.get("/coleta-email", summary="Coleta dados de e-mails do Gmail com anexos PDF")
# def coleta_email_router(usuario=Depends(pegar_usuario)):
#     """
#     Função: Inicia o processo de coleta de dados de e-mails (para, por exemplo, notas fiscais).
#     Recebe parâmetros:
#         usuario (Depends): Dependência de segurança.
#     Detalhes:
#     - Chama `iniciar_coleta_email_controller` para começar a coleta.
#     - Retorna uma mensagem sobre o status da coleta.
#     """
#     try:
#         result = iniciar_coleta_email_controller() # Inicia a coleta de e-mails.
#         return {"message": "Coleta de e-mail concluída", "resultado": str(result)}
#     except Exception as e:
#         # Se houver erro na coleta, levanta uma exceção HTTP 500.
#         raise HTTPException(status_code=500, detail=f"Erro na coleta de e-mails: {e}")
    
@router.post("/estoque/atualizar")
def atualizar_estoque(dados: EstoqueCheckout, usuario=Depends(pegar_usuario)):
    """
    Função: Atualiza o estoque de um produto (diminuindo a quantidade).
    Recebe parâmetros:
        dados (EstoqueCheckout): Contém o ID do produto e a quantidade a ser diminuída.
        usuario (Depends): Dependência de segurança.
    Detalhes:
    - Usa a função `diminuir_estoque` para dar baixa na quantidade.
    - Retorna uma mensagem de sucesso ou erro.
    """
    success, msg = diminuir_estoque(dados.id_produto, dados.qtde_estoque) # Diminui o estoque.
    if success: # Retorna sucesso.
        return {"message": "Estoque atualizado"}
    else:
        # Se a atualização falhar, levanta uma exceção HTTP 400.
        raise HTTPException(status_code=400, detail=msg)

@router.post("/produtos/saida")
def registrar_saida(produto_id: int, quantidade: int):
    sucesso, mensagem = diminuir_estoque(produto_id, quantidade)
    if sucesso:
        return {"mensagem": mensagem}
    else:
        raise HTTPException(status_code=400, detail=mensagem)
    


@router.get("/coletar-emails", summary="Inicia a coleta e download de anexos de e-mails.", status_code=status.HTTP_200_OK)
async def coletar_emails_router(usuario=Depends(pegar_usuario)): 
    """
    função para iniciar o processo de coleta e download de anexos de e-mails.
    Requer autenticação de usuário.
    """
    print("Requisição recebida para /coletar-emails")
    try:
        # Chama a função síncrona do controller.
        success, count = iniciar_coleta_email_controller() 
        
        if success:
            return JSONResponse(content={
                "status": "sucesso",
                "mensagem": f"{count} PDFs baixados com sucesso (se aplicável).",
                "pdfs_baixados": count,
                "usuario_autenticado": usuario.get('email', 'N/A') # Exemplo de retorno do usuário
            }, status_code=status.HTTP_200_OK)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Falha na coleta de e-mails. Verifique os logs do servidor para mais detalhes."
            )
    except Exception as e:
        print(f"Erro no endpoint /coletar-emails: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro interno inesperado: {str(e)}"
        )


@router.post("/processar-pdfs", summary="Inicia o processo de extração e cadastro de dados dos PDFs baixados.", status_code=status.HTTP_200_OK)
async def processar_pdfs_router(usuario=Depends(pegar_usuario)):
    """
    funçaõ para iniciar o processo de leitura de arquivos PDF baixados,
    extração de dados de produtos e tentativa de cadastro no banco de dados.
    
    Requer autenticação de usuário.
    """
    print("Requisição recebida para /processar-pdfs")
    try:
        # Chama a função síncrona do controller.
        # FastAPI a executará em um thread pool.
        all_processed_data = iniciar_coleta_dados_pdf() 
        
        if all_processed_data is not None: # Verifica se não houve erro grave antes de retornar []
            if len(all_processed_data) > 0:
                return JSONResponse(content={
                    "status": "sucesso",
                    "mensagem": f"{len(all_processed_data)} PDFs processados. Verifique os logs para status de cadastro.",
                    "detalhes_processamento": all_processed_data, # Pode retornar os dados extraídos
                    "usuario_autenticado": usuario.get('email', 'N/A')
                }, status_code=status.HTTP_200_OK)
            else:
                return JSONResponse(content={
                    "status": "info",
                    "mensagem": "Nenhum PDF encontrado no diretório ou nenhum dado extraído para processamento."
                }, status_code=status.HTTP_200_OK)
        else:
             raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno ao iniciar o processamento de PDFs. Verifique os logs."
            )

    except Exception as e:
        print(f"Erro no endpoint /processar-pdfs: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro interno inesperado: {str(e)}"
        )