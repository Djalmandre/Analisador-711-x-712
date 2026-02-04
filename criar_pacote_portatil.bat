@echo off
echo ========================================
echo Criando Pacote Portatil do App 711/712
echo ========================================
echo.

echo [1/3] Criando estrutura de pastas...
mkdir App_711_712_Portatil
mkdir App_711_712_Portatil\python
mkdir App_711_712_Portatil\app

echo.
echo [2/3] Baixando Python Embeddable...
echo Acesse: https://www.python.org/downloads/windows/
echo Baixe: "Windows embeddable package (64-bit)"
echo Extraia na pasta: App_711_712_Portatil\python
echo.
pause

echo.
echo [3/3] Copiando arquivos da aplicacao...
copy app_711_712.py App_711_712_Portatil\app\
copy "logo_petrobras.png" App_711_712_Portatil\app\
copy "logo jsl.png" App_711_712_Portatil\app\
copy requirements.txt App_711_712_Portatil\app\

echo.
echo Criando script de instalacao de dependencias...
(
echo @echo off
echo echo Instalando dependencias...
echo ..\python\python.exe -m pip install --upgrade pip
echo ..\python\python.exe -m pip install -r requirements.txt
echo echo.
echo echo Dependencias instaladas!
echo pause
) > App_711_712_Portatil\app\instalar_dependencias.bat

echo.
echo Criando script de execucao...
(
echo @echo off
echo echo ========================================
echo echo   App 711/712 - Movimentos SAP
echo echo ========================================
echo echo.
echo echo Iniciando aplicacao...
echo echo O navegador abrira automaticamente.
echo echo.
echo cd app
echo ..\python\python.exe -m streamlit run app_711_712.py
echo pause
) > App_711_712_Portatil\EXECUTAR_APP.bat

echo.
echo ========================================
echo Pacote portatil criado!
echo Pasta: App_711_712_Portatil
echo ========================================
echo.
echo PROXIMOS PASSOS:
echo 1. Baixe Python Embeddable em:
echo    https://www.python.org/ftp/python/3.11.8/python-3.11.8-embed-amd64.zip
echo 2. Extraia na pasta: App_711_712_Portatil\python
echo 3. Execute: App_711_712_Portatil\app\instalar_dependencias.bat
echo 4. Execute: App_711_712_Portatil\EXECUTAR_APP.bat
echo.
pause