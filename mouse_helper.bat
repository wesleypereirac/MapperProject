@echo off
:: Verifica se está rodando como administrador
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Solicitando permissao de administrador...
    powershell -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)

echo Rodando como administrador...

:: AJUSTE O CAMINHO (SEM ASPAS SIMPLES)
cd /d "C:\Users\homec\Downloads\mouse" || (
    echo Erro ao acessar o diretorio
    pause
    exit /b
)

python mouse.py

pause