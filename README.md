
# 📦 Sistema de Gerenciamento de Estoque Fullstack

Projeto completo com frontend em Vue.js e backend em FastAPI, com integração a banco de dados MySQL, autenticação via JWT e comunicação em tempo real via WebSocket.

---

## 🧰 Tecnologias Utilizadas

### 🔹 Front-End

- **Vue.js 3** — Framework progressivo para construção de interfaces web reativas  
- **Vue Router** — Gerenciamento de rotas SPA (Single Page Application)  
- **Tailwind CSS** — Framework utilitário para estilização com classes CSS  
- **Heroicons** — Biblioteca de ícones SVG compatível com Tailwind  
- **Vite** — Ferramenta de build e bundler moderna para Vue.js  
- **Axios** — Cliente HTTP usado para comunicação com o backend  
- **EventBus (Vue)** — Comunicação entre componentes independentes  

### 🔸 Back-End

- **Python 3.x** — Linguagem principal do servidor  
- **FastAPI** — Framework web assíncrono e rápido para criação de APIs REST e WebSocket  
- **Uvicorn** — Servidor ASGI usado para executar a aplicação FastAPI  
- **Starlette** — Toolkit assíncrono que serve de base para o FastAPI (middlewares, WebSockets, etc.)  
- **MySQL** — Banco de dados relacional usado para persistência dos dados  
- **MySQL Connector (mysql-connector-python)** — Driver oficial para conectar Python ao MySQL  

### 🔐 Autenticação e Segurança

- **python-jose** — Geração e verificação de tokens JWT  
- **PyJWT** — Manipulação de JWTs (token de autenticação)  
- **itsdangerous** — Geração de tokens seguros para sessão e validação  
- **email-validator** — Validação de e-mails no backend  
- **cryptography / rsa / ecdsa** — Suporte para operações criptográficas  

### 🧾 Manipulação de PDFs

- **pdfplumber** — Leitura e extração de texto de arquivos PDF  
- **pdfminer.six** — Biblioteca base usada para interpretar PDFs  
- **pypdfium2** — Renderização e manipulação de arquivos PDF  
- **Pillow** — Manipulação de imagens (usado em conjunto com PDFs)  

### 🔄 Comunicação em Tempo Real

- **websockets** — Comunicação via WebSocket (dashboard, atualizações em tempo real)  
- **FastAPI WebSocket** — Rotas específicas para conexões WebSocket  

### ⚙️ Utilitários e Outros

- **python-dotenv** — Leitura de variáveis de ambiente do arquivo `.env`  
- **Pydantic** — Validação de dados e criação de modelos (base do FastAPI)  
- **Watchfiles** — Recarga automática da aplicação durante desenvolvimento  
- **SessionMiddleware** — Controle de sessão no backend com cookies  
- **CORS Middleware** — Liberação de requisições do frontend (`localhost:5173`)  

---

## 📁 Estrutura do Projeto

### Frontend (`/frontend`)

```
frontend/
└── src/
    ├── main.js                 # Arquivo principal da aplicação (ponto de entrada)
    ├── App.vue                 # Componente raiz
    ├── assets/                 # Arquivos estáticos (imagens, ícones, etc.)
    │
    ├── components/             # Componentes reutilizáveis
    │   ├── layout/             # Componentes de layout (Nav-bar, Sidebar)
    │   └── ui/                 # Componentes de interface (botões, inputs, etc.)
    │
    ├── composables/            # Composables (lógica reutilizável com Composition API)
    ├── pages/                  # Páginas da aplicação (Cadastro.vue, Login.vue, etc.)
    ├── router/                 # Configuração de rotas com Vue Router
    └── services/               # Serviços responsáveis por comunicação e lógica externa
        ├── api.js              # Configuração e funções de chamadas HTTP (Axios) para o backend
        └── eventBus.js         # Canal de comunicação entre componentes usando Event Bus (Vue.js)
```

### Backend (`/backend`)

## 📁 Estrutura do Backend

