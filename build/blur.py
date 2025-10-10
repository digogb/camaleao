#!/usr/bin/env python3
"""
Script para gerar executável do BlurCam & Voice Controller
Inclui todos os arquivos necessários
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

def check_required_files():
    """Verifica se todos os arquivos necessários existem"""
    print("\n🔍 Verificando arquivos necessários...")
    print("=" * 60)
    
    required_files = {
        "blur_voice.py": "Código principal",
        "BlurCamOptDbg.exe": "Executável de blur de vídeo",
        "ffplay.exe": "Executável de áudio FFmpeg"
    }
    
    optional_files = {
        "ffmpeg.exe": "FFmpeg completo (opcional)",
        "icon.ico": "Ícone personalizado (opcional)"
    }
    
    missing_required = []
    
    # Verifica arquivos obrigatórios
    for file, description in required_files.items():
        if os.path.exists(file):
            print(f"✓ {file} - {description}")
        else:
            print(f"✗ {file} - {description} [FALTANDO]")
            missing_required.append(file)
    
    # Verifica arquivos opcionais
    print("\nArquivos opcionais:")
    for file, description in optional_files.items():
        if os.path.exists(file):
            print(f"✓ {file} - {description}")
        else:
            print(f"○ {file} - {description} [Não encontrado]")
    
    if missing_required:
        print("\n❌ ERRO: Arquivos obrigatórios faltando!")
        print("\nArquivos que precisam estar na pasta:")
        for file in missing_required:
            print(f"  - {file}")
        
        if "ffplay.exe" in missing_required:
            print("\n💡 Para obter o ffplay.exe:")
            print("   1. Acesse: https://www.gyan.dev/ffmpeg/builds/")
            print("   2. Baixe: ffmpeg-release-essentials.zip")
            print("   3. Extraia e copie ffplay.exe da pasta bin/")
        
        return False
    
    print("\n✅ Todos os arquivos obrigatórios encontrados!")
    return True

def build_executable():
    """Gera o executável usando PyInstaller"""
    
    print("\n🚀 Iniciando processo de build...")
    print("=" * 60)
    
    # Comando PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",                      # Arquivo único
        "--windowed",                     # Sem console
        "--noconsole",                    # Força sem console
        "--name=BlurCamVoiceController",  # Nome do executável
        "--clean",                        # Limpa cache
        "--optimize=2",                   # Otimização máxima
    ]
    
    # Adiciona ícone se existir
    if os.path.exists("icon.ico"):
        cmd.extend(["--icon=icon.ico"])
        print("✓ Ícone personalizado será incluído")
    
    # Adiciona arquivos de dados
    data_files = []
    
    if os.path.exists("BlurCamOptDbg.exe"):
        data_files.append("BlurCamOptDbg.exe")
    
    if os.path.exists("ffplay.exe"):
        data_files.append("ffplay.exe")
    
    if os.path.exists("ffmpeg.exe"):
        data_files.append("ffmpeg.exe")
    
    # Adiciona cada arquivo de dados
    for file in data_files:
        cmd.extend(["--add-data", f"{file};."])
        print(f"✓ {file} será incluído no executável")
    
    # Adiciona o arquivo Python principal
    cmd.append("blur_voice.py")
    
    print("\n📦 Comando PyInstaller:")
    print(" ".join(cmd))
    print("=" * 60)
    
    try:
        # Executa o PyInstaller
        print("\n⏳ Compilando... (isso pode demorar alguns minutos)")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("\n✅ BUILD CONCLUÍDO COM SUCESSO!")
            print("=" * 60)
            
            # Localiza o executável
            exe_path = Path("dist/BlurCamVoiceController.exe")
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / 1024 / 1024
                print(f"\n📁 Executável criado:")
                print(f"   Local: {exe_path.absolute()}")
                print(f"   Tamanho: {size_mb:.1f} MB")
                
                print("\n📋 INSTRUÇÕES DE USO:")
                print("   1. O executável está em: dist\\BlurCamVoiceController.exe")
                print("   2. Todos os arquivos necessários já estão incluídos")
                print("   3. Copie o executável para onde quiser")
                print("   4. Execute e aproveite!")
                
                print("\n💡 RECURSOS INCLUÍDOS:")
                print("   ✓ Blur de vídeo (BlurCam)")
                print("   ✓ Modificador de voz (FFplay)")
                print("   ✓ Detecção automática de dispositivos")
                print("   ✓ Interface gráfica completa")
                print("   ✓ Log de atividades")
                
                return True
            else:
                print("✗ Executável não encontrado em dist/")
                return False
        else:
            print("\n✗ ERRO NO BUILD:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"\n✗ Erro ao executar PyInstaller: {e}")
        return False

def clean_build_files():
    """Limpa arquivos temporários do build"""
    import shutil
    
    print("\n🧹 Limpando arquivos temporários...")
    
    folders_to_clean = ["build", "__pycache__"]
    
    for folder in folders_to_clean:
        if os.path.exists(folder):
            try:
                shutil.rmtree(folder)
                print(f"✓ Removido: {folder}/")
            except Exception as e:
                print(f"⚠️  Não foi possível remover {folder}/: {e}")
    
    # Remove arquivos .spec
    for spec_file in Path(".").glob("*.spec"):
        try:
            spec_file.unlink()
            print(f"✓ Removido: {spec_file}")
        except Exception as e:
            print(f"⚠️  Não foi possível remover {spec_file}: {e}")

def create_readme():
    """Cria um README para distribuição"""
    readme_content = """

