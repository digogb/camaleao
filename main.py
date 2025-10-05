#!/usr/bin/env python3
"""
Ponto de entrada principal do Anonimizador
"""
import sys
from pathlib import Path

# Adiciona o diretório build ao path apenas quando rodando como script
if not getattr(sys, 'frozen', False):
    sys.path.insert(0, str(Path(__file__).parent / "build"))

from blur_voice import ModernBlurCam

if __name__ == "__main__":
    app = ModernBlurCam()
    app.root.mainloop()
