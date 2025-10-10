@echo off
echo ========================================
echo   Gerando executável do Camaleão
echo ========================================
echo.

echo [1/4] Verificando dependências...
pip install -q pyinstaller
if errorlevel 1 (
    echo ERRO: Falha ao instalar PyInstaller
    pause
    exit /b 1
)

echo [2/4] Limpando builds anteriores...
if exist "dist\Camaleao" rmdir /s /q "dist\Camaleao"
if exist "build\temp" rmdir /s /q "build\temp"

echo [3/4] Gerando executável...
pyinstaller Camaleao.spec --clean
if errorlevel 1 (
    echo ERRO: Falha ao gerar executável
    pause
    exit /b 1
)

echo [4/4] Criando arquivo ZIP...
powershell -Command "Compress-Archive -Path 'dist\Camaleao' -DestinationPath 'dist\Camaleao.zip' -Force"
if errorlevel 1 (
    echo AVISO: Falha ao criar ZIP, mas o executável foi gerado com sucesso
) else (
    echo ZIP criado com sucesso!
)

echo.
echo ========================================
echo   Build completo!
echo   Executável: dist\Camaleao\Camaleao.exe
echo   ZIP: dist\Camaleao.zip
echo ========================================
pause
