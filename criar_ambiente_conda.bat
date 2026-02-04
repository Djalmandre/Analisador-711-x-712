@echo off
echo ========================================
echo Criando Ambiente Conda para App 711/712
echo ========================================
echo.

echo [1/3] Criando ambiente virtual...
conda create -n app_711_712 python=3.11 -y

echo.
echo [2/3] Ativando ambiente...
call conda activate app_711_712

echo.
echo [3/3] Instalando dependencias...
pip install streamlit pandas openpyxl Pillow

echo.
echo ========================================
echo Ambiente criado com sucesso!
echo ========================================
echo.
echo Para executar o app:
echo 1. conda activate app_711_712
echo 2. streamlit run app_711_712.py
echo.
pause