"""
Peanut OS Compact v0.1.0 Concept

Um mini OS simulado em terminal, feito em Python.
Esta versão é propositalmente básica: boot, estado do sistema,
hora, bateria, menu principal e modo recovery.
"""

from __future__ import annotations

import os
import platform
import random
import time
from datetime import datetime

VERSION = "0.1.0 Concept"
SYSTEM_NAME = "Peanut OS Compact"


class PeanutCompact:
    def __init__(self) -> None:
        self.battery = random.randint(25, 95)
        self.state = "desligado"
        self.running = True

    def clear(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def now(self) -> str:
        return datetime.now().strftime("%H:%M")

    def header(self) -> None:
        print("=" * 54)
        print(f"{SYSTEM_NAME} - v{VERSION}")
        print("=" * 54)
        print(f"Bateria: {self.battery}%")
        print(f"Hora: {self.now()}")
        print(f"Estado do sistema: {self.state}")
        print("=" * 54)
        print()

    def pause(self) -> None:
        input("\nPressione ENTER para continuar...")

    def boot_screen(self) -> None:
        self.state = "ligando"
        self.clear()
        self.header()
        steps = [
            "Carregando nucleo Compact...",
            "Verificando interface de terminal...",
            "Preparando menu principal...",
            "Inicializacao concluida.",
        ]
        for step in steps:
            print(f"> {step}")
            time.sleep(0.5)
        self.state = "ligado"
        self.pause()

    def shutdown(self) -> None:
        self.state = "encerrando"
        self.clear()
        self.header()
        print("Encerrando o Peanut OS Compact...")
        time.sleep(0.8)
        self.state = "desligado"
        self.running = False

    def recovery_mode(self) -> None:
        self.state = "recovery"
        while True:
            self.clear()
            self.header()
            print("MODO RECOVERY")
            print()
            print("[1] Ver diagnostico basico")
            print("[2] Reiniciar sistema")
            print("[3] Desligar")
            print("[4] Voltar para tela inicial")
            choice = input("\nEscolha uma opcao: ").strip()

            if choice == "1":
                self.diagnostics()
            elif choice == "2":
                self.reboot()
                return
            elif choice == "3":
                self.shutdown()
                return
            elif choice == "4":
                self.state = "desligado"
                return
            else:
                print("Opcao invalida.")
                self.pause()

    def diagnostics(self) -> None:
        self.clear()
        self.header()
        print("DIAGNOSTICO BASICO")
        print()
        print(f"Sistema: {SYSTEM_NAME}")
        print(f"Versao: {VERSION}")
        print(f"Python: {platform.python_version()}")
        print(f"Plataforma: {platform.system()} {platform.release()}")
        print(f"Maquina: {platform.machine()}")
        print(f"Bateria simulada: {self.battery}%")
        print("Status: nenhum erro critico detectado")
        self.pause()

    def reboot(self) -> None:
        self.state = "reiniciando"
        self.clear()
        self.header()
        print("Reiniciando...")
        time.sleep(0.8)
        self.boot_screen()

    def system_info(self) -> None:
        self.clear()
        self.header()
        print("INFORMACOES DO SISTEMA")
        print()
        print(f"Nome: {SYSTEM_NAME}")
        print(f"Versao: {VERSION}")
        print(f"Estado: {self.state}")
        print(f"Python: {platform.python_version()}")
        print(f"Sistema hospedeiro: {platform.system()} {platform.release()}")
        print()
        print("Observacao: esta e uma simulacao educacional em terminal.")
        self.pause()

    def main_menu(self) -> None:
        while self.running and self.state == "ligado":
            self.clear()
            self.header()
            print("MENU PRINCIPAL")
            print()
            print("[1] Informacoes do sistema")
            print("[2] Reiniciar")
            print("[3] Entrar em modo recovery")
            print("[4] Desligar")
            choice = input("\nEscolha uma opcao: ").strip()

            if choice == "1":
                self.system_info()
            elif choice == "2":
                self.reboot()
            elif choice == "3":
                self.recovery_mode()
                if self.running and self.state == "desligado":
                    return
            elif choice == "4":
                self.shutdown()
            else:
                print("Opcao invalida.")
                self.pause()

    def start_screen(self) -> None:
        while self.running:
            self.clear()
            self.header()
            print("[1] Ligar")
            print("[2] Entrar em modo recovery")
            print("[3] Sair")
            choice = input("\nEscolha uma opcao: ").strip()

            if choice == "1":
                self.boot_screen()
                self.main_menu()
            elif choice == "2":
                self.recovery_mode()
            elif choice == "3":
                self.shutdown()
            else:
                print("Opcao invalida.")
                self.pause()


def main() -> None:
    PeanutCompact().start_screen()


if __name__ == "__main__":
    main()
