"""Baixaí - interface simples para baixar vídeos do YouTube com yt-dlp."""
import queue
import sys
import threading
from pathlib import Path
from tkinter import filedialog, messagebox
from types import SimpleNamespace

import customtkinter as ctk
import yt_dlp

# no .exe o FFmpeg vem embutido (pasta "ffmpeg" extraída pelo PyInstaller); rodando pelo código, usa o do sistema
FFMPEG = Path(getattr(sys, "_MEIPASS", "")) / "ffmpeg"


def baixar(links, pasta, log, mp3=False, playlist=False, barra=lambda fracao, texto: None):
    """Baixa cada link em `pasta`; um link com erro não interrompe os outros. Retorna os que falharam."""
    atual = {"link": 0}

    def progresso(d):
        total = d.get("total_bytes") or d.get("total_bytes_estimate")
        if d["status"] == "error" or not total:
            return
        info = d["info_dict"]
        texto = f"Link {atual['link']} de {len(links)}"
        if info.get("n_entries"):
            texto += f" · vídeo {info['playlist_index']} de {info['n_entries']}"
        barra(1 if d["status"] == "finished" else min(d["downloaded_bytes"] / total, 1),f"{texto} · {info.get('title', '')}")

    opcoes = {
        "outtmpl": str(Path(pasta) / "%(title)s.%(ext)s"),
        "progress_hooks": [progresso],
        "post_hooks": [lambda arquivo: log(f"✔ {Path(arquivo).name}")],
        # links de vídeo com "&list=" baixam só o vídeo, a menos que a playlist seja pedida
        "noplaylist": not playlist,
        # um vídeo indisponível dentro da playlist não deve derrubar o resto dela
        "ignoreerrors": "only_download",
        "logger": SimpleNamespace(debug=lambda m: None, warning=lambda m: None, error=lambda m: log(f"✖ {m}")),
        "quiet": True,
        "noprogress": True,
        "no_warnings": True,
    }
    if FFMPEG.is_dir():
        opcoes["ffmpeg_location"] = str(FFMPEG)
    if mp3:
        opcoes["format"] = "bestaudio/best"
        opcoes["postprocessors"] = [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}]
    falhas = []
    with yt_dlp.YoutubeDL(opcoes) as ydl:
        for i, link in enumerate(links, 1):
            atual["link"] = i
            log(f"[{i}/{len(links)}] {link}")
            try:
                if ydl.download([link]):  # código != 0: algum vídeo falhou (o motivo já saiu pelo logger)
                    falhas.append(link)
            except Exception as e:
                log(f"✖ Erro: {e}")
                falhas.append(link)
    return falhas


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Baixaí")
        self.geometry("760x680")
        self.minsize(560, 560)
        self.mensagens = queue.Queue()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(self, text="Baixaí", font=ctk.CTkFont(size=30, weight="bold")).grid(
            row=0, column=0, sticky="w", padx=24, pady=(20, 0))
        ctk.CTkLabel(self, text="Cole os links do YouTube abaixo, um por linha", text_color="gray").grid(
            row=1, column=0, sticky="w", padx=24)

        self.links = ctk.CTkTextbox(self, font=ctk.CTkFont(size=14), border_width=1)
        self.links.grid(row=2, column=0, sticky="nsew", padx=24, pady=(8, 12))

        linha = ctk.CTkFrame(self, fg_color="transparent")
        linha.grid(row=3, column=0, sticky="ew", padx=24)
        linha.grid_columnconfigure(0, weight=1)
        self.pasta = ctk.StringVar(value=str(Path.home() / "Downloads"))
        ctk.CTkEntry(linha, textvariable=self.pasta, height=36).grid(row=0, column=0, sticky="ew", padx=(0, 8))
        ctk.CTkButton(linha, text="Escolher pasta", height=36, width=130, command=self.escolher_pasta).grid(row=0, column=1)

        opcoes = ctk.CTkFrame(self, fg_color="transparent")
        opcoes.grid(row=4, column=0, sticky="w", padx=24, pady=12)
        self.mp3 = ctk.BooleanVar()
        self.playlist = ctk.BooleanVar()
        ctk.CTkSwitch(opcoes, text="Só o áudio (MP3)", variable=self.mp3).pack(side="left", padx=(0, 24))
        ctk.CTkSwitch(opcoes, text="Baixar a playlist inteira", variable=self.playlist).pack(side="left")

        self.botao = ctk.CTkButton(self, text="Baixar", height=44, font=ctk.CTkFont(size=16, weight="bold"),
                                   command=self.iniciar)
        self.botao.grid(row=5, column=0, sticky="ew", padx=24)

        self.status = ctk.CTkLabel(self, text="Pronto para baixar", anchor="w")
        self.status.grid(row=6, column=0, sticky="ew", padx=24, pady=(14, 0))
        self.barra = ctk.CTkProgressBar(self, height=12)
        self.barra.set(0)
        self.barra.grid(row=7, column=0, sticky="ew", padx=24, pady=(4, 12))

        self.saida = ctk.CTkTextbox(self, height=130, state="disabled", font=ctk.CTkFont(family="Consolas", size=12))
        self.saida.grid(row=8, column=0, sticky="nsew", padx=24, pady=(0, 20))

        self.after(100, self.atualizar)

    def escolher_pasta(self):
        pasta = filedialog.askdirectory(initialdir=self.pasta.get())
        if pasta:
            self.pasta.set(pasta)

    def iniciar(self):
        links = [l.strip() for l in self.links.get("1.0", "end").splitlines() if l.strip()]
        pasta = self.pasta.get()
        if not links:
            messagebox.showwarning("Baixaí", "Cole pelo menos um link.")
            return
        if not Path(pasta).is_dir():
            messagebox.showwarning("Baixaí", "Escolha uma pasta válida.")
            return
        self.botao.configure(state="disabled", text="Baixando...")
        args = (links, pasta, self.mp3.get(), self.playlist.get())
        threading.Thread(target=self.trabalhar, args=args, daemon=True).start()

    def trabalhar(self, links, pasta, mp3, playlist):
        falhas = baixar(links, pasta, lambda m: self.mensagens.put(("log", m)), mp3, playlist,
                        lambda f, t: self.mensagens.put(("barra", f, t)))
        self.mensagens.put(("fim", f"Concluído! {len(links) - len(falhas)} de {len(links)} links baixados."))

    def atualizar(self):
        # tkinter não é thread-safe: a thread de download só escreve na fila, e a tela lê daqui
        while not self.mensagens.empty():
            tipo, *dados = self.mensagens.get()
            if tipo == "barra":
                self.barra.set(dados[0])
                self.status.configure(text=f"{dados[1]} — {dados[0]:.0%}")
                continue
            if tipo == "fim":
                self.botao.configure(state="normal", text="Baixar")
                self.barra.set(1)
                self.status.configure(text=dados[0])
            self.saida.configure(state="normal")
            self.saida.insert("end", dados[0] + "\n")
            self.saida.see("end")
            self.saida.configure(state="disabled")
        self.after(100, self.atualizar)


if __name__ == "__main__":
    App().mainloop()
