#!/usr/bin/env python3
"""
Script para gerar executável do BlurCam Controller
Autor: Assistant
"""

import subprocess
import sys
import os
from pathlib import Path

def install_pyinstaller():
    """Instala o PyInstaller se não estiver instalado"""
    try:
        import PyInstaller
        print("✓ PyInstaller já está instalado")
        return True
    except ImportError:
        print("PyInstaller não encontrado. Instalando...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✓ PyInstaller instalado com sucesso!")
            return True
        except subprocess.CalledProcessError:
            print("✗ Erro ao instalar PyInstaller")
            return False

def create_icon_file():
    """Cria um arquivo de ícone simples em Python (opcional)"""
    icon_content = '''
# Este é um exemplo de como você pode adicionar um ícone personalizado
# Coloque um arquivo .ico na pasta do projeto e descomente a linha --icon no comando PyInstaller
'''
    
    print("💡 Dica: Para um ícone personalizado, coloque um arquivo 'icon.ico' na pasta do projeto")

def build_executable():
    """Gera o executável usando PyInstaller"""
    
    print("🚀 Iniciando processo de build...")
    print("=" * 50)
    
    # Verifica se o arquivo Python existe
    python_file = "blur.py"
    if not os.path.exists(python_file):
        print(f"✗ Arquivo {python_file} não encontrado!")
        print("Certifique-se de que o arquivo está na mesma pasta que este script.")
        return False
    
    # Comando PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",                    # Gera um único arquivo executável
        "--windowed",                   # Remove a janela do console (GUI apenas)
        "--noconsole",                  # Força remoção do console (Windows)
        "--name=BlurCamController",     # Nome do executável
        "--clean",                      # Limpa cache antes do build
        "--optimize=2",                 # Otimização máxima
        # "--icon=icon.ico",            # Descomente se tiver um arquivo icon.ico
    ]
    
    # Adiciona argumentos para incluir dados necessários
    cmd.extend([
        "--add-data", "BlurCamOptDbg.exe;." if os.path.exists("BlurCamOptDbg.exe") else "",
        python_file
    ])
    
    # Remove argumentos vazios
    cmd = [arg for arg in cmd if arg]
    
    print("Comando PyInstaller:")
    print(" ".join(cmd))
    print("=" * 50)
    
    try:
        # Executa o PyInstaller
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ BUILD CONCLUÍDO COM SUCESSO!")
            print("=" * 50)
            
            # Localiza o executável gerado
            exe_path = Path("dist/BlurCamController.exe")
            if exe_path.exists():
                print(f"📁 Executável criado em: {exe_path.absolute()}")
                print(f"📦 Tamanho: {exe_path.stat().st_size / 1024 / 1024:.1f} MB")
                
                # Instruções de uso
                print("\n📋 INSTRUÇÕES DE USO:")
                print("1. Copie o arquivo BlurCamController.exe para onde quiser")
                print("2. Coloque o BlurCamOptDbg.exe na mesma pasta")
                print("3. Execute o BlurCamController.exe")
                
                # Verifica se o BlurCamOptDbg.exe existe
                if os.path.exists("BlurCamOptDbg.exe"):
                    print("✓ BlurCamOptDbg.exe encontrado - será incluído automaticamente")
                else:
                    print("⚠️  BlurCamOptDbg.exe não encontrado - coloque na mesma pasta do executável")
                
                return True
            else:
                print("✗ Executável não encontrado em dist/")
                return False
        else:
            print("✗ ERRO NO BUILD:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"✗ Erro ao executar PyInstaller: {e}")
        return False

def clean_build_files():
    """Limpa arquivos temporários do build"""
    import shutil
    
    print("\n🧹 Limpando arquivos temporários...")
    
    # Pastas a limpar
    folders_to_clean = ["build", "__pycache__"]
    files_to_clean = ["*.spec"]
    
    for folder in folders_to_clean:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"✓ Removido: {folder}/")
    
    # Remove arquivos .spec
    for spec_file in Path(".").glob("*.spec"):
        spec_file.unlink()
        print(f"✓ Removido: {spec_file}")

def main():
    """Função principal"""
    print("🛠️  GERADOR DE EXECUTÁVEL - BLURCAM CONTROLLER")
    print("=" * 55)
    
    # Passo 1: Instalar PyInstaller
    if not install_pyinstaller():
        print("Não foi possível instalar o PyInstaller. Tente manualmente:")
        print("pip install pyinstaller")
        return
    
    # Passo 2: Criar ícone (opcional)
    create_icon_file()
    
    # Passo 3: Gerar executável
    success = build_executable()
    
    # Passo 4: Limpar arquivos temporários
    if success:
        clean_build_files()
        
        print("\n🎉 PROCESSO CONCLUÍDO!")
        print("Seu executável está pronto para distribuição!")
    else:
        print("\n❌ Build falhou. Verifique os erros acima.")
    
    print("\nPressione Enter para sair...")
    input()

if __name__ == "__main__":
    main()