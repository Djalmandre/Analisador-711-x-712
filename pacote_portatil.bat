@echo off
chcp 65001 >nul
echo ========================================
echo   Criando Pacote Portátil
echo   App 711/712 - Movimentos SAP
echo ========================================
echo.

REM Criar estrutura de pastas
echo [1/5] Criando estrutura de pastas...
if exist App_711_712_Portatil rmdir /s /q App_711_712_Portatil
mkdir App_711_712_Portatil
mkdir App_711_712_Portatil\python_embed
mkdir App_711_712_Portatil\app
mkdir App_711_712_Portatil\dados

echo.
echo [2/5] Baixando Python Embeddable 3.11.8...
echo.

REM Baixar Python Embeddable usando PowerShell
powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.8/python-3.11.8-embed-amd64.zip' -OutFile 'python_embed.zip'}"

echo.
echo [3/5] Extraindo Python Embeddable...
powershell -Command "& {Expand-Archive -Path 'python_embed.zip' -DestinationPath 'App_711_712_Portatil\python_embed' -Force}"
del python_embed.zip

echo.
echo [4/5] Baixando get-pip.py...
powershell -Command "& {Invoke-WebRequest -Uri 'https://bootstrap.pypa.io/get-pip.py' -OutFile 'App_711_712_Portatil\python_embed\get-pip.py'}"

echo.
echo [5/5] Configurando Python Embeddable...
REM Remover import site comentado para permitir pip
powershell -Command "(Get-Content 'App_711_712_Portatil\python_embed\python311._pth') -replace '#import site', 'import site' | Set-Content 'App_711_712_Portatil\python_embed\python311._pth'"

echo.
echo Copiando arquivos da aplicação...
copy app_711_712.py App_711_712_Portatil\app\
copy "logo_petrobras.png" App_711_712_Portatil\app\ 2>nul
copy "logo petrobras.png" App_711_712_Portatil\app\ 2>nul
copy "logo_jsl.png" App_711_712_Portatil\app\ 2>nul
copy "logo jsl.png" App_711_712_Portatil\app\ 2>nul

echo.
echo Criando requirements.txt...
(
echo streamlit==1.32.0
echo pandas==2.2.0
echo openpyxl==3.1.2
echo Pillow==10.2.0
) > App_711_712_Portatil\app\requirements.txt

echo.
echo Criando script de instalação de dependências...
(
echo @echo off
echo chcp 65001 ^>nul
echo echo ========================================
echo echo   Instalando Dependências
echo echo   App 711/712
echo echo ========================================
echo echo.
echo cd /d "%%~dp0"
echo echo [1/3] Instalando pip...
echo python_embed\python.exe python_embed\get-pip.py
echo echo.
echo echo [2/3] Atualizando pip...
echo python_embed\python.exe -m pip install --upgrade pip
echo echo.
echo echo [3/3] Instalando dependências da aplicação...
echo python_embed\python.exe -m pip install -r app\requirements.txt
echo echo.
echo echo ========================================
echo echo   Instalação concluída com sucesso!
echo echo ========================================
echo echo.
echo echo Agora você pode executar o app clicando em:
echo echo EXECUTAR_APP.bat
echo echo.
echo pause
) > App_711_712_Portatil\INSTALAR_DEPENDENCIAS.bat

echo.
echo Criando script de execução do app...
(
echo @echo off
echo chcp 65001 ^>nul
echo cls
echo echo ========================================
echo echo   App 711/712 - Movimentos SAP
echo echo   Desenvolvido por Djalma A Barbosa
echo echo ========================================
echo echo.
echo cd /d "%%~dp0"
echo echo Iniciando aplicação...
echo echo.
echo echo O navegador será aberto automaticamente.
echo echo Para encerrar, feche esta janela.
echo echo.
echo cd app
echo ..\python_embed\python.exe -m streamlit run app_711_712.py
echo pause
) > App_711_712_Portatil\EXECUTAR_APP.bat

echo.
echo Criando arquivo LEIA-ME.txt...
(
echo ========================================
echo   App 711/712 - Movimentos SAP
echo   Versão Portátil 1.0
echo ========================================
echo.
echo INSTRUÇÕES DE USO:
echo.
echo 1. PRIMEIRA VEZ - Instalação:
echo    - Execute: INSTALAR_DEPENDENCIAS.bat
echo    - Aguarde a instalação completar
echo    - Isso precisa ser feito apenas UMA VEZ
echo.
echo 2. EXECUTAR O APP:
echo    - Execute: EXECUTAR_APP.bat
echo    - O navegador abrirá automaticamente
echo    - Faça upload do arquivo Excel
echo    - Use as funcionalidades do app
echo.
echo 3. SEUS DADOS:
echo    - Coloque seus arquivos Excel na pasta "dados"
echo    - Ou faça upload direto pelo app
echo.
echo FUNCIONALIDADES:
echo    - Busca de Movimentos 711/712
echo    - Análise de Materiais Duplicados
echo    - 5 Temas de Aparência
echo    - Exportação para Excel
echo.
echo REQUISITOS:
echo    - Windows 10 ou superior
echo    - Navegador web moderno
echo    - Conexão com internet ^(primeira instalação^)
echo.
echo SUPORTE:
echo    Desenvolvido por Djalma A Barbosa - 2026
echo    Todos os direitos reservados ®
echo.
) > App_711_712_Portatil\LEIA-ME.txt

echo.
echo ========================================
echo   Pacote Portátil Criado com Sucesso!
echo ========================================
echo.
echo Pasta criada: App_711_712_Portatil
echo.
echo PRÓXIMOS PASSOS:
echo 1. Compacte a pasta "App_711_712_Portatil" em ZIP
echo 2. Distribua o arquivo ZIP
echo 3. O usuário deve:
echo    a) Extrair o ZIP
echo    b) Executar: INSTALAR_DEPENDENCIAS.bat
echo    c) Executar: EXECUTAR_APP.bat
echo.
echo Tamanho aproximado: 50-80 MB
echo.
pause