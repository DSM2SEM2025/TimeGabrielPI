@echo off
title Setup do Projeto - Fullstack

echo ======== Criando ambiente virtual do backend ========
cd backend
python -m venv venv

echo ======== Ativando ambiente virtual e instalando dependências do backend ========
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r req.txt
python -m pip install -r req2.txt
cd ..

echo ======== Instalando dependências do frontend ========
cd frontend
call npm install
cd ..

echo ======== Iniciando o backend ========
start cmd /k "cd backend && call venv\Scripts\activate.bat && uvicorn main:app --reload"

echo ======== Iniciando o frontend ========
start cmd /k "cd frontend && npm run dev"

echo ======== Tudo pronto! Backend e frontend estão rodando. ========
pause