```
backend/
├── main.py                          # Ponto de entrada da aplicação FastAPI
├── req.txt e req2.txt               # Arquivos com as dependências do projeto
├── db_setup.py                      # Script para criação do banco e tabelas
│
├── controller/                      # Camada de controle (regras de negócio)
│   ├── dashboard_controller/
│   │   └── dashboard_controller.py  # Controlador de dados do dashboard
│   ├── produtos_controller/
│   │   └── produtos_controller.py   # Controlador para produtos
│   └── usuarios_controller/
│       └── usuarios_controller.py  # Controlador para usuários
│
├── database/                        # Configuração de banco de dados
│   ├── db_model.py                  # Carrega variáveis de ambiente do .env
│   ├── db_mysql.py                  # Conexão com banco de dados MySQL
│   ├── test_db.py                   # Teste de conexão com o banco
│   ├── sql/                         # Scripts SQL (procedures, criação de tabelas)
│   └── .env                         # Variáveis de ambiente (.env)
│
├── model/                           # Camada de modelos de dados
│   ├── produtos_model/
│   │   ├── modules_produtos_model/ 
│   │   │   ├── email_data_extractor.py   # Extração de e-mails de PDFs
│   │   │   ├── get_env_email.py          # Lê configurações de e-mail do .env
│   │   │   └── pdf_reader.py             # Leitura de PDFs
│   │   ├── notificacao_model.py          # Modelo de notificações
│   │   └── produtos_model.py             # Modelo principal de produto
│   └── usuarios_model/
│       └── usuarios_model.py             # Modelo principal de usuário
│
├── router/                          # Definição das rotas da API
│   ├── dashboard_router.py          # Rotas relacionadas ao dashboard
│   ├── notificacao_router.py        # Rotas para envio de notificações
│   ├── produto_route.py             # Rotas para produtos
│   ├── usuarios_router.py           # Rotas para usuários
│   └── ws_router.py                 # Rota para WebSocket (tempo real)
│
└── utils/                           # Funções auxiliares reutilizáveis
    ├── auth.py                      # Utilitários de autenticação/autorização
    └── pdf_data/                    # Manipulação de dados de PDF
```

## 🚀 Instalação do Projeto

Este projeto possui backend (FastAPI + Python) e frontend (Vue.js + Vite) integrados e configurados para rodar juntos com um único comando via `setup.bat`.

### Pré-requisitos

- [Python 3.x](https://www.python.org/downloads/)
- [Node.js + NPM](https://nodejs.org/)
- [Git](https://git-scm.com/)
- [MySQL](https://dev.mysql.com/downloads/installer/)

---

### 🔧 Passos para Executar

1. Clone o repositório:

```bash
git clone https://github.com/DSM2SEM2025/TimeGabrielPI.git
```

2. Acesse a pasta do projeto:

```bash
cd TimeGabrielPI
```

3. Execute o script de setup:

```bash
.\setup.bat
```

Esse script realiza automaticamente:

- Criação e ativação de ambiente virtual do Python
- Instalação de dependências do backend (`req.txt` e `req2.txt`)
- Instalação de dependências do frontend (`npm install`)
- Inicialização simultânea do backend e do frontend

---

## 🖥️ Acesso à Aplicação

- Frontend: [http://localhost:5173](http://localhost:5173)  
- Backend (API): [http://localhost:8000](http://localhost:8000)

---

## 🔐 Configuração do Banco de Dados

Antes de executar a aplicação, certifique-se de configurar corretamente o arquivo `.env` localizado na pasta `backend/database`.

Abra o arquivo `.env` e **substitua a senha padrão pelo valor correto da sua instalação do MySQL**:

```env
user=root
password=SuaSenhaAqui  # Altere para a senha real do seu MySQL
host=localhost
database=db
port=3306
sid=None
VITE_API_URL=http://localhost:8000
```

---

## 📦 Gerar Build de Produção

Se desejar gerar a versão de produção do frontend:

```bash
cd frontend
npm run build
npm run preview
```

---

## 👥 Desenvolvedores

- Allan Martins Silva (https://github.com/allanmsilva23) — Desenvolvedor Back-end  
- Gabriel Marques da Silva (https://github.com/the-gabriel-marques) — Desenvolvedor Back-end
- Heitor Augusto de Carvalho Silva (https://github.com/HeitorAugustoC) — Desenvolvedor Back-end
- Jhon Deyvid Quispe Mamani (https://github.com/d-Jhon-b) - Desenvolvedor Back-end
- Pedro Henrique de Carvalho Silva (https://github.com/Bruxx092) - Desenvolvedor Front-end
- Roberto Tadashi Miura (https://github.com/RobertoFATEC24) - Desenvolvedor Front-end
- Vitor Luiz Soares da Silva (https://github.com/VitorVraal) - Desenvolvedor Front-end
