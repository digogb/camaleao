# 🎭 Anonimizador - BlurCam & Voice Controller

Sistema de anonimização de vídeo e voz em tempo real com interface gráfica moderna.

## 📋 Funcionalidades

- 🎥 **Blur de Vídeo**: Desfoque de rosto em tempo real via webcam
- 🎤 **Modificação de Voz**: Alteração de voz em tempo real (masculina/feminina)
- 🖥️ **Interface Moderna**: GUI intuitiva com tema escuro/claro
- ⚙️ **Configurações Persistentes**: Salvamento automático de preferências
- 📊 **Logs em Tempo Real**: Monitoramento de processos

## 🗂️ Estrutura do Projeto

```
Anonimizador/
├── assets/
│   ├── executables/       # Executáveis externos (BlurCamOptDbg.exe, ffplay.exe)
│   └── icons/             # Ícones e imagens
├── build/                 # Scripts de aplicação e build
│   ├── blur_voice.py      # Interface gráfica principal
│   ├── blur.py            # Script de blur standalone
│   └── build_exe.py       # Gerador de executável
├── config/                # Arquivos de configuração
│   └── camaleao_config.json
├── dist/                  # Executáveis compilados (gerado)
├── docs/                  # Documentação adicional
├── requirements.txt       # Dependências Python
└── README.md
```

## 🚀 Instalação

### Requisitos
- Python 3.8+
- Windows (para executáveis .exe)

### Passos

1. **Clone o repositório**
```bash
git clone <url-do-repositorio>
cd Anonimizador
```

2. **Crie um ambiente virtual** (recomendado)
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

## 💻 Uso

### Modo Desenvolvimento (Python)

Execute a interface gráfica:
```bash
python build/blur_voice.py
```

### Modo Produção (Executável)

1. **Gere o executável**:
```bash
python build/build_exe.py
```

2. **Execute o programa**:
   - O executável será criado em `dist/`
   - Execute `BlurCamVoiceController.exe`

## 📦 Dependências

- `sounddevice` - Captura e reprodução de áudio
- `numpy` - Processamento numérico
- `scipy` - Processamento de sinais
- `Pillow` - Manipulação de imagens
- `pyinstaller` - Geração de executáveis (dev)

## ⚙️ Configuração

As configurações são salvas automaticamente em `config/camaleao_config.json`:

```json
{
    "selected_audio_device": "Nome do Dispositivo"
}
```

## 🛠️ Desenvolvimento

### Estrutura de Código

- **build/blur_voice.py**: Interface principal com tkinter
- **build/blur.py**: Script standalone de blur
- **build/build_exe.py**: Automatização do build com PyInstaller

### Caminhos Dinâmicos

O código detecta automaticamente se está rodando como script ou executável:
- **Script**: Usa caminhos relativos a partir da raiz do projeto
- **Executável**: Usa caminhos relativos ao executável

## 🐛 Troubleshooting

### Executáveis não encontrados
- Verifique se `BlurCamOptDbg.exe` e `ffplay.exe` estão em `assets/executables/`

### Erro de dispositivos de áudio
- Certifique-se de ter dispositivos de áudio conectados
- Execute como administrador se necessário

### Build falha
- Instale PyInstaller: `pip install pyinstaller`
- Verifique se todos os arquivos necessários existem

## 📝 Licença

[Adicione sua licença aqui]

## 👤 Autor

[Adicione informações do autor aqui]

---

**Nota**: Este projeto utiliza executáveis externos para processamento de vídeo (BlurCamOptDbg.exe) e áudio (ffplay.exe).
