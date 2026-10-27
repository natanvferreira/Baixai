# Baixaí

Programinha com interface gráfica para baixar **vários vídeos do YouTube de uma vez**, usando o [yt-dlp](https://github.com/yt-dlp/yt-dlp).

Cole os links, escolha a pasta, clique em **Baixar**. Pronto.

## Instalação (Windows)

1. **Instale o Python** (3.9 ou mais novo): baixe em <https://www.python.org/downloads/> e, no instalador, marque **"Add python.exe to PATH"**.
   Ou, pelo terminal:
   ```
   winget install Python.Python.3.13
   ```
2. **Instale o FFmpeg** (recomendado: permite juntar vídeo e áudio na melhor qualidade):
   ```
   winget install Gyan.FFmpeg
   ```
   Sem o FFmpeg o programa funciona, mas baixa numa qualidade menor.
3. **Baixe este projeto**: no GitHub, clique em **Code → Download ZIP** e extraia, ou:
   ```
   git clone https://github.com/<seu-usuario>/Baixai.git
   ```
4. **Instale as dependências**, abrindo um terminal dentro da pasta do projeto:
   ```
   pip install -r requirements.txt
   ```

## Como usar

1. Dentro da pasta do projeto, rode:
   ```
   python baixai.py
   ```
   (ou dê dois cliques em `baixai.py`)
2. Cole os links na caixa de cima, **um por linha**.
3. Em **Pasta**, clique em **Escolher...** e selecione onde os vídeos serão salvos (o padrão é a pasta *Downloads*).
4. Clique em **Baixar** e acompanhe o andamento na caixa de baixo.

Se algum link der erro, os outros continuam sendo baixados normalmente; no fim aparece quantos deram certo.

## Problemas comuns

- **Um vídeo que funcionava parou de baixar**: o YouTube muda com frequência; atualize o yt-dlp:
  ```
  pip install -U yt-dlp
  ```
- **"python não é reconhecido"**: o Python não foi adicionado ao PATH. Reinstale marcando a opção **"Add python.exe to PATH"**.

## Teste

Com internet, rode `python test_baixai.py`: ele baixa um vídeo curto numa pasta temporária e confere que um link inválido é reportado como falha.
