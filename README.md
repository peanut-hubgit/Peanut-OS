# PeanutOS Classic 🥜

O **PeanutOS Classic** é uma experiência de sistema operacional em terminal, desenvolvida em Python para fins educacionais. Ele não substitui Windows, Linux ou macOS: roda como um programa dentro do sistema hospedeiro.

## Recursos atuais

- Shell interativo em português;
- informações do dispositivo e da versão do Python;
- data e hora;
- calculadora segura;
- listagem de arquivos;
- comandos `eco`, `limpar`, `ajuda` e `sair`;
- estrutura modular pronta para receber novos aplicativos.

## Requisitos

- Python 3.10 ou superior.

O projeto funciona somente com a biblioteca padrão. `rich`, `colorama` e `pyfiglet` ficam reservados para melhorias visuais futuras.

## Instalação

### Windows

```powershell
winget install Python.Python.3.12
git clone https://github.com/peanut-hubgit/Peanut-OS.git
cd Peanut-OS
python main.py
```

### macOS

O comando abaixo exige o Homebrew:

```bash
brew install python git
git clone https://github.com/peanut-hubgit/Peanut-OS.git
cd Peanut-OS
python3 main.py
```

### Android com Termux

```bash
pkg update && pkg upgrade -y
pkg install python git -y
git clone https://github.com/peanut-hubgit/Peanut-OS.git
cd Peanut-OS
python main.py
```

## Comandos

| Comando | Função |
|---|---|
| `ajuda` | Mostra os comandos disponíveis |
| `sobre` | Exibe informações do projeto |
| `info` | Mostra informações do dispositivo |
| `hora` | Exibe data e hora |
| `calc 2 + 2` | Calcula uma expressão matemática |
| `listar` | Lista os arquivos da pasta atual |
| `eco texto` | Repete um texto |
| `limpar` | Limpa o terminal |
| `sair` | Encerra o PeanutOS |

## Estrutura

```text
Peanut-OS/
├── main.py
├── peanut_os/
│   ├── __init__.py
│   ├── shell.py
│   └── apps/
│       ├── __init__.py
│       └── calculator.py
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

## Contribuição

Contribuições são bem-vindas. Builds e forks distribuídos devem manter o código-fonte disponível conforme os termos da GPL v3.

## Comunidade

- Discord oficial: https://discord.gg/wrSMwXHw

## Licença

Distribuído sob a **GNU General Public License v3.0**. Consulte o arquivo [`LICENSE`](LICENSE).
