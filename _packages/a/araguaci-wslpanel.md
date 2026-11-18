---
title: wslpanel
description: "Painel do WSL: CPU, memória, disco, logs e programas instalados. Resources and packages for a WSL distro."
license: MIT
author: araguaci
author_github: araguaci
repository: https://github.com/araguaci/wslpanel
keywords:
  - gtk3
date: 2026-11-18
updated_at: 2026-11-18T16:28:44+00:00
last_sync: 2026-11-18T16:28:44Z
package_kind: binary
has_library: false
has_binary: true
has_distributable_binary: true
binary_count: 1
distributable_binary_count: 1
multiple_binaries: false
is_sponsor: false
sync_priority: normal
sync_source: zigistry
permalink: /packages/araguaci/wslpanel/
---

# wslpanel

[English](README-EN.md) · [Español](README-ES.md)

Painel da distro WSL: consumo de CPU, memória, disco, `/tmp` e `/var/log`, no ritmo de um segundo, e os programas instalados pelo dpkg. A versão **0.2.0** (2026-11-18) aparece no rodapé.

Repositório: <https://github.com/araguaci/wslpanel>

![Painel do WSL com Recursos, Processos, Docker, Logs e Programas](docs/wslpanel-dev.jpg)

## Recursos

- **Recursos** (página inicial): percentual de CPU, carga, uma barra por núcleo, RAM, swap, disco de `/`, tamanho de `/tmp` e de `/var/log`, com o histórico recente.
- **Limpar /tmp**: pede confirmação e apaga arquivos e pastas comuns. Ficam os sockets da sessão gráfica: `.X11-unix`, `.ICE-unix`, `.XIM-unix` e `.font-unix`.
- **Limpar logs**: pede confirmação e só remove arquivos já rodados (`.gz`, `.xz`, `.bz2`, `.old` ou nome terminado em `.<número>`, como `syslog.1`). O log ativo permanece. Sem permissão, o painel avisa e não pede senha.
- **Processos**: nome, PID, fatia de CPU, RSS e estado, lidos de `/proc`. Encerrar envia SIGTERM, com confirmação. O processo 1 e o próprio painel ficam de fora.
- **Docker**: a aba só aparece se o cliente `docker` estiver instalado. Mostra cada container em execução, com CPU e memória lidas do cgroup, PIDs e o estado do `docker ps`.
- **Logs**: o fim dos arquivos de texto em `/var/log` (também um nível abaixo, como `apt/history.log`). O número de linhas começa em 50 e sobe de 50 em 50, até 2000. Arquivos compactados e os binários `wtmp`, `btmp`, `lastlog` e `faillog` ficam de fora.
- **Programas**: pacotes desta distro Debian/Ubuntu. Busca, filtros (programas, manuais, todos, atualizações, órfãos, bibliotecas), ordenação por nome, tamanho ou data. O detalhe mostra versão, origem, tamanho, dependências e quem exige o pacote.
- Atualizar, remover e limpar órfãos pedem confirmação num diálogo e rodam `sudo -n apt-get`. A senha não fica guardada: se o sudo pedir senha, o comando aparece no rodapé, com **Copiar**. Pacote essencial ou de prioridade obrigatória não é removido.
- **Tema**: Auto segue o sistema. Claro e Escuro ficam no rodapé, ao lado de PT, EN e ES.
- **Idiomas**: português (pt_BR), inglês e espanhol. O idioma segue `WSLPANEL_LANG`, depois `LC_ALL`, `LC_MESSAGES` e `LANG`. Sem isso, a interface abre em português. Os botões PT, EN e ES no rodapé valem para a sessão.
- O rodapé mostra `wslpanel`, a versão de `build.zig.zon` e a data da release.

O que já entrou e o que vem depois está em [docs/PLANO.md](docs/PLANO.md).

## Requisitos

- Linux, inclusive uma distro Debian ou Ubuntu no WSL2. A aba Programas lê `/var/lib/dpkg/status`.
- [Zig 0.17.0](https://ziglang.org/download/0.17.0/).
- GTK 3 (`libgtk-3-0`) para a janela. No WSL2, o WSLg deixa `DISPLAY` definido.
- `sudo` para as ações de pacote. A limpeza de `/tmp` e `/var/log` usa as permissões do usuário.
- Uma tela. Sem GPU, o OpenGL não abre (`libEGL`, `ZINK`, `gdk_gl_context`) e a janela fecha. Nesse caso: `NANOUI_RENDERER=cpu ./zig-out/bin/wslpanel`.

## Instalar e executar

```sh
git clone https://github.com/araguaci/wslpanel
cd wslpanel
zig build -Doptimize=ReleaseSafe
./zig-out/bin/wslpanel
```

A primeira compilação baixa o [nanoui](https://github.com/justrach/nanoui) (MIT, Rach Pradhan), na revisão fixada em `build.zig.zon`.

No Debian ou Ubuntu:

```sh
sudo apt-get update
sudo apt-get install -y libgtk-3-0
```

Zig 0.17.0, se ainda não estiver no `PATH`:

```sh
mkdir -p "$HOME/.local"
curl -fL -o zig-x86_64-linux-0.17.0.tar.xz \
  https://ziglang.org/download/0.17.0/zig-x86_64-linux-0.17.0.tar.xz
tar -xJf zig-x86_64-linux-0.17.0.tar.xz -C "$HOME/.local"
export PATH="$HOME/.local/zig-x86_64-linux-0.17.0:$PATH"
```

`$HOME/.local` precisa existir antes do `tar`. O `export` vale neste terminal.

Outro idioma nesta execução:

```sh
WSLPANEL_LANG=en ./zig-out/bin/wslpanel
WSLPANEL_LANG=es ./zig-out/bin/wslpanel
WSLPANEL_LANG=pt_BR ./zig-out/bin/wslpanel
```

## Desenvolvimento

```sh
zig build test
zig build
./zig-out/bin/wslpanel --nanoui-snapshot=/tmp/wslpanel.png --nanoui-wait=2
```

`--nanoui-wait=2` deixa o medidor ler um segundo delta de `/proc/stat` antes do snapshot. A janela não é mostrada.

A versão publicada é a de `build.zig.zon`. A data do rodapé está em `src/meta.zig`. O histórico fica no [CHANGELOG.md](CHANGELOG.md). O passo a passo de versão, changelog e release está em [docs/RELEASE.md](docs/RELEASE.md).

## Licença

MIT. Veja [LICENSE](LICENSE). A interface é desenhada com o nanoui, que tem a própria licença MIT.
