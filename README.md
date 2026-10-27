# Baixaí

Programinha com interface gráfica para baixar **vários vídeos do YouTube de uma vez**, usando o [yt-dlp](https://github.com/yt-dlp/yt-dlp).

Cole os links, escolha a pasta, clique em **Baixar**. Pronto. Também baixa **só o áudio em MP3** e **playlists inteiras**.

## Jeito mais fácil: o .exe (Windows)

1. Baixe o `Baixai.exe` na página de [Releases](https://github.com/natanvferreira/Baixa-/releases) do projeto.
2. **Instale o FFmpeg** (necessário para MP3 e para a melhor qualidade de vídeo). Abra o *Terminal* e rode:
   ```
   winget install Gyan.FFmpeg
   ```
3. Dê dois cliques no `Baixai.exe`.

> O Windows pode mostrar "O Windows protegeu o computador" porque o programa não é assinado. Clique em **Mais informações → Executar assim mesmo**.

## Rodando pelo código (Python)

1. **Instale o Python** (3.9 ou mais novo): baixe em <https://www.python.org/downloads/> e, no instalador, marque **"Add python.exe to PATH"**. Ou: `winget install Python.Python.3.13`
2. **Instale o FFmpeg**: `winget install Gyan.FFmpeg`
3. **Baixe este projeto**: no GitHub, clique em **Code → Download ZIP** e extraia, ou:
   ```
   git clone https://github.com/natanvferreira/Baixa-.git
   ```
4. **Instale as dependências**, num terminal dentro da pasta do projeto:
   ```
   pip install -r requirements.txt
   ```
5. **Abra o programa**:
   ```
   python baixai.py
   ```

## Como usar

1. Cole os links na caixa de cima, **um por linha**.
2. Em **Pasta**, clique em **Escolher...** e selecione onde salvar (o padrão é a pasta *Downloads*).
3. Marque as opções, se quiser:
   - **Só o áudio (MP3)**: salva apenas o áudio, em `.mp3`.
   - **Baixar a playlist inteira**: quando o link for de um vídeo dentro de uma playlist (tem `&list=` no endereço), baixa a playlist toda em vez de só aquele vídeo. Links de playlist (`youtube.com/playlist?list=...`) sempre baixam a playlist inteira.
4. Clique em **Baixar** e acompanhe o andamento na caixa de baixo.

Se algum link der erro, os outros continuam sendo baixados normalmente; no fim aparece quantos deram certo.

## Problemas comuns

- **Um vídeo que funcionava parou de baixar**: o YouTube muda com frequência.
  - Pelo código: `pip install -U yt-dlp`
  - Pelo .exe: baixe a versão mais nova na página de Releases.
- **Erro falando de "ffmpeg" ou "ffprobe"**: o FFmpeg não está instalado (veja acima). Depois de instalar, feche e abra o programa de novo.
- **"python não é reconhecido"**: o Python não foi adicionado ao PATH. Reinstale marcando **"Add python.exe to PATH"**.

## Para desenvolvedores

**Teste** (precisa de internet e FFmpeg): `python test_baixai.py`. Ele baixa um vídeo curto, em vídeo e em MP3, numa pasta temporária e confere que um link inválido é reportado como falha.

**Publicar uma versão nova** (o GitHub gera o `.exe` com o yt-dlp mais recente e cria a Release sozinho):
```
git tag v1.1.0
git push origin v1.1.0
```

**Gerar o .exe localmente**:
```
pip install pyinstaller
pyinstaller --onefile --windowed --name Baixai baixai.py
```
O arquivo sai em `dist/Baixai.exe`.
