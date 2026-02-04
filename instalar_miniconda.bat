@echo off
chcp 65001 >nul
echo ========================================
echo   Instalador Automático do Miniconda
echo   Para App 711/712
echo ========================================
echo.

echo [1/3] Baixando Miniconda3...
echo Isso pode levar alguns minutos...
echo.

powershell -Command "& {Invoke-WebRequest -Uri 'https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe' -OutFile 'Miniconda3-Installer.exe'}"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERRO] Falha ao baixar Miniconda.
    echo.
    echo Baixe manualmente em:
    echo https://docs.conda.io/en/latest/miniconda.html
    echo.
    pause
    exit /b 1
)

echo.
echo [2/3] Instalando Miniconda...
echo.
echo ATENÇÃO: 
echo - Aceite o contrato de licença
echo - Instale para "Just Me"
echo - Marque "Add Miniconda3 to PATH"
echo.
pause

start /wait Miniconda3-Installer.exe /InstallationType=JustMe /AddToPath=1 /RegisterPython=0 /S

echo.
echo [3/3] Limpando arquivos temporários...
del Miniconda3-Installer.exe

echo.
echo ========================================
echo   Miniconda Instalado!
echo ========================================
echo.
echo IMPORTANTE: Feche e reabra o Prompt de Comando
echo.
echo Depois execute: criar_instalador_conda.bat
echo.
pause