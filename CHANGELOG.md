# Changelog

Todas as mudanças importantes do Baixaí ficam registradas aqui.
O formato segue o [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e as versões seguem o [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [1.3.0] - 2026-10-27

### Corrigido
- Vídeos diferentes com o mesmo título eram pulados como "já baixados". Agora o nome do arquivo inclui o ID do vídeo, ex.: `Intro [AAA].mp4`.
- A barra de progresso ficava cheia mesmo quando todos os downloads falhavam.

### Segurança
- O build confere a impressão digital (SHA256) do FFmpeg antes de colocá-lo dentro do `.exe`.
- O build para se a versão não for gravada no programa ou se a janela não abrir, em vez de publicar um `.exe` quebrado.

## [1.2.0] - 2026-10-27

### Adicionado
- Aviso de nova versão: ao abrir, o programa consulta o GitHub e mostra um botão verde se houver atualização.
- Licença MIT.

## [1.1.0] - 2026-10-27

### Adicionado
- Interface nova (customtkinter), que segue o tema claro/escuro do Windows.
- Barra de progresso com o título do vídeo e o andamento ("Link 2 de 5", "vídeo 3 de 20").
- FFmpeg embutido no `.exe`: não precisa instalar mais nada.

## [1.0.0] - 2026-10-27

### Adicionado
- Primeira versão: baixar vários links de uma vez, escolher a pasta, opção de só áudio (MP3) e de baixar a playlist inteira.
- `.exe` gerado e publicado automaticamente pelo GitHub a cada tag.

[1.3.0]: https://github.com/natanvferreira/Baixai/releases/tag/v1.3.0
[1.2.0]: https://github.com/natanvferreira/Baixai/releases/tag/v1.2.0
[1.1.0]: https://github.com/natanvferreira/Baixai/releases/tag/v1.1.0
[1.0.0]: https://github.com/natanvferreira/Baixai/releases/tag/v1.0.0
