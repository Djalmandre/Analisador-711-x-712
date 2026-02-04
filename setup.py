from cx_Freeze import setup, Executable
import sys

# Dependências
build_exe_options = {
    "packages": ["streamlit", "pandas", "openpyxl", "PIL", "os", "datetime"],
    "include_files": [
        "logo_petrobras.png",
        "logo jsl.png",
    ],
    "excludes": ["tkinter"]
}

# Configuração do executável
setup(
    name="App_711_712",
    version="1.0",
    description="Sistema de Análise - Movimentos SAP 711/712",
    options={"build_exe": build_exe_options},
    executables=[Executable("app_711_712.py", base=None, icon=None)]
)