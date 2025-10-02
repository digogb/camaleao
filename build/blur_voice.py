import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import threading
import os
import sys
import time
import re
import json
from pathlib import Path
from PIL import Image, ImageTk

class ModernBlurCam:
    def __init__(self):
        self.video_process = None
        self.audio_process = None
        self.video_pid = None
        self.audio_pid = None
        self.is_video_running = False
        self.is_audio_running = False
        
        # Detecta se está rodando como executável ou script Python
        if getattr(sys, 'frozen', False):
            # Rodando como executável
            self.base_path = Path(sys.executable).parent
        else:
            # Rodando como script Python
            self.base_path = Path(__file__).parent.parent

        self.video_executable = str(self.base_path / "assets" / "executables" / "BlurCamOptDbg.exe")
        self.audio_executable = str(self.base_path / "assets" / "executables" / "ffplay.exe")

        self.video_args = [
            "--mode", "box", "--blur", "61",
            "--capture-scale", "0.5", "--proc-scale", "0.5", "--frame-skip", "2"
        ]

        self.audio_devices = []
        self.selected_audio_device = None
        self.audio_filters_male = 'highpass=f=60,asetrate=48000*0.700899,aresample=48000,atempo=1.122462,lowpass=f=7000,aformat=channel_layouts=mono'
        self.audio_filters_female = 'highpass=f=60,asetrate=48000*1.3,aresample=48000,atempo=0.85,lowpass=f=7000,aformat=channel_layers=mono'
        self.audio_filters = self.audio_filters_male

        # Caminho para a imagem do ícone
        self.icon_path = str(self.base_path / "assets" / "icons" / "camaleao_icon.jpg")

        # Arquivo de configurações
        self.config_file = str(self.base_path / "config" / "camaleao_config.json")
        
        self.colors = {
            'bg': '#f8f9fa',
            'card': '#ffffff',
            'primary': '#667eea',
            'secondary': '#764ba2',
            'success': '#48bb78',
            'danger': '#f56565',
            'text': '#2d3748',
            'text_light': '#718096',
            'border': '#e2e8f0'
        }
        
        self.setup_gui()
        self.load_config()
        self.check_executables()
        self.load_audio_devices()
        self.cleanup_orphaned_processes()
    
    def load_config(self):
        """Carrega as configurações salvas do arquivo JSON"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    saved_device = config.get('selected_audio_device', None)
                    if saved_device:
                        self.selected_audio_device = saved_device
                        self.log_message("Configuração carregada")
        except Exception as e:
            self.log_message(f"Erro ao carregar config: {e}")
    
    def save_config(self):
        """Salva as configurações no arquivo JSON"""
        try:
            config = {
                'selected_audio_device': self.selected_audio_device
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            self.log_message("Configuração salva")
        except Exception as e:
            self.log_message(f"Erro ao salvar config: {e}")
    
    def cleanup_orphaned_processes(self):
        if sys.platform == "win32":
            try:
                subprocess.run(["taskkill", "/F", "/IM", self.video_executable], capture_output=True, text=True)
                subprocess.run(["taskkill", "/F", "/IM", "ffplay.exe"], capture_output=True, text=True)
            except: pass
    
    def load_audio_devices(self):
        try:
            self.log_message("Carregando dispositivos...")
            if not os.path.exists(self.audio_executable):
                self.audio_devices = []
                return
            
            result = subprocess.run([self.audio_executable, "-list_devices", "true", "-f", "dshow", "-i", "dummy"],
                                  capture_output=True, text=True, timeout=10)
            
            audio_devices = []
            for line in result.stderr.split('\n'):
                if '(audio)' in line.lower() and '"' in line:
                    match = re.search(r'"([^"]+)"', line)
                    if match:
                        audio_devices.append(match.group(1))
            
            self.audio_devices = audio_devices
            if audio_devices:
                self.log_message(f"{len(audio_devices)} dispositivo(s) encontrado(s)")
                self.update_audio_device_list()
                # Atualiza o display após carregar os dispositivos
                self.update_device_display()
        except Exception as e:
            self.log_message(f"Erro: {e}")
            self.audio_devices = []
    
    def update_audio_device_list(self):
        if self.audio_devices and not self.selected_audio_device:
            self.selected_audio_device = self.audio_devices[0]
            self.update_device_display()
    
    def update_device_display(self):
        if self.selected_audio_device:
            device = self.selected_audio_device[:40] + "..." if len(self.selected_audio_device) > 40 else self.selected_audio_device
            self.device_label.config(text=device)
        else:
            self.device_label.config(text="Não configurado")
    
    def check_executables(self):
        script_dir = Path(__file__).parent
        
        video_found = os.path.exists(self.video_executable) or (script_dir / self.video_executable).exists()
        audio_found = os.path.exists(self.audio_executable) or (script_dir / self.audio_executable).exists()
        
        if not video_found:
            self.video_btn.button.config(state="disabled", bg=self.colors['text_light'])
        if not audio_found:
            self.audio_btn.button.config(state="disabled", bg=self.colors['text_light'])
    
    def create_rounded_button(self, parent, text, bg, command):
        # Frame externo para simular bordas arredondadas
        outer_frame = tk.Frame(parent, bg=parent.cget('bg'), highlightthickness=0, bd=0)
        
        btn = tk.Button(outer_frame, text=text, font=("Segoe UI", 11, "bold"),
                       bg=bg, fg='white', activebackground=bg,
                       activeforeground='white', relief=tk.FLAT,
                       cursor="hand2", bd=0, highlightthickness=0,
                       command=command)
        btn.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Armazenar referência do botão no frame para acesso posterior
        outer_frame.button = btn
        
        return outer_frame
    
    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Camaleão - Proteção de Privacidade")
        self.root.geometry("750x750")
        self.root.resizable(True, True)
        self.root.minsize(700, 720)
        self.root.configure(bg=self.colors['bg'])
        
        # Definir ícone da janela
        try:
            # Opção 1: Se você tiver um arquivo .ico
            # self.root.iconbitmap("camaleao_icon.ico")
            
            # Opção 2: Se você tiver PNG/JPG (mesmo arquivo do header)
            icon_img = Image.open(self.icon_path)
            icon_photo = ImageTk.PhotoImage(icon_img)
            self.root.iconphoto(True, icon_photo)
        except:
            pass  # Se não conseguir carregar, usa o ícone padrão
        
        self.voice_gender = tk.StringVar(value="masculino")
        
        main = tk.Frame(self.root, bg=self.colors['bg'])
        main.pack(fill=tk.BOTH, expand=True, padx=25, pady=20)
        
        # Header
        header = tk.Frame(main, bg=self.colors['bg'])
        header.pack(fill=tk.X, pady=(0, 20))
        
        # Frame para ícone + título
        title_frame = tk.Frame(header, bg=self.colors['bg'])
        title_frame.pack(anchor="w")
        
        # Tentar carregar o ícone
        try:
            icon_image = Image.open(self.icon_path)
            icon_image = icon_image.resize((40, 40), Image.Resampling.LANCZOS)
            self.icon_photo = ImageTk.PhotoImage(icon_image)
            icon_label = tk.Label(title_frame, image=self.icon_photo, bg=self.colors['bg'])
            icon_label.pack(side=tk.LEFT, padx=(0, 10))
        except:
            # Se não encontrar a imagem, usa o emoji
            icon_label = tk.Label(title_frame, text="🦎", font=("Segoe UI", 32), bg=self.colors['bg'])
            icon_label.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(title_frame, text="Camaleão", font=("Comic Sans MS", 26, "bold"),
                bg=self.colors['bg'], fg=self.colors['text']).pack(side=tk.LEFT)
        
        tk.Label(header, text="Proteção Digital de Áudio e Vídeo", font=("Segoe UI", 11),
                bg=self.colors['bg'], fg=self.colors['text_light']).pack(anchor="w")
        
        # Video Card
        video_card_shadow = tk.Frame(main, bg='#d0d5dd', highlightthickness=0)
        video_card_shadow.pack(fill=tk.X, pady=(0, 15))
        
        video_card = tk.Frame(video_card_shadow, bg=self.colors['card'], highlightbackground=self.colors['border'],
                             highlightthickness=0)
        video_card.pack(fill=tk.X, padx=2, pady=2)
        
        vc = tk.Frame(video_card, bg=self.colors['card'])
        vc.pack(fill=tk.X, padx=20, pady=18)
        
        tk.Label(vc, text="Desfoque de Vídeo", font=("Segoe UI", 15, "bold"),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor="w", pady=(0, 5))
        tk.Label(vc, text="Desfoca completamente a imagem da câmera", font=("Segoe UI", 10),
                bg=self.colors['card'], fg=self.colors['text_light']).pack(anchor="w", pady=(0, 12))
        
        self.video_btn = self.create_rounded_button(vc, "LIGAR DESFOQUE DE VÍDEO", self.colors['primary'], self.toggle_video)
        self.video_btn.pack(fill=tk.X, ipady=12)
        
        # Audio Card
        audio_card_shadow = tk.Frame(main, bg='#d0d5dd', highlightthickness=0)
        audio_card_shadow.pack(fill=tk.X, pady=(0, 15))
        
        audio_card = tk.Frame(audio_card_shadow, bg=self.colors['card'], highlightbackground=self.colors['border'],
                             highlightthickness=0)
        audio_card.pack(fill=tk.X, padx=2, pady=2)
        
        ac = tk.Frame(audio_card, bg=self.colors['card'])
        ac.pack(fill=tk.X, padx=20, pady=18)
        
        tk.Label(ac, text="Modificação de Voz", font=("Segoe UI", 15, "bold"),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor="w", pady=(0, 5))
        tk.Label(ac, text="Altera o timbre da sua voz em tempo real", font=("Segoe UI", 10),
                bg=self.colors['card'], fg=self.colors['text_light']).pack(anchor="w", pady=(0, 12))
        
        # Device
        dev_frame = tk.Frame(ac, bg='#f7fafc', highlightbackground=self.colors['border'],
                            highlightthickness=1)
        dev_frame.pack(fill=tk.X, pady=(10, 12))
        dev_inner = tk.Frame(dev_frame, bg='#f7fafc')
        dev_inner.pack(padx=12, pady=8)
        
        tk.Label(dev_inner, text="Dispositivo:", font=("Segoe UI", 9),
                bg='#f7fafc', fg=self.colors['text_light']).pack(side=tk.LEFT)
        self.device_label = tk.Label(dev_inner, text="Carregando...", font=("Segoe UI", 9, "bold"),
                                     bg='#f7fafc', fg=self.colors['text'])
        self.device_label.pack(side=tk.LEFT, padx=(8, 0))
        
        # Gender
        tk.Label(ac, text="Tipo de Voz", font=("Segoe UI", 10, "bold"),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor="w", pady=(0, 8))
        
        gender_frame = tk.Frame(ac, bg=self.colors['card'])
        gender_frame.pack(fill=tk.X, pady=(0, 12))
        
        self.male_btn = tk.Button(gender_frame, text="Masculino", font=("Segoe UI", 10),
                                  bg=self.colors['secondary'], fg='white', relief=tk.FLAT,
                                  activebackground=self.colors['secondary'], activeforeground='white',
                                  cursor="hand2", bd=0,
                                  command=lambda: self.select_gender("masculino"))
        self.male_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 6), ipady=10)
        
        self.female_btn = tk.Button(gender_frame, text="Feminino", font=("Segoe UI", 10),
                                    bg='#e2e8f0', fg=self.colors['text'], relief=tk.FLAT,
                                    activebackground='#e2e8f0', activeforeground=self.colors['text'],
                                    cursor="hand2", bd=0,
                                    command=lambda: self.select_gender("feminino"))
        self.female_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(6, 0), ipady=10)
        
        self.audio_btn = self.create_rounded_button(ac, "LIGAR MODIFICAÇÃO DE VOZ", self.colors['secondary'], self.toggle_audio)
        self.audio_btn.pack(fill=tk.X, ipady=12)
        
        # Control Buttons
        controls = tk.Frame(main, bg=self.colors['bg'])
        controls.pack(fill=tk.X, pady=(0, 15))
        
        btn1 = self.create_rounded_button(controls, "LIGAR TUDO", self.colors['success'], self.start_all)
        btn1.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 6), ipady=11)
        
        btn2 = self.create_rounded_button(controls, "DESLIGAR TUDO", self.colors['danger'], self.stop_all)
        btn2.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(3, 6), ipady=11)
        
        btn3 = self.create_rounded_button(controls, "CONFIGURAÇÕES", '#718096', self.show_config)
        btn3.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(3, 0), ipady=11)
        
        # Log
        log_card_shadow = tk.Frame(main, bg='#d0d5dd', highlightthickness=0)
        log_card_shadow.pack(fill=tk.BOTH, expand=True)
        
        log_card = tk.Frame(log_card_shadow, bg=self.colors['card'], highlightbackground=self.colors['border'],
                           highlightthickness=0)
        log_card.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        lc = tk.Frame(log_card, bg=self.colors['card'])
        lc.pack(fill=tk.BOTH, expand=True, padx=20, pady=18)
        
        tk.Label(lc, text="Log de Atividades", font=("Segoe UI", 12, "bold"),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor="w", pady=(0, 10))
        
        self.log_text = scrolledtext.ScrolledText(lc, height=4, font=("Consolas", 9),
                                                  bg='#f7fafc', fg=self.colors['text'],
                                                  relief=tk.FLAT, wrap=tk.WORD,
                                                  highlightbackground=self.colors['border'],
                                                  highlightthickness=1)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.center_window()
        
        self.log_message("Sistema iniciado")
        self.log_message("Tipo de voz: MASCULINO")
    
    def select_gender(self, gender):
        self.voice_gender.set(gender)
        if gender == "masculino":
            self.male_btn.config(bg=self.colors['secondary'], fg='white')
            self.female_btn.config(bg='#e2e8f0', fg=self.colors['text'])
            self.audio_filters = self.audio_filters_male
            self.log_message("Tipo de voz: MASCULINO")
        else:
            self.female_btn.config(bg=self.colors['secondary'], fg='white')
            self.male_btn.config(bg='#e2e8f0', fg=self.colors['text'])
            self.audio_filters = self.audio_filters_female
            self.log_message("Tipo de voz: FEMININO")
        
        if self.is_audio_running:
            self.log_message("Reinicie para aplicar")
    
    def log_message(self, message):
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        try:
            print(f"[{timestamp}] {message}")
        except: pass
    
    def center_window(self):
        self.root.update_idletasks()
        w, h = self.root.winfo_width(), self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (w // 2)
        y = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.root.geometry(f'{w}x{h}+{x}+{y}')
    
    def toggle_video(self):
        self.start_video() if not self.is_video_running else self.stop_video()
    
    def start_video(self):
        if not os.path.exists(self.video_executable):
            messagebox.showerror("Erro", "BlurCam não encontrado!")
            return
        
        self.log_message("Iniciando blur...")
        
        def run():
            try:
                self.video_process = subprocess.Popen([self.video_executable] + self.video_args,
                                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                      creationflags=subprocess.CREATE_NO_WINDOW if sys.platform=="win32" else 0)
                self.video_pid = self.video_process.pid
                self.log_message(f"Blur iniciado (PID: {self.video_pid})")
                self.video_process.wait()
                self.root.after(0, self.on_video_ended)
            except Exception as e:
                self.log_message(f"Erro: {e}")
                self.root.after(0, self.on_video_ended)
        
        threading.Thread(target=run, daemon=True).start()
        self.is_video_running = True
        self.video_btn.button.config(text="DESLIGAR DESFOQUE DE VÍDEO", bg=self.colors['danger'])
    
    def stop_video(self):
        self.log_message("Parando blur...")
        if self.video_process:
            try:
                if self.video_process.poll() is None:
                    self.video_process.terminate()
                    try:
                        self.video_process.wait(timeout=1)
                    except subprocess.TimeoutExpired:
                        self.video_process.kill()
                        self.video_process.wait()
            except: pass
        
        if sys.platform == "win32":
            subprocess.run(["taskkill", "/F", "/IM", self.video_executable], capture_output=True, text=True)
        
        self.on_video_ended()
        self.log_message("Blur parado")
    
    def on_video_ended(self):
        self.is_video_running = False
        self.video_process = None
        self.video_pid = None
        self.video_btn.button.config(text="LIGAR DESFOQUE DE VÍDEO", bg=self.colors['primary'])
    
    def toggle_audio(self):
        self.start_audio() if not self.is_audio_running else self.stop_audio()
    
    def start_audio(self):
        if not os.path.exists(self.audio_executable):
            messagebox.showerror("Erro", "FFplay não encontrado!")
            return
        
        if not self.selected_audio_device:
            if self.audio_devices:
                self.selected_audio_device = self.audio_devices[0]
            else:
                messagebox.showerror("Erro", "Nenhum dispositivo!\n\nVá em CONFIGURAÇÕES")
                return
        
        self.log_message(f"Iniciando modificador...")
        
        def run():
            try:
                cmd = f'{self.audio_executable} -nodisp -autoexit -f dshow -i "audio={self.selected_audio_device}" -af "{self.audio_filters}"'
                self.audio_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                self.audio_pid = self.audio_process.pid
                self.log_message(f"Modificador iniciado (PID: {self.audio_pid})")
                self.log_message(self.audio_process.args)
                self.audio_process.wait()
                
                self.root.after(0, self.on_audio_ended)
            except Exception as e:
                self.log_message(f"Erro: {e}")
                self.root.after(0, self.on_audio_ended)
        
        threading.Thread(target=run, daemon=True).start()
        self.is_audio_running = True
        self.audio_btn.button.config(text="DESLIGAR MODIFICAÇÃO DE VOZ", bg=self.colors['danger'])
    
    def stop_audio(self):
        self.log_message("Parando modificador...")
        if self.audio_process:
            try:
                if self.audio_process.poll() is None:
                    self.audio_process.terminate()
                    try:
                        self.audio_process.wait(timeout=1)
                    except subprocess.TimeoutExpired:
                        self.audio_process.kill()
                        self.audio_process.wait()
            except: pass
        
        if sys.platform == "win32":
            subprocess.run(["taskkill", "/F", "/IM", "ffplay.exe"], capture_output=True, text=True)
        
        self.on_audio_ended()
        self.log_message("Modificador parado")
    
    def on_audio_ended(self):
        self.is_audio_running = False
        self.audio_process = None
        self.audio_pid = None
        self.audio_btn.button.config(text="LIGAR MODIFICAÇÃO DE VOZ", bg=self.colors['secondary'])
    
    def start_all(self):
        self.log_message("Iniciando tudo...")
        if not self.is_video_running:
            self.start_video()
        if not self.is_audio_running:
            time.sleep(0.5)
            self.start_audio()
    
    def stop_all(self):
        self.log_message("Parando tudo...")
        if self.is_video_running:
            self.stop_video()
        if self.is_audio_running:
            self.stop_audio()
    
    def show_config(self):
        cw = tk.Toplevel(self.root)
        cw.title("Configurações")
        cw.geometry("650x400")
        cw.minsize(600, 350)
        cw.configure(bg=self.colors['bg'])
        cw.transient(self.root)
        cw.grab_set()
        
        # Centralizar janela
        cw.update_idletasks()
        x = (cw.winfo_screenwidth() // 2) - (650 // 2)
        y = (cw.winfo_screenheight() // 2) - (400 // 2)
        cw.geometry(f'650x400+{x}+{y}')
        
        c = tk.Frame(cw, bg=self.colors['bg'])
        c.pack(fill=tk.BOTH, expand=True, padx=35, pady=30)
        
        tk.Label(c, text="Configurações", font=("Segoe UI", 22, "bold"),
                bg=self.colors['bg'], fg=self.colors['text']).pack(pady=(0,25))
        
        card_shadow = tk.Frame(c, bg='#d0d5dd', highlightthickness=0)
        card_shadow.pack(fill=tk.BOTH, expand=True)
        
        card = tk.Frame(card_shadow, bg=self.colors['card'], highlightbackground=self.colors['border'],
                       highlightthickness=0)
        card.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        cc = tk.Frame(card, bg=self.colors['card'])
        cc.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        tk.Label(cc, text="Dispositivo de Áudio", font=("Segoe UI", 14, "bold"),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor="w", pady=(0,10))
        
        tk.Label(cc, text="Selecione o microfone que será usado para modificação de voz", 
                font=("Segoe UI", 10),
                bg=self.colors['card'], fg=self.colors['text_light']).pack(anchor="w", pady=(0,20))
        
        combo = ttk.Combobox(cc, state="readonly", font=("Segoe UI", 11), values=self.audio_devices)
        combo.pack(fill=tk.X, ipady=12, pady=(0,25))
        
        if self.selected_audio_device and self.selected_audio_device in self.audio_devices:
            combo.set(self.selected_audio_device)
        elif self.audio_devices:
            combo.current(0)
        
        btn_frame = tk.Frame(cc, bg=self.colors['card'])
        btn_frame.pack(fill=tk.X)
        
        apply_btn = self.create_rounded_button(btn_frame, "APLICAR", self.colors['success'],
                                               lambda: self.apply_config(cw, combo))
        apply_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 8), ipady=14)
        
        cancel_btn = self.create_rounded_button(btn_frame, "CANCELAR", self.colors['text_light'],
                                               lambda: cw.destroy())
        cancel_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(8, 0), ipady=14)
    
    def apply_config(self, window, combo):
        try:
            sel = combo.get()
            if sel:
                self.selected_audio_device = sel
                self.save_config()
                self.log_message(f"Dispositivo configurado")
                self.update_device_display()
                window.destroy()
                messagebox.showinfo("Sucesso", f"Configurado:\n{sel}")
            else:
                messagebox.showwarning("Aviso", "Selecione um dispositivo")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    
    def on_closing(self):
        self.log_message("Encerrando...")
        self.stop_all()
        time.sleep(0.5)
        self.cleanup_orphaned_processes()
        self.root.destroy()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ModernBlurCam()
    app.run()