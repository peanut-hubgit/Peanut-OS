"""
Peanut OS Compact v0.2.0 Concept

Um mini OS simulado em terminal, feito em Python.
Esta versão adiciona sistema de notificações e memória armazenada
em arquivo local, mantendo a ideia básica de boot, estado do sistema,
hora, bateria, menu principal e modo recovery.
"""

from __future__ import annotations

import json
import os
import platform
import random
import time
from datetime import datetime
from pathlib import Path
from typing import Any

VERSION = "0.2.0 Concept"
SYSTEM_NAME = "Peanut OS Compact"
MEMORY_FILE = Path(__file__).with_name("peanut_memory.json")


class PeanutCompact:
    def __init__(self) -> None:
        self.memory = self.load_memory()
        self.battery = self.memory.get("battery", random.randint(25, 95))
        self.state = self.memory.get("last_state", "desligado")
        if self.state not in ["desligado", "ligando", "ligado", "recovery", "reiniciando", "encerrando"]:
            self.state = "desligado"
        self.running = True
        self.memory["boot_count"] = int(self.memory.get("boot_count", 0))
        self.memory.setdefault("username", "Usuario Compact")
        self.memory.setdefault("notifications", [])
        self.memory.setdefault("history", [])
        self.add_notification("Sistema pronto para iniciar.", category="sistema")
        self.save_memory()

    def default_memory(self) -> dict[str, Any]:
        return {
            "username": "Usuario Compact",
            "battery": random.randint(25, 95),
            "last_state": "desligado",
            "boot_count": 0,
            "notifications": [],
            "history": [],
        }

    def load_memory(self) -> dict[str, Any]:
        if not MEMORY_FILE.exists():
            return self.default_memory()
        try:
            with MEMORY_FILE.open("r", encoding="utf-8") as file:
                data = json.load(file)
            if isinstance(data, dict):
                return {**self.default_memory(), **data}
        except (json.JSONDecodeError, OSError):
            pass
        return self.default_memory()

    def save_memory(self) -> None:
        self.memory["battery"] = self.battery
        self.memory["last_state"] = self.state
        try:
            with MEMORY_FILE.open("w", encoding="utf-8") as file:
                json.dump(self.memory, file, ensure_ascii=False, indent=2)
        except OSError:
            print("Aviso: nao foi possivel salvar a memoria local.")

    def add_history(self, action: str) -> None:
        history = self.memory.setdefault("history", [])
        history.append({"time": self.timestamp(), "action": action})
        if len(history) > 20:
            del history[:-20]

    def add_notification(self, message: str, category: str = "geral") -> None:
        notifications = self.memory.setdefault("notifications", [])
        notifications.append(
            {
                "id": len(notifications) + 1,
                "time": self.timestamp(),
                "category": category,
                "message": message,
                "read": False,
            }
        )
        if len(notifications) > 30:
            del notifications[:-30]

    def unread_count(self) -> int:
        return sum(1 for item in self.memory.get("notifications", []) if not item.get("read", False))

    def clear(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def now(self) -> str:
        return datetime.now().strftime("%H:%M")

    def timestamp(self) -> str:
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def header(self) -> None:
        print("=" * 58)
        print(f"{SYSTEM_NAME} - v{VERSION}")
        print("=" * 58)
        print(f"Usuario: {self.memory.get('username', 'Usuario Compact')}")
        print(f"Bateria: {self.battery}%")
        print(f"Hora: {self.now()}")
        print(f"Estado do sistema: {self.state}")
        print(f"Notificacoes nao lidas: {self.unread_count()}")
        print("=" * 58)
        print()

    def pause(self) -> None:
        input("\nPressione ENTER para continuar...")

    def boot_screen(self) -> None:
        self.state = "ligando"
        self.add_history("Boot iniciado")
        self.save_memory()
        self.clear()
        self.header()
        steps = [
            "Carregando nucleo Compact...",
            "Lendo memoria armazenada...",
            "Preparando notificacoes...",
            "Verificando interface de terminal...",
            "Preparando menu principal...",
            "Inicializacao concluida.",
        ]
        for step in steps:
            print(f"> {step}")
            time.sleep(0.45)
        self.state = "ligado"
        self.memory["boot_count"] = int(self.memory.get("boot_count", 0)) + 1
        self.add_notification("Peanut OS Compact foi ligado com sucesso.", category="boot")
        self.add_history("Boot concluido")
        self.save_memory()
        self.pause()

    def shutdown(self) -> None:
        self.state = "encerrando"
        self.add_history("Sistema encerrado")
        self.save_memory()
        self.clear()
        self.header()
        print("Encerrando o Peanut OS Compact...")
        time.sleep(0.8)
        self.state = "desligado"
        self.save_memory()
        self.running = False

    def recovery_mode(self) -> None:
        self.state = "recovery"
        self.add_notification("Modo recovery acessado.", category="recovery")
        self.add_history("Recovery acessado")
        self.save_memory()
        while True:
            self.clear()
            self.header()
            print("MODO RECOVERY")
            print()
            print("[1] Ver diagnostico basico")
            print("[2] Reiniciar sistema")
            print("[3] Desligar")
            print("[4] Limpar notificacoes")
            print("[5] Resetar memoria armazenada")
            print("[6] Voltar para tela inicial")
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
                self.clear_notifications()
            elif choice == "5":
                self.reset_memory()
                return
            elif choice == "6":
                self.state = "desligado"
                self.save_memory()
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
        print(f"Arquivo de memoria: {MEMORY_FILE.name}")
        print(f"Boots registrados: {self.memory.get('boot_count', 0)}")
        print(f"Notificacoes salvas: {len(self.memory.get('notifications', []))}")
        print("Status: nenhum erro critico detectado")
        self.pause()

    def reboot(self) -> None:
        self.state = "reiniciando"
        self.add_notification("Reinicializacao solicitada.", category="sistema")
        self.add_history("Reinicializacao solicitada")
        self.save_memory()
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
        print(f"Arquivo de memoria: {MEMORY_FILE}")
        print()
        print("Observacao: esta e uma simulacao educacional em terminal.")
        self.pause()

    def notifications_menu(self) -> None:
        while True:
            self.clear()
            self.header()
            print("CENTRAL DE NOTIFICACOES")
            print()
            notifications = self.memory.get("notifications", [])
            if not notifications:
                print("Nenhuma notificacao salva.")
            else:
                for item in notifications[-10:]:
                    status = "lida" if item.get("read") else "nova"
                    print(f"#{item.get('id')} [{status}] {item.get('time')} - {item.get('category')}")
                    print(f"  {item.get('message')}")
                    print()
            print("[1] Marcar todas como lidas")
            print("[2] Criar notificacao de teste")
            print("[3] Limpar notificacoes")
            print("[4] Voltar")
            choice = input("\nEscolha uma opcao: ").strip()

            if choice == "1":
                for item in self.memory.get("notifications", []):
                    item["read"] = True
                self.add_history("Notificacoes marcadas como lidas")
                self.save_memory()
            elif choice == "2":
                self.add_notification("Esta e uma notificacao de teste do Peanut Compact.", category="teste")
                self.add_history("Notificacao de teste criada")
                self.save_memory()
            elif choice == "3":
                self.clear_notifications()
            elif choice == "4":
                return
            else:
                print("Opcao invalida.")
                self.pause()

    def clear_notifications(self) -> None:
        self.memory["notifications"] = []
        self.add_history("Notificacoes limpas")
        self.save_memory()
        print("Notificacoes limpas.")
        self.pause()

    def memory_menu(self) -> None:
        while True:
            self.clear()
            self.header()
            print("MEMORIA ARMAZENADA")
            print()
            print(f"Arquivo: {MEMORY_FILE}")
            print(f"Usuario salvo: {self.memory.get('username')}")
            print(f"Boots registrados: {self.memory.get('boot_count', 0)}")
            print(f"Ultimo estado salvo: {self.memory.get('last_state')}")
            print(f"Historico salvo: {len(self.memory.get('history', []))} eventos")
            print()
            print("[1] Alterar nome do usuario")
            print("[2] Ver historico")
            print("[3] Resetar memoria")
            print("[4] Voltar")
            choice = input("\nEscolha uma opcao: ").strip()

            if choice == "1":
                new_name = input("Novo nome do usuario: ").strip()
                if new_name:
                    self.memory["username"] = new_name
                    self.add_notification(f"Nome do usuario alterado para {new_name}.", category="memoria")
                    self.add_history("Nome do usuario alterado")
                    self.save_memory()
            elif choice == "2":
                self.show_history()
            elif choice == "3":
                self.reset_memory()
                return
            elif choice == "4":
                return
            else:
                print("Opcao invalida.")
                self.pause()

    def show_history(self) -> None:
        self.clear()
        self.header()
        print("HISTORICO DO SISTEMA")
        print()
        history = self.memory.get("history", [])
        if not history:
            print("Nenhum evento salvo.")
        else:
            for item in history[-15:]:
                print(f"- {item.get('time')}: {item.get('action')}")
        self.pause()

    def reset_memory(self) -> None:
        confirm = input("Digite RESET para apagar a memoria armazenada: ").strip()
        if confirm != "RESET":
            print("Reset cancelado.")
            self.pause()
            return
        self.memory = self.default_memory()
        self.battery = self.memory["battery"]
        self.state = "desligado"
        self.add_notification("Memoria armazenada foi recriada.", category="recovery")
        self.save_memory()
        print("Memoria resetada.")
        self.pause()

    def main_menu(self) -> None:
        while self.running and self.state == "ligado":
            self.clear()
            self.header()
            print("MENU PRINCIPAL")
            print()
            print("[1] Informacoes do sistema")
            print("[2] Central de notificacoes")
            print("[3] Memoria armazenada")
            print("[4] Reiniciar")
            print("[5] Entrar em modo recovery")
            print("[6] Desligar")
            choice = input("\nEscolha uma opcao: ").strip()

            if choice == "1":
                self.system_info()
            elif choice == "2":
                self.notifications_menu()
            elif choice == "3":
                self.memory_menu()
            elif choice == "4":
                self.reboot()
            elif choice == "5":
                self.recovery_mode()
                if self.running and self.state == "desligado":
                    return
            elif choice == "6":
                self.shutdown()
            else:
                print("Opcao invalida.")
                self.pause()

    def start_screen(self) -> None:
        self.state = "desligado" if self.state in ["encerrando", "ligado", "ligando", "reiniciando"] else self.state
        self.save_memory()
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
