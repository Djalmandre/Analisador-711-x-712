@echo off
echo ========================================
echo Criando executavel do App 711/712
echo ========================================
echo.

echo Instalando dependencias...
pip install -r requirements.txt
pip install cx_Freeze

echo.
echo Criando executavel...
python setup.py build

echo.
echo ========================================
echo Executavel criado na pasta "build"!
echo ========================================
pause