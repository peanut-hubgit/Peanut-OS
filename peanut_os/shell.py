from __future__ import annotations

import os
import platform
from datetime import datetime
from pathlib import Path
from typing import Callable

from peanut_os import __version__
from peanut_os.apps.calculator import calculate


class PeanutShell:
    """Shell simples e extensível do PeanutOS Classic."""

    def __init__(self) -> None:
        self.running = True
        self.commands: dict[str, Callable[[list[str]], None]] = {
            "ajuda": self._help,
            "help": self._help,
            "sobre": self._about,
            "info": self._system_info,
            "hora": self._time,
            "limpar": self._clear,
            "clear": self._clear,
            "eco": self._echo,
            "calc": self._calculator,
            "listar": self._list_files,
            "ls": self._list_files,
            "sair": self._exit,
            "exit": self._exit,
        }

    def run(self) -> None:
        self._banner()
        while self.running:
            try:
                raw = input("peanut@classic > ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nEncerrando o PeanutOS...")
                break

            if not raw:
                continue

            name, *args = raw.split()
            command = self.commands.get(name.lower())
            if command is None:
                print(f"Comando desconhecido: {name}. Digite 'ajuda'.")
                continue

            try:
                command(args)
            except Exception as error:
                print(f"Erro: {error}")

    @staticmethod
    def _banner() -> None:
        print("=" * 46)
        print(f" PeanutOS Classic v{__version__} — terminal Python")
        print(" Digite 'ajuda' para ver os comandos.")
        print("=" * 46)

    def _help(self, _: list[str]) -> None:
        print(
            "\nComandos disponíveis:\n"
            "  ajuda        Mostra esta lista\n"
            "  sobre        Exibe informações do projeto\n"
            "  info         Mostra informações do dispositivo\n"
            "  hora         Exibe data e hora atuais\n"
            "  limpar       Limpa o terminal\n"
            "  eco TEXTO    Repete um texto\n"
            "  calc CONTA   Calculadora segura (ex.: calc 2 + 2)\n"
            "  listar       Lista arquivos da pasta atual\n"
            "  sair         Encerra o sistema\n"
        )

    def _about(self, _: list[str]) -> None:
        print(f"PeanutOS Classic v{__version__}")
        print("Uma experiência de sistema em terminal, feita em Python.")
        print("Projeto educacional de código aberto sob GPL-3.0.")

    def _system_info(self, _: list[str]) -> None:
        print(f"Sistema hospedeiro: {platform.system()} {platform.release()}")
        print(f"Arquitetura: {platform.machine() or 'desconhecida'}")
        print(f"Python: {platform.python_version()}")
        print(f"Diretório atual: {Path.cwd()}")

    def _time(self, _: list[str]) -> None:
        print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

    def _clear(self, _: list[str]) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def _echo(self, args: list[str]) -> None:
        print(" ".join(args))

    def _calculator(self, args: list[str]) -> None:
        if not args:
            print("Uso: calc 2 + 2")
            return
        expression = " ".join(args)
        print(calculate(expression))

    def _list_files(self, _: list[str]) -> None:
        entries = sorted(Path.cwd().iterdir(), key=lambda item: (not item.is_dir(), item.name.lower()))
        if not entries:
            print("Pasta vazia.")
            return
        for entry in entries:
            marker = "[DIR]" if entry.is_dir() else "     "
            print(f"{marker} {entry.name}")

    def _exit(self, _: list[str]) -> None:
        print("Até a próxima. 🥜")
        self.running = False
