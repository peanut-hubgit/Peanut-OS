"""
Peanut OS Compact v0.3.0 Concept

Mini OS simulado em terminal, feito em Python.
Esta versão foca no Bootloader: Secure Boot simulado, minigame de desbloqueio,
Custom Mods estilo Magisk, importação de módulos locais, animações coloridas e
modo Auto Destruction simulado apenas dentro do Peanut OS.
"""

from __future__ import annotations

import importlib.util
import json
import os
import platform
import random
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

VERSION = "0.3.0 Concept"
SYSTEM_NAME = "Peanut OS Compact"
BASE_DIR = Path(__file__).resolve().parent
MEMORY_FILE = BASE_DIR / "peanut_memory.json"
MODULES_DIR = BASE_DIR / "modules"


class Color:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"


class PeanutCompact:
    def __init__(self) -> None:
        MODULES_DIR.mkdir(exist_ok=True)
        self.memory = self.load_memory()
        self.battery = int(self.memory.get("battery", random.randint(25, 95)))
        self.state = self.memory.get("last_state", "desligado")
        self.running = True
        self.memory.setdefault("username", "Usuario Compact")
        self.memory.setdefault("notifications", [])
        self.memory.setdefault("history", [])
        self.memory.setdefault("boot_count", 0)
        self.memory.setdefault("secure_boot_unlocked", False)
        self.memory.setdefault("custom_mods_enabled", False)
        self.memory.setdefault("enabled_modules", [])
        self.memory.setdefault("destroyed", False)
        self.memory.setdefault("bootloader_attempts", 0)
        self.add_notification("Bootloader Compact pronto.", category="bootloader")
        self.save_memory()

    def default_memory(self) -> dict[str, Any]:
        return {
            "username": "Usuario Compact",
            "battery": random.randint(25, 95),
            "last_state": "desligado",
            "boot_count": 0,
            "notifications": [],
            "history": [],
            "secure_boot_unlocked": False,
            "custom_mods_enabled": False,
            "enabled_modules": [],
            "destroyed": False,
            "bootloader_attempts": 0,
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

    def timestamp(self) -> str:
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def add_history(self, action: str) -> None:
        history = self.memory.setdefault("history", [])
        history.append({"time": self.timestamp(), "action": action})
        if len(history) > 30:
            del history[:-30]

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
        if len(notifications) > 40:
            del notifications[:-40]

    def unread_count(self) -> int:
        return sum(1 for item in self.memory.get("notifications", []) if not item.get("read", False))

    def clear(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def now(self) -> str:
        return datetime.now().strftime("%H:%M")

    def c(self, text: str, color: str) -> str:
        return f"{color}{text}{Color.RESET}"

    def header(self) -> None:
        lock = "UNLOCKED" if self.memory.get("secure_boot_unlocked") else "LOCKED"
        mods = "ON" if self.memory.get("custom_mods_enabled") else "OFF"
        destroyed = "SIM" if self.memory.get("destroyed") else "NAO"
        print(self.c("=" * 64, Color.CYAN))
        print(self.c(f"{SYSTEM_NAME} - v{VERSION}", Color.BOLD + Color.YELLOW))
        print(self.c("=" * 64, Color.CYAN))
        print(f"Usuario: {self.memory.get('username', 'Usuario Compact')}")
        print(f"Bateria: {self.battery}% | Hora: {self.now()} | Estado: {self.state}")
        print(f"Secure Boot: {lock} | Custom Mods: {mods} | Destruction: {destroyed}")
        print(f"Notificacoes nao lidas: {self.unread_count()}")
        print(self.c("=" * 64, Color.CYAN))
        print()

    def pause(self) -> None:
        input("\nPressione ENTER para continuar...")

    def loading(self, title: str, steps: list[str], color: str = Color.GREEN, delay: float = 0.18) -> None:
        print(self.c(title, Color.BOLD + color))
        print()
        spinner = ["|", "/", "-", "\\"]
        for index, step in enumerate(steps):
            icon = spinner[index % len(spinner)]
            print(self.c(f" {icon} {step}", color))
            time.sleep(delay)
        print()

    def progress_bar(self, label: str, seconds: float = 1.2, color: str = Color.CYAN) -> None:
        print(label)
        total = 24
        for i in range(total + 1):
            filled = "#" * i
            empty = "." * (total - i)
            percent = int((i / total) * 100)
            print(f"\r{self.c('[', color)}{self.c(filled, color)}{empty}{self.c(']', color)} {percent}%", end="")
            time.sleep(seconds / total)
        print("\n")

    def bootloader_screen(self) -> None:
        while self.running:
            self.clear()
            self.state = "bootloader"
            self.save_memory()
            self.header()
            if self.memory.get("destroyed"):
                self.destroyed_screen()
                return
            print(self.c("BOOTLOADER COMPACT", Color.BOLD + Color.MAGENTA))
            print()
            print("[1] Boot normal")
            print("[2] Desbloquear Secure Boot (minigame)")
            print("[3] Custom Mods")
            print("[4] Modo Recovery")
            print("[5] Auto Destruction simulado")
            print("[6] Sair")
            choice = input("\nEscolha uma opcao: ").strip()
            if choice == "1":
                self.boot_screen()
                self.main_menu()
            elif choice == "2":
                self.secure_boot_minigame()
            elif choice == "3":
                self.custom_mods_menu()
            elif choice == "4":
                self.recovery_mode()
            elif choice == "5":
                self.auto_destruction()
            elif choice == "6":
                self.shutdown()
            else:
                print("Opcao invalida.")
                self.pause()

    def secure_boot_minigame(self) -> None:
        self.clear()
        self.header()
        print(self.c("MINIGAME: DESBLOQUEIO DO SECURE BOOT", Color.BOLD + Color.YELLOW))
        print()
        print("Digite a sequencia correta antes do sistema bloquear o token.")
        sequence = [random.choice(["A", "B", "X", "Y"]) for _ in range(5)]
        print("Sequencia:", " ".join(sequence))
        answer = input("Repita a sequencia separada por espaco: ").upper().strip().split()
        self.memory["bootloader_attempts"] = int(self.memory.get("bootloader_attempts", 0)) + 1
        if answer == sequence:
            self.memory["secure_boot_unlocked"] = True
            self.add_notification("Secure Boot desbloqueado. Custom Mods liberados.", category="bootloader")
            self.add_history("Secure Boot desbloqueado pelo minigame")
            self.loading("Validando token de desbloqueio...", ["Token aceito", "Bootloader aberto", "Custom Mods liberados"], Color.GREEN)
        else:
            self.add_notification("Falha ao desbloquear Secure Boot.", category="bootloader")
            self.add_history("Falha no minigame do Secure Boot")
            print(self.c("Sequencia incorreta. Secure Boot continua bloqueado.", Color.RED))
        self.save_memory()
        self.pause()

    def boot_screen(self) -> None:
        self.state = "ligando"
        self.add_history("Boot iniciado")
        self.save_memory()
        self.clear()
        self.header()
        steps = [
            "Inicializando Bootloader Compact...",
            "Verificando Secure Boot simulado...",
            "Lendo memoria armazenada...",
            "Carregando notificacoes...",
            "Preparando interface colorida...",
            "Importando modulos ativados...",
        ]
        self.loading("BOOT ANIMATION", steps, Color.CYAN, delay=0.24)
        self.load_enabled_modules()
        self.progress_bar("Finalizando boot", seconds=1.0, color=Color.GREEN)
        self.state = "ligado"
        self.memory["boot_count"] = int(self.memory.get("boot_count", 0)) + 1
        self.add_notification("Peanut OS Compact foi ligado com sucesso.", category="boot")
        self.add_history("Boot concluido")
        self.save_memory()
        self.pause()

    def load_enabled_modules(self) -> None:
        if not self.memory.get("custom_mods_enabled"):
            print(self.c("Custom Mods desativado. Nenhum modulo carregado.", Color.DIM))
            return
        enabled = self.memory.get("enabled_modules", [])
        if not enabled:
            print(self.c("Custom Mods ativo, mas nenhum modulo esta habilitado.", Color.DIM))
            return
        for module_file in enabled:
            module_path = MODULES_DIR / module_file
            if not module_path.exists() or module_path.suffix != ".py":
                print(self.c(f"Modulo ignorado: {module_file}", Color.RED))
                continue
            try:
                spec = importlib.util.spec_from_file_location(module_path.stem, module_path)
                if spec is None or spec.loader is None:
                    raise ImportError("spec invalido")
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_path.stem] = module
                spec.loader.exec_module(module)
                if hasattr(module, "activate"):
                    result = module.activate(self)
                    print(self.c(f"Modulo carregado: {module_file}", Color.GREEN))
                    if result:
                        self.add_notification(str(result), category="mod")
                else:
                    print(self.c(f"Modulo sem activate(): {module_file}", Color.YELLOW))
            except Exception as error:
                print(self.c(f"Erro ao carregar {module_file}: {error}", Color.RED))

    def list_modules(self) -> list[str]:
        return sorted(path.name for path in MODULES_DIR.glob("*.py") if path.name != "__init__.py")

    def custom_mods_menu(self) -> None:
        while True:
            self.clear()
            self.header()
            print(self.c("CUSTOM MODS - estilo Magisk do Peanut OS", Color.BOLD + Color.MAGENTA))
            print()
            if not self.memory.get("secure_boot_unlocked"):
                print(self.c("Secure Boot ainda esta bloqueado.", Color.RED))
                print("Desbloqueie pelo minigame para ativar Custom Mods.")
                self.pause()
                return
            modules = self.list_modules()
            enabled = set(self.memory.get("enabled_modules", []))
            print("[1] Ativar/desativar Custom Mods")
            print("[2] Listar modulos")
            print("[3] Habilitar modulo")
            print("[4] Desabilitar modulo")
            print("[5] Testar importacao agora")
            print("[6] Voltar")
            print()
            print(f"Modulos encontrados: {len(modules)} | Habilitados: {len(enabled)}")
            choice = input("\nEscolha uma opcao: ").strip()
            if choice == "1":
                self.memory["custom_mods_enabled"] = not self.memory.get("custom_mods_enabled")
                status = "ativado" if self.memory["custom_mods_enabled"] else "desativado"
                self.add_notification(f"Custom Mods {status}.", category="mod")
                self.add_history(f"Custom Mods {status}")
                self.save_memory()
            elif choice == "2":
                self.show_modules(modules, enabled)
            elif choice == "3":
                self.enable_module(modules)
            elif choice == "4":
                self.disable_module()
            elif choice == "5":
                self.load_enabled_modules()
                self.save_memory()
                self.pause()
            elif choice == "6":
                return
            else:
                print("Opcao invalida.")
                self.pause()

    def show_modules(self, modules: list[str], enabled: set[str]) -> None:
        self.clear()
        self.header()
        print("MODULOS DISPONIVEIS")
        print()
        if not modules:
            print("Nenhum modulo .py encontrado em editions/compact/modules.")
        for index, name in enumerate(modules, start=1):
            status = "ON" if name in enabled else "OFF"
            print(f"[{index}] {name} - {status}")
        self.pause()

    def enable_module(self, modules: list[str]) -> None:
        if not modules:
            print("Nenhum modulo disponivel.")
            self.pause()
            return
        self.show_modules(modules, set(self.memory.get("enabled_modules", [])))
        choice = input("Numero do modulo para habilitar: ").strip()
        if not choice.isdigit() or not (1 <= int(choice) <= len(modules)):
            print("Modulo invalido.")
            self.pause()
            return
        name = modules[int(choice) - 1]
        enabled = self.memory.setdefault("enabled_modules", [])
        if name not in enabled:
            enabled.append(name)
            self.add_notification(f"Modulo habilitado: {name}", category="mod")
            self.add_history(f"Modulo habilitado: {name}")
            self.save_memory()
        print("Modulo habilitado.")
        self.pause()

    def disable_module(self) -> None:
        enabled = self.memory.get("enabled_modules", [])
        if not enabled:
            print("Nenhum modulo habilitado.")
            self.pause()
            return
        for index, name in enumerate(enabled, start=1):
            print(f"[{index}] {name}")
        choice = input("Numero do modulo para desabilitar: ").strip()
        if not choice.isdigit() or not (1 <= int(choice) <= len(enabled)):
            print("Modulo invalido.")
            self.pause()
            return
        name = enabled.pop(int(choice) - 1)
        self.add_notification(f"Modulo desabilitado: {name}", category="mod")
        self.add_history(f"Modulo desabilitado: {name}")
        self.save_memory()
        print("Modulo desabilitado.")
        self.pause()

    def auto_destruction(self) -> None:
        self.clear()
        self.header()
        print(self.c("AUTO DESTRUCTION SIMULADO", Color.BOLD + Color.RED))
        print()
        print("Isso NAO mexe no aparelho real, disco, sistema operacional, boot real ou arquivos pessoais.")
        print("Apenas marca a memoria do Peanut OS como destruida, travando o boot simulado.")
        confirm = input("Digite DESTRUIR PEANUT para confirmar: ").strip()
        if confirm != "DESTRUIR PEANUT":
            print("Auto destruction cancelado.")
            self.pause()
            return
        for number in range(5, 0, -1):
            print(self.c(f"Auto destruction em {number}...", Color.RED))
            time.sleep(0.45)
        self.progress_bar("Corrompendo boot simulado", seconds=1.4, color=Color.RED)
        self.memory["destroyed"] = True
        self.state = "destruido"
        self.add_history("Auto destruction simulado executado")
        self.save_memory()
        self.destroyed_screen()

    def destroyed_screen(self) -> None:
        self.clear()
        print(self.c("!" * 64, Color.RED))
        print(self.c("PEANUT OS COMPACT NAO CONSEGUE INICIALIZAR", Color.BOLD + Color.RED))
        print(self.c("!" * 64, Color.RED))
        print()
        print("Estado: destruido dentro da simulacao")
        print("Motivo: Auto Destruction foi ativado")
        print()
        print("[1] Tentar recovery")
        print("[2] Sair")
        choice = input("\nEscolha uma opcao: ").strip()
        if choice == "1":
            self.recovery_mode()
        else:
            self.running = False

    def shutdown(self) -> None:
        self.state = "encerrando"
        self.add_history("Sistema encerrado")
        self.save_memory()
        self.clear()
        self.header()
        self.loading("Encerrando Peanut OS Compact...", ["Salvando memoria", "Fechando interface", "Sistema desligado"], Color.YELLOW)
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
            print(self.c("MODO RECOVERY", Color.BOLD + Color.BLUE))
            print()
            print("[1] Ver diagnostico basico")
            print("[2] Reiniciar sistema")
            print("[3] Limpar notificacoes")
            print("[4] Resetar memoria armazenada")
            print("[5] Reparar Auto Destruction simulado")
            print("[6] Desligar")
            print("[7] Voltar ao Bootloader")
            choice = input("\nEscolha uma opcao: ").strip()
            if choice == "1":
                self.diagnostics()
            elif choice == "2":
                self.boot_screen()
                return
            elif choice == "3":
                self.clear_notifications()
            elif choice == "4":
                self.reset_memory()
                return
            elif choice == "5":
                self.repair_destruction()
                return
            elif choice == "6":
                self.shutdown()
                return
            elif choice == "7":
                return
            else:
                print("Opcao invalida.")
                self.pause()

    def repair_destruction(self) -> None:
        confirm = input("Digite REPARAR para recuperar o boot simulado: ").strip()
        if confirm != "REPARAR":
            print("Reparo cancelado.")
            self.pause()
            return
        self.memory["destroyed"] = False
        self.state = "desligado"
        self.add_notification("Auto Destruction simulado foi reparado pelo recovery.", category="recovery")
        self.add_history("Auto Destruction simulado reparado")
        self.save_memory()
        print("Boot simulado reparado.")
        self.pause()

    def diagnostics(self) -> None:
        self.clear()
        self.header()
        print(self.c("DIAGNOSTICO BASICO", Color.BOLD + Color.GREEN))
        print()
        print(f"Sistema: {SYSTEM_NAME}")
        print(f"Versao: {VERSION}")
        print(f"Python: {platform.python_version()}")
        print(f"Plataforma: {platform.system()} {platform.release()}")
        print(f"Maquina: {platform.machine()}")
        print(f"Arquivo de memoria: {MEMORY_FILE.name}")
        print(f"Pasta de modulos: {MODULES_DIR}")
        print(f"Boots registrados: {self.memory.get('boot_count', 0)}")
        print(f"Secure Boot desbloqueado: {self.memory.get('secure_boot_unlocked')}")
        print(f"Custom Mods ativo: {self.memory.get('custom_mods_enabled')}")
        print(f"Auto Destruction: {self.memory.get('destroyed')}")
        print("Status: simulacao controlada, nenhum recurso real do dispositivo foi alterado")
        self.pause()

    def reboot(self) -> None:
        self.state = "reiniciando"
        self.add_notification("Reinicializacao solicitada.", category="sistema")
        self.add_history("Reinicializacao solicitada")
        self.save_memory()
        self.clear()
        self.header()
        self.loading("Reiniciando...", ["Voltando ao bootloader", "Recriando sessao", "Pronto"], Color.YELLOW)
        self.bootloader_screen()

    def system_info(self) -> None:
        self.clear()
        self.header()
        print(self.c("INFORMACOES DO SISTEMA", Color.BOLD + Color.GREEN))
        print()
        print(f"Nome: {SYSTEM_NAME}")
        print(f"Versao: {VERSION}")
        print(f"Estado: {self.state}")
        print(f"Python: {platform.python_version()}")
        print(f"Sistema hospedeiro: {platform.system()} {platform.release()}")
        print(f"Arquivo de memoria: {MEMORY_FILE}")
        print("Observacao: esta e uma simulacao educacional em terminal.")
        self.pause()

    def notifications_menu(self) -> None:
        while True:
            self.clear()
            self.header()
            print(self.c("CENTRAL DE NOTIFICACOES", Color.BOLD + Color.CYAN))
            print()
            notifications = self.memory.get("notifications", [])
            if not notifications:
                print("Nenhuma notificacao salva.")
            else:
                for item in notifications[-12:]:
                    status = "lida" if item.get("read") else self.c("nova", Color.YELLOW)
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
                self.add_notification("Notificacao de teste do Peanut Compact.", category="teste")
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
            print(self.c("MEMORIA ARMAZENADA", Color.BOLD + Color.CYAN))
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
                    self.add_notification(f"Nome alterado para {new_name}.", category="memoria")
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
            for item in history[-18:]:
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
        self.add_notification("Memoria armazenada recriada.", category="recovery")
        self.save_memory()
        print("Memoria resetada.")
        self.pause()

    def main_menu(self) -> None:
        while self.running and self.state == "ligado":
            self.clear()
            self.header()
            print(self.c("MENU PRINCIPAL", Color.BOLD + Color.GREEN))
            print()
            print("[1] Informacoes do sistema")
            print("[2] Central de notificacoes")
            print("[3] Memoria armazenada")
            print("[4] Custom Mods")
            print("[5] Reiniciar")
            print("[6] Entrar em modo recovery")
            print("[7] Desligar")
            choice = input("\nEscolha uma opcao: ").strip()
            if choice == "1":
                self.system_info()
            elif choice == "2":
                self.notifications_menu()
            elif choice == "3":
                self.memory_menu()
            elif choice == "4":
                self.custom_mods_menu()
            elif choice == "5":
                self.reboot()
                return
            elif choice == "6":
                self.recovery_mode()
                if self.running and self.state != "ligado":
                    return
            elif choice == "7":
                self.shutdown()
            else:
                print("Opcao invalida.")
                self.pause()


def main() -> None:
    PeanutCompact().bootloader_screen()


if __name__ == "__main__":
    main()
