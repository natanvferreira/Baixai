"""Baixaí - interface simples para baixar vídeos do YouTube com yt-dlp."""
import queue
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, scrolledtext

import yt_dlp


def baixar(links, pasta, log):
    """Baixa cada link em `pasta`; um link com erro não interrompe os outros. Retorna os que falharam."""
    opcoes = {
        "outtmpl": str(Path(pasta) / "%(title)s.%(ext)s"),
        "post_hooks": [lambda arquivo: log(f"  ✔ {Path(arquivo).name}")],
        "quiet": True,
        "noprogress": True,
        "no_warnings": True,
    }
    falhas = []
    with yt_dlp.YoutubeDL(opcoes) as ydl:
        for i, link in enumerate(links, 1):
            log(f"[{i}/{len(links)}] {link}")
            try:
                ydl.download([link])
            except Exception as e:
                log(f"  ✖ Erro: {e}")
                falhas.append(link)
    return falhas


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Baixaí - Baixar vídeos do YouTube")
        self.geometry("700x550")
        self.mensagens = queue.Queue()

        tk.Label(self, text="Cole os links (um por linha):").pack(anchor="w", padx=10, pady=(10, 0))
        self.links = scrolledtext.ScrolledText(self, height=10)
        self.links.pack(fill="both", expand=True, padx=10)

        linha = tk.Frame(self)
        linha.pack(fill="x", padx=10, pady=10)
        tk.Label(linha, text="Pasta:").pack(side="left")
        self.pasta = tk.StringVar(value=str(Path.home() / "Downloads"))
        tk.Entry(linha, textvariable=self.pasta).pack(side="left", fill="x", expand=True, padx=5)
        tk.Button(linha, text="Escolher...", command=self.escolher_pasta).pack(side="left")

        self.botao = tk.Button(self, text="Baixar", font=("Segoe UI", 12, "bold"), command=self.iniciar)
        self.botao.pack(pady=(0, 10))

        self.saida = scrolledtext.ScrolledText(self, height=10, state="disabled")
        self.saida.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.after(100, self.atualizar_log)

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
        self.botao.config(state="disabled", text="Baixando...")
        threading.Thread(target=self.trabalhar, args=(links, pasta), daemon=True).start()

    def trabalhar(self, links, pasta):
        falhas = baixar(links, pasta, self.mensagens.put)
        self.mensagens.put(f"\nConcluído! {len(links) - len(falhas)} de {len(links)} baixados.\n")
        self.mensagens.put(None)  # sinaliza fim

    def atualizar_log(self):
        # tkinter não é thread-safe: a thread de download só escreve na fila, e a tela lê daqui
        while not self.mensagens.empty():
            msg = self.mensagens.get()
            if msg is None:
                self.botao.config(state="normal", text="Baixar")
                continue
            self.saida.config(state="normal")
            self.saida.insert("end", msg + "\n")
            self.saida.see("end")
            self.saida.config(state="disabled")
        self.after(100, self.atualizar_log)


if __name__ == "__main__":
    App().mainloop()