# Camaleão

## 🎯 O que é?

Este programa permite:
- 🎥 Borrar completamente sua câmera (blur de vídeo)
- 🎤 Modificar sua voz em tempo real
- ⚙️ Controlar tudo em uma interface simples

## 🚀 Como usar?

1. Execute o arquivo Camaleao.exe
2. Em configurações, selecione seu microfone na lista
3. Clique em "LIGAR TUDO" ou ligue cada recurso individualmente
4. Entre na sua videochamada
5. Quando terminar, clique em "DESLIGAR TUDO"

## 🔧 Compatibilidade

Funciona com:
- Zoom
- Microsoft Teams
- Google Meet
- Discord
- Skype
- Qualquer app que use DirectShow

## 📋 Requisitos

- Windows 7 ou superior
- Câmera e microfone conectados
- Driver UnityCapture instalado na máquina  
- Virtual Audio Cable (VB-Audio) instalado na máquina

## 💡 Dicas

- Teste antes de usar em reuniões importantes
- Configure seu app de videochamada para usar "Unity Video Capture" como câmera
- Configure seu app de videochamada para usar "Cable Output (VB-Audio Virtual Cable)" como microfone
- Configure seu dispositivo de saída do windows para usar "Cable Input (VB-Audio Virtual Cable)" como saída
- O microfone configurado no app será automaticamente modificado

## 🔒 Privacidade

- Toda modificação acontece localmente no seu computador
- Nenhum dado é enviado para internet
- Seu vídeo fica completamente borrado
- Sua voz é modificada em tempo real

Aproveite! 🎉
"""
    
    readme_path = Path("dist/README.txt")
    if readme_path.parent.exists():
        try:
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(readme_content)
            print(f"✓ README criado em: {readme_path}")
        except Exception as e:
            print(f"⚠️  Não foi possível criar README: {e}")

def main():
    """Função principal"""
    print("=" * 60)
    print("🛠️  GERADOR DE EXECUTÁVEL")
    print("    BlurCam & Voice Controller")
    print("=" * 60)
    
    # Passo 1: Instalar PyInstaller
    if not install_pyinstaller():
        print("\nNão foi possível instalar o PyInstaller.")
        print("Tente instalar manualmente: pip install pyinstaller")
        input("\nPressione Enter para sair...")
        return
    
    # Passo 2: Verificar arquivos
    if not check_required_files():
        print("\n❌ Build cancelado - arquivos faltando")
        input("\nPressione Enter para sair...")
        return
    
    input("\n✅ Tudo pronto! Pressione Enter para iniciar o build...")
    
    # Passo 3: Gerar executável
    success = build_executable()
    
    if success:
        # Passo 4: Limpar arquivos temporários
        clean_build_files()
        
        # Passo 5: Criar README
        create_readme()
        
        print("\n" + "=" * 60)
        print("🎉 PROCESSO CONCLUÍDO COM SUCESSO!")
        print("=" * 60)
        print("\n📦 Seu executável está pronto para distribuição!")
        print("📁 Localize em: dist\\BlurCamVoiceController.exe")
        
    else:
        print("\n❌ Build falhou. Verifique os erros acima.")
    
    input("\nPressione Enter para sair...")

if __name__ == "__main__":
    main()