"""
Peanut OS Compact v0.4.0 Concept

Mini OS simulado em terminal, feito em Python.
Esta versão foca em Bootloader, minigames mais fortes, comandos de reparo,
Auto Destruction persistente dentro da memória do Peanut OS, apps internos,
Custom Mods próprios do Peanut OS, cores e animações de carregamento.

Segurança: este arquivo NÃO altera boot real, BIOS/UEFI, Android, Windows,
partições, drivers ou arquivos fora da pasta do Peanut OS Compact.
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
from typing import Any, Callable

VERSION = "0.4.0 Concept"
SYSTEM_NAME = "Peanut OS Compact"
BASE_DIR = Path(__file__).resolve().parent
MEMORY_FILE = BASE_DIR / "peanut_memory.json"
MODULES_DIR = BASE_DIR / "modules"
NOTES_FILE = BASE_DIR / "compact_notes.txt"


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
        self.theme_color = str(self.memory.get("theme_color", "cyan"))
        self.ensure_memory_schema()
        self.add_notification("Bootloader Compact v0.4.0 pronto.", category="bootloader")
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
            "destroyed_at": None,
            "bootloader_attempts": 0,
            "destruction_attempts": 0,
            "installed_apps": [
                "Configuracoes",
                "Loja de Apps Beta",
                "Notificacoes",
                "Memoria",
                "Informacoes",
                "Calculadora",
                "Notas",
                "Relogio",
                "Arquivos",
                "Seguranca",
                "Temas",
                "Comandos",
            ],
            "app_updates": [],
            "theme_color": "cyan",
        }

    def ensure_memory_schema(self) -> None:
        defaults = self.default_memory()
        for key, value in defaults.items():
            self.memory.setdefault(key, value)

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
        if len(history) > 50:
            del history[:-50]

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
        if len(notifications) > 60:
            del notifications[:-60]

    def unread_count(self) -> int:
        return sum(1 for item in self.memory.get("notifications", []) if not item.get("read", False))

    def clear(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def now(self) -> str:
        return datetime.now().strftime("%H:%M")

    def c(self, text: str, color: str | None = None) -> str:
        if color is None:
            color = self.get_theme_color()
        return f"{color}{text}{Color.RESET}"

    def get_theme_color(self) -> str:
        colors = {
            "cyan": Color.CYAN,
            "green": Color.GREEN,
            "yellow": Color.YELLOW,
            "blue": Color.BLUE,
            "magenta": Color.MAGENTA,
            "white": Color.WHITE,
        }
        return colors.get(str(self.memory.get("theme_color", "cyan")), Color.CYAN)

    def header(self) -> None:
        lock = "UNLOCKED" if self.memory.get("secure_boot_unlocked") else "LOCKED"
        mods = "ON" if self.memory.get("custom_mods_enabled") else "OFF"
        destroyed = "SIM" if self.memory.get("destroyed") else "NAO"
        print(self.c("=" * 68))
        print(self.c(f"{SYSTEM_NAME} - v{VERSION}", Color.BOLD + self.get_theme_color()))
        print(self.c("=" * 68))
        print(f"Usuario: {self.memory.get('username', 'Usuario Compact')}")
        print(f"Bateria: {self.battery}% | Hora: {self.now()} | Estado: {self.state}")
        print(f"Secure Boot: {lock} | Custom Mods: {mods} | Destruction: {destroyed}")
        print(f"Apps: {len(self.memory.get('installed_apps', []))} | Notificacoes nao lidas: {self.unread_count()}")
        print(self.c("=" * 68))
        print()

    def pause(self) -> None:
        input("\nPressione ENTER para continuar...")

    def loading(self, title: str, steps: list[str], color: str | None = None, delay: float = 0.16) -> None:
        color = color or self.get_theme_color()
        print(self.c(title, Color.BOLD + color))
        print()
        spinner = ["|", "/", "-", "\\"]
        for index, step in enumerate(steps):
            icon = spinner[index % len(spinner)]
            print(self.c(f" {icon} {step}", color))
            time.sleep(delay)
        print()

    def progress_bar(self, label: str, seconds: float = 0.9, color: str | None = None) -> None:
        color = color or self.get_theme_color()
        print(label)
        total = 28
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
                print(self.c("PEANUT OS COMPACT ESTA DESTRUIDO NA MEMORIA LOCAL.", Color.RED + Color.BOLD))
                print("Boot normal bloqueado. Use a aba Comandos e digite Reparo Fix.")
                print()
                print("[1] Aba Comandos")
                print("[2] Modo Recovery")
                print("[3] Sair")
                choice = input("\nEscolha uma opcao: ").strip()
                if choice == "1":
                    self.command_center()
                elif choice == "2":
                    self.recovery_mode()
                elif choice == "3":
                    self.shutdown()
                else:
                    print("Opcao invalida.")
                    self.pause()
                continue

            print(self.c("BOOTLOADER COMPACT", Color.BOLD + Color.MAGENTA))
            print()
            print("[1] Boot normal")
            print("[2] Desbloquear Secure Boot (minigame avancado)")
            print("[3] Custom Mods")
            print("[4] Modo Recovery")
            print("[5] Auto Destruction permanente do Peanut OS")
            print("[6] Aba Comandos")
            print("[7] Sair")
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
                self.command_center()
            elif choice == "7":
                self.shutdown()
            else:
                print("Opcao invalida.")
                self.pause()

    def secure_boot_minigame(self) -> None:
        self.clear()
        self.header()
        print(self.c("MINIGAME AVANCADO: SECURE BOOT", Color.BOLD + Color.YELLOW))
        print("Venca 3 fases. Errou uma, o token falha.")
        score = 0
        phases: list[Callable[[], bool]] = [self.game_sequence, self.game_math, self.game_reverse]
        random.shuffle(phases)
        for index, phase in enumerate(phases, start=1):
            print(self.c(f"\nFASE {index}/3", Color.BOLD + Color.CYAN))
            if phase():
                score += 1
                print(self.c("Fase concluida.", Color.GREEN))
            else:
                print(self.c("Fase falhou.", Color.RED))
                break
        self.memory["bootloader_attempts"] = int(self.memory.get("bootloader_attempts", 0)) + 1
        if score == 3:
            self.memory["secure_boot_unlocked"] = True
            self.add_notification("Secure Boot desbloqueado pelo minigame avancado.", category="bootloader")
            self.add_history("Secure Boot desbloqueado na v0.4.0")
            self.loading("Assinando token local...", ["Token aceito", "Bootloader aberto", "Custom Mods liberados"], Color.GREEN)
        else:
            self.add_notification("Falha no minigame avancado do Secure Boot.", category="bootloader")
            self.add_history("Falha no Secure Boot avancado")
            print(self.c("Secure Boot continua bloqueado.", Color.RED))
        self.save_memory()
        self.pause()

    def game_sequence(self) -> bool:
        sequence = [random.choice(["A", "B", "X", "Y", "L", "R"]) for _ in range(7)]
        print("Memorize a sequencia:", " ".join(sequence))
        time.sleep(2.0)
        print("\n" * 5)
        answer = input("Digite a sequencia separada por espaco: ").upper().strip().split()
        return answer == sequence

    def game_math(self) -> bool:
        a = random.randint(8, 25)
        b = random.randint(3, 12)
        op = random.choice(["+", "-"])
        result = a + b if op == "+" else a - b
        answer = input(f"Resolva o token numerico: {a} {op} {b} = ").strip()
        return answer == str(result)

    def game_reverse(self) -> bool:
        word = random.choice(["PEANUT", "COMPACT", "BOOT", "SYSTEM", "KERNEL"])
        answer = input(f"Digite esta palavra ao contrario: {word} -> ").strip().upper()
        return answer == word[::-1]

    def boot_screen(self) -> None:
        self.state = "ligando"
        self.add_history("Boot iniciado")
        self.save_memory()
        self.clear()
        self.header()
        steps = [
            "Inicializando Bootloader Compact...",
            "Verificando estado de destruicao local...",
            "Verificando Secure Boot simulado...",
            "Lendo memoria armazenada...",
            "Atualizando apps internos...",
            "Carregando notificacoes...",
            "Preparando interface colorida...",
            "Importando modulos ativados...",
        ]
        self.loading("BOOT ANIMATION", steps, Color.CYAN, delay=0.18)
        self.update_system_apps(silent=True)
        self.load_enabled_modules()
        self.progress_bar("Finalizando boot", seconds=0.9, color=Color.GREEN)
        self.state = "ligado"
        self.memory["boot_count"] = int(self.memory.get("boot_count", 0)) + 1
        self.add_notification("Peanut OS Compact foi ligado com sucesso.", category="boot")
        self.add_history("Boot concluido")
        self.save_memory()
        self.pause()

    def update_system_apps(self, silent: bool = False) -> None:
        apps = [
            "Configuracoes",
            "Loja de Apps Beta",
            "Notificacoes",
            "Memoria",
            "Informacoes",
            "Calculadora",
            "Notas",
            "Relogio",
            "Arquivos",
            "Seguranca",
            "Temas",
            "Comandos",
        ]
        self.memory["installed_apps"] = apps
        update_entry = {"time": self.timestamp(), "version": VERSION, "apps": len(apps)}
        updates = self.memory.setdefault("app_updates", [])
        updates.append(update_entry)
        if len(updates) > 10:
            del updates[:-10]
        self.add_history("Apps internos atualizados")
        self.save_memory()
        if not silent:
            print(self.c("Apps internos atualizados.", Color.GREEN))
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
            print(self.c("CUSTOM MODS DO PEANUT OS", Color.BOLD + Color.MAGENTA))
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
            print("Nenhum modulo .py encontrado.")
        for index, module in enumerate(modules, start=1):
            status = "ON" if module in enabled else "OFF"
            print(f"[{index}] {module} - {status}")
        self.pause()

    def enable_module(self, modules: list[str]) -> None:
        if not modules:
            print("Nenhum modulo disponivel.")
            self.pause()
            return
        self.show_modules(modules, set(self.memory.get("enabled_modules", [])))
        choice = input("Numero do modulo para habilitar: ").strip()
        if not choice.isdigit():
            return
        index = int(choice) - 1
        if 0 <= index < len(modules):
            enabled = self.memory.setdefault("enabled_modules", [])
            if modules[index] not in enabled:
                enabled.append(modules[index])
            self.add_notification(f"Modulo habilitado: {modules[index]}", category="mod")
            self.add_history(f"Modulo habilitado: {modules[index]}")
            self.save_memory()

    def disable_module(self) -> None:
        enabled = self.memory.get("enabled_modules", [])
        if not enabled:
            print("Nenhum modulo habilitado.")
            self.pause()
            return
        for index, module in enumerate(enabled, start=1):
            print(f"[{index}] {module}")
        choice = input("Numero do modulo para desabilitar: ").strip()
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(enabled):
                removed = enabled.pop(index)
                self.add_notification(f"Modulo desabilitado: {removed}", category="mod")
                self.add_history(f"Modulo desabilitado: {removed}")
                self.save_memory()

    def auto_destruction(self) -> None:
        self.clear()
        self.header()
        print(self.c("AUTO DESTRUCTION PERMANENTE DO PEANUT OS", Color.BOLD + Color.RED))
        print("Isto destrói apenas a memoria local do Peanut OS Compact.")
        print("O boot ficará bloqueado até usar a aba Comandos com: Reparo Fix")
        print()
        print("Para continuar, vença o minigame de confirmação.")
        print("Digite CANCELAR a qualquer momento para sair.")
        code = "DESTROY-" + str(random.randint(100, 999))
        phrase = random.choice(["PEANUT", "BOOT", "COMPACT"])
        answer1 = input(f"Digite exatamente o codigo {code}: ").strip()
        if answer1.upper() == "CANCELAR":
            return
        answer2 = input(f"Digite {phrase} ao contrario: ").strip().upper()
        number_a = random.randint(10, 30)
        number_b = random.randint(2, 9)
        answer3 = input(f"Confirme o checksum {number_a} + {number_b}: ").strip()
        self.memory["destruction_attempts"] = int(self.memory.get("destruction_attempts", 0)) + 1
        if answer1 == code and answer2 == phrase[::-1] and answer3 == str(number_a + number_b):
            self.progress_bar("Executando destruicao local do Peanut OS", seconds=1.2, color=Color.RED)
            self.memory["destroyed"] = True
            self.memory["destroyed_at"] = self.timestamp()
            self.memory["custom_mods_enabled"] = False
            self.memory["enabled_modules"] = []
            self.add_notification("Auto Destruction ativado. Boot bloqueado ate Reparo Fix.", category="seguranca")
            self.add_history("Auto Destruction permanente ativado")
            self.save_memory()
            print(self.c("Peanut OS Compact bloqueado na memoria local.", Color.RED))
        else:
            print(self.c("Minigame falhou. Auto Destruction cancelado.", Color.GREEN))
            self.add_history("Auto Destruction cancelado por falha no minigame")
            self.save_memory()
        self.pause()

    def command_center(self) -> None:
        while True:
            self.clear()
            self.header()
            print(self.c("ABA COMANDOS", Color.BOLD + Color.BLUE))
            print("Digite /help para ver comandos.")
            print("Digite sair para voltar.")
            command = input("\nPeanutCMD> ").strip()
            if command.lower() == "sair":
                return
            if command == "/help":
                self.show_help()
            elif command == "Reparo Fix":
                self.repair_fix()
            elif command == "status":
                self.system_info()
            elif command == "apps update":
                self.update_system_apps(silent=False)
            elif command == "notificacoes limpar":
                self.clear_notifications()
            elif command == "memoria reset":
                self.reset_memory()
                return
            else:
                print("Comando nao reconhecido. Use /help.")
                self.pause()

    def show_help(self) -> None:
        self.clear()
        self.header()
        print("COMANDOS DISPONIVEIS")
        print()
        print("/help                 - mostra esta tela")
        print("Reparo Fix            - repara Auto Destruction do Peanut OS")
        print("status                - mostra informacoes do sistema")
        print("apps update           - atualiza apps internos")
        print("notificacoes limpar   - limpa notificacoes")
        print("memoria reset         - reseta memoria armazenada")
        print("sair                  - volta para a tela anterior")
        self.pause()

    def repair_fix(self) -> None:
        self.clear()
        self.header()
        if not self.memory.get("destroyed"):
            print("Nenhum estado destruido detectado.")
            self.pause()
            return
        confirm = input("Digite REPARAR para restaurar o Peanut OS Compact: ").strip()
        if confirm != "REPARAR":
            print("Reparo cancelado.")
            self.pause()
            return
        self.progress_bar("Aplicando Reparo Fix", seconds=1.0, color=Color.GREEN)
        self.memory["destroyed"] = False
        self.memory["destroyed_at"] = None
        self.state = "desligado"
        self.add_notification("Reparo Fix aplicado. Boot liberado novamente.", category="comandos")
        self.add_history("Reparo Fix aplicado")
        self.save_memory()
        print(self.c("Peanut OS Compact reparado.", Color.GREEN))
        self.pause()

    def shutdown(self) -> None:
        self.state = "encerrando"
        self.add_history("Sistema encerrado")
        self.save_memory()
        self.clear()
        self.header()
        self.loading("Encerrando Peanut OS Compact", ["Salvando memoria", "Fechando interface", "Finalizado"], Color.YELLOW)
        self.state = "desligado"
        self.save_memory()
        self.running = False

    def reboot(self) -> None:
        self.state = "reiniciando"
        self.add_notification("Reinicializacao solicitada.", category="sistema")
        self.add_history("Reinicializacao solicitada")
        self.save_memory()
        self.clear()
        self.header()
        self.progress_bar("Reiniciando", seconds=0.7, color=Color.YELLOW)
        self.boot_screen()

    def recovery_mode(self) -> None:
        self.state = "recovery"
        self.add_notification("Modo recovery acessado.", category="recovery")
        self.add_history("Recovery acessado")
        self.save_memory()
        while True:
            self.clear()
            self.header()
            print(self.c("MODO RECOVERY", Color.BOLD + Color.YELLOW))
            print()
            print("[1] Ver diagnostico basico")
            print("[2] Reiniciar sistema")
            print("[3] Desligar")
            print("[4] Limpar notificacoes")
            print("[5] Resetar memoria armazenada")
            print("[6] Aba Comandos")
            print("[7] Voltar para Bootloader")
            choice = input("\nEscolha uma opcao: ").strip()
            if choice == "1":
                self.diagnostics()
            elif choice == "2":
                if self.memory.get("destroyed"):
                    print("Boot bloqueado. Use Reparo Fix na aba Comandos.")
                    self.pause()
                else:
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
                self.command_center()
            elif choice == "7":
                self.state = "bootloader"
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
        print(f"Arquivo de memoria: {MEMORY_FILE.name}")
        print(f"Boots registrados: {self.memory.get('boot_count', 0)}")
        print(f"Apps instalados: {len(self.memory.get('installed_apps', []))}")
        print(f"Estado destruido: {self.memory.get('destroyed')}")
        print("Status: simulacao local controlada")
        self.pause()

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
        print("Observacao: esta e uma simulacao educacional em terminal.")
        self.pause()

    def main_menu(self) -> None:
        while self.running and self.state == "ligado":
            self.clear()
            self.header()
            print(self.c("MENU PRINCIPAL", Color.BOLD + Color.GREEN))
            print()
            apps = [
                ("1", "Informacoes", self.system_info),
                ("2", "Notificacoes", self.notifications_menu),
                ("3", "Memoria", self.memory_menu),
                ("4", "Apps", self.apps_menu),
                ("5", "Configuracoes", self.settings_app),
                ("6", "Loja de Apps Beta", self.app_store_beta),
                ("7", "Calculadora", self.calculator_app),
                ("8", "Notas", self.notes_app),
                ("9", "Relogio", self.clock_app),
                ("10", "Arquivos", self.files_app),
                ("11", "Seguranca", self.security_app),
                ("12", "Temas", self.themes_app),
                ("13", "Comandos", self.command_center),
                ("14", "Reiniciar", self.reboot),
                ("15", "Modo Recovery", self.recovery_mode),
                ("16", "Desligar", self.shutdown),
            ]
            for key, name, _ in apps:
                print(f"[{key}] {name}")
            choice = input("\nEscolha uma opcao: ").strip()
            for key, _, action in apps:
                if choice == key:
                    action()
                    break
            else:
                print("Opcao invalida.")
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
                for item in notifications[-12:]:
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
                self.add_notification("Notificacao de teste do Peanut Compact v0.4.0.", category="teste")
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
            for item in history[-20:]:
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

    def apps_menu(self) -> None:
        self.clear()
        self.header()
        print("APPS DO SISTEMA")
        print()
        for index, app in enumerate(self.memory.get("installed_apps", []), start=1):
            print(f"[{index}] {app}")
        print()
        print("Use a Loja de Apps Beta para ver apps planejados.")
        self.pause()

    def settings_app(self) -> None:
        while True:
            self.clear()
            self.header()
            print("CONFIGURACOES")
            print()
            print("[1] Alterar usuario")
            print("[2] Atualizar apps internos")
            print("[3] Voltar")
            choice = input("\nEscolha uma opcao: ").strip()
            if choice == "1":
                name = input("Novo usuario: ").strip()
                if name:
                    self.memory["username"] = name
                    self.save_memory()
            elif choice == "2":
                self.update_system_apps(silent=False)
            elif choice == "3":
                return

    def app_store_beta(self) -> None:
        self.clear()
        self.header()
        print("LOJA DE APPS BETA")
        print()
        print("Status: beta fechado")
        print("Apps planejados:")
        print("- Player de musica")
        print("- Galeria ASCII")
        print("- Gerenciador de perfis")
        print("- Atualizador de modulos")
        print()
        print("A loja ainda nao baixa apps externos. Ela apenas mostra planos internos.")
        self.pause()

    def calculator_app(self) -> None:
        self.clear()
        self.header()
        print("CALCULADORA")
        print("Use apenas contas simples. Exemplo: 2 + 2")
        expr = input("Conta: ").strip()
        allowed = set("0123456789+-*/(). ")
        if expr and all(char in allowed for char in expr):
            try:
                print("Resultado:", eval(expr, {"__builtins__": {}}, {}))
            except Exception:
                print("Conta invalida.")
        else:
            print("Entrada bloqueada por seguranca.")
        self.pause()

    def notes_app(self) -> None:
        self.clear()
        self.header()
        print("NOTAS")
        print("[1] Ver notas")
        print("[2] Adicionar nota")
        choice = input("Opcao: ").strip()
        if choice == "1":
            if NOTES_FILE.exists():
                print(NOTES_FILE.read_text(encoding="utf-8"))
            else:
                print("Nenhuma nota salva.")
        elif choice == "2":
            note = input("Nota: ").strip()
            if note:
                with NOTES_FILE.open("a", encoding="utf-8") as file:
                    file.write(f"[{self.timestamp()}] {note}\n")
                print("Nota salva.")
        self.pause()

    def clock_app(self) -> None:
        self.clear()
        self.header()
        print("RELOGIO")
        print(f"Hora atual: {datetime.now().strftime('%H:%M:%S')}")
        print(f"Data atual: {datetime.now().strftime('%d/%m/%Y')}")
        self.pause()

    def files_app(self) -> None:
        self.clear()
        self.header()
        print("ARQUIVOS DO PEANUT COMPACT")
        print()
        for path in sorted(BASE_DIR.iterdir()):
            label = "Pasta" if path.is_dir() else "Arquivo"
            print(f"- {label}: {path.name}")
        self.pause()

    def security_app(self) -> None:
        self.clear()
        self.header()
        print("SEGURANCA")
        print(f"Secure Boot desbloqueado: {self.memory.get('secure_boot_unlocked')}")
        print(f"Custom Mods ativo: {self.memory.get('custom_mods_enabled')}")
        print(f"Auto Destruction ativo: {self.memory.get('destroyed')}")
        print(f"Tentativas Bootloader: {self.memory.get('bootloader_attempts')}")
        print(f"Tentativas Destruction: {self.memory.get('destruction_attempts')}")
        self.pause()

    def themes_app(self) -> None:
        self.clear()
        self.header()
        print("TEMAS")
        themes = ["cyan", "green", "yellow", "blue", "magenta", "white"]
        for index, theme in enumerate(themes, start=1):
            print(f"[{index}] {theme}")
        choice = input("Escolha um tema: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(themes):
            self.memory["theme_color"] = themes[int(choice) - 1]
            self.save_memory()
            print("Tema aplicado.")
        self.pause()


def main() -> None:
    PeanutCompact().bootloader_screen()


if __name__ == "__main__":
    main()
