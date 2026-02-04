@echo off
chcp 65001 >nul
echo ========================================
echo   Instalador Conda
echo   App 711/712 - Movimentos SAP
echo ========================================
echo.

REM Verificar se conda está instalado
where conda >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERRO] Conda não encontrado!
    echo.
    echo Por favor, instale o Miniconda primeiro:
    echo https://docs.conda.io/en/latest/miniconda.html
    echo.
    echo Ou execute: instalar_miniconda.bat
    echo.
    pause
    exit /b 1
)

echo [1/6] Conda encontrado!
conda --version
echo.

echo [2/6] Removendo ambiente anterior (se existir)...
call conda env remove -n app_711_712 -y 2>nul
echo.

echo [3/6] Criando novo ambiente Python 3.11...
call conda create -n app_711_712 python=3.11 -y
echo.

echo [4/6] Ativando ambiente...
call conda activate app_711_712
echo.

echo [5/6] Instalando dependências...
pip install streamlit==1.32.0 pandas==2.2.0 openpyxl==3.1.2 Pillow==10.2.0
echo.

echo [6/6] Criando atalhos de execução...

REM Criar atalho para executar o app
(
echo @echo off
echo chcp 65001 ^>nul
echo cls
echo echo ========================================
echo echo   App 711/712 - Movimentos SAP
echo echo   Desenvolvido por Djalma A Barbosa
echo echo ========================================
echo echo.
echo call conda activate app_711_712
echo if %%ERRORLEVEL%% NEQ 0 ^(
echo     echo [ERRO] Não foi possível ativar o ambiente conda.
echo     echo Execute novamente: criar_instalador_conda.bat
echo     pause
echo     exit /b 1
echo ^)
echo echo.
echo echo Iniciando aplicação...
echo echo O navegador será aberto automaticamente.
echo echo.
echo echo Para encerrar, feche esta janela ou pressione Ctrl+C
echo echo.
echo streamlit run app_711_712.py
) > EXECUTAR_APP_CONDA.bat

REM Criar atalho para atualizar dependências
(
echo @echo off
echo chcp 65001 ^>nul
echo echo ========================================
echo echo   Atualizando Dependências
echo echo   App 711/712
echo echo ========================================
echo echo.
echo call conda activate app_711_712
echo echo.
echo echo Atualizando pacotes...
echo pip install --upgrade streamlit pandas openpyxl Pillow
echo echo.
echo echo ========================================
echo echo   Atualização concluída!
echo echo ========================================
echo pause
) > ATUALIZAR_DEPENDENCIAS.bat

REM Criar script de desinstalação
(
echo @echo off
echo chcp 65001 ^>nul
echo echo ========================================
echo echo   Desinstalar App 711/712
echo echo ========================================
echo echo.
echo echo ATENÇÃO: Isso removerá o ambiente conda completo.
echo echo.
echo set /p confirma="Deseja continuar? (S/N): "
echo if /i "%%confirma%%"=="S" ^(
echo     echo.
echo     echo Removendo ambiente...
echo     call conda env remove -n app_711_712 -y
echo     echo.
echo     echo Ambiente removido com sucesso!
echo     echo.
echo     echo Você pode deletar os arquivos do app manualmente.
echo ^) else ^(
echo     echo.
echo     echo Operação cancelada.
echo ^)
echo echo.
echo pause
) > DESINSTALAR_APP.bat

REM Criar documentação
(
echo ========================================
echo   App 711/712 - Movimentos SAP
echo   Instalação via Conda
echo ========================================
echo.
echo INSTALAÇÃO CONCLUÍDA COM SUCESSO!
echo.
echo COMO USAR:
echo.
echo 1. EXECUTAR O APP:
echo    - Clique em: EXECUTAR_APP_CONDA.bat
echo    - O navegador abrirá automaticamente
echo.
echo 2. ATUALIZAR DEPENDÊNCIAS:
echo    - Clique em: ATUALIZAR_DEPENDENCIAS.bat
echo.
echo 3. DESINSTALAR:
echo    - Clique em: DESINSTALAR_APP.bat
echo.
echo COMANDOS MANUAIS (Opcional):
echo.
echo    Ativar ambiente:
echo    conda activate app_711_712
echo.
echo    Executar app:
echo    streamlit run app_711_712.py
echo.
echo    Desativar ambiente:
echo    conda deactivate
echo.
echo FUNCIONALIDADES DO APP:
echo    - Busca de Movimentos 711/712
echo    - Análise de Materiais Duplicados
echo    - 5 Temas de Aparência
echo    - Relógio Digital
echo    - Exportação para Excel
echo.
echo REQUISITOS:
echo    - Windows 10 ou superior
echo    - Miniconda/Anaconda instalado
echo    - Navegador web moderno
echo.
echo DESENVOLVIDO POR:
echo    Djalma A Barbosa - 2026
echo    Todos os direitos reservados ®
echo.
) > LEIA-ME_CONDA.txt

echo.
echo ========================================
echo   Instalação Concluída com Sucesso!
echo ========================================
echo.
echo Ambiente conda criado: app_711_712
echo.
echo ARQUIVOS CRIADOS:
echo    - EXECUTAR_APP_CONDA.bat
echo    - ATUALIZAR_DEPENDENCIAS.bat
echo    - DESINSTALAR_APP.bat
echo    - LEIA-ME_CONDA.txt
echo.
echo PRÓXIMO PASSO:
echo    Execute: EXECUTAR_APP_CONDA.bat
echo.
type LEIA-ME_CONDA.txt
echo.
pause