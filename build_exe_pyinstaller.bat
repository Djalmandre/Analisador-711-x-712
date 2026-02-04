@echo off
echo ========================================
echo Criando executavel do App 711/712
echo ========================================
echo.

echo [1/4] Atualizando pip...
python.exe -m pip install --upgrade pip

echo.
echo [2/4] Instalando dependencias...
pip install -r requirements_exe.txt

echo.
echo [3/4] Criando executavel com PyInstaller...
pyinstaller --onefile --windowed --name="App_711_712" ^
--add-data "logo_petrobras.png;." ^
--add-data "logo jsl.png;." ^
--hidden-import=streamlit ^
--hidden-import=pandas ^
--hidden-import=openpyxl ^
--hidden-import=PIL ^
--collect-all streamlit ^
app_711_712.py

echo.
echo [4/4] Limpando arquivos temporarios...
rmdir /s /q build
del App_711_712.spec

echo.
echo ========================================
echo Executavel criado na pasta "dist"!
echo Arquivo: dist\App_711_712.exe
echo ========================================
pause