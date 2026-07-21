from __future__ import annotations

import html.parser
import importlib.util
import json
import os
import platform
import random
import re
import sys
import textwrap
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any

VERSION = "0.5.5 Concept"
SYSTEM_NAME = "Peanut OS Compact"
BASE_DIR = Path(__file__).resolve().parent
MEMORY_FILE = BASE_DIR / "peanut_memory.json"
MODULES_DIR = BASE_DIR / "modules"
ROM_LIMIT_MB = 1024


class C:
    R = "\033[0m"
    B = "\033[1m"
    D = "\033[2m"
    RED = "\033[31m"
    G = "\033[32m"
    Y = "\033[33m"
    BL = "\033[34m"
    M = "\033[35m"
    CY = "\033[36m"
    W = "\033[37m"


class TerminalPageParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title: list[str] = []
        self.text: list[str] = []
        self.links: list[dict[str, str]] = []
        self.images: list[dict[str, str]] = []
        self.videos: list[dict[str, str]] = []
        self.in_title = False
        self.skip = False
        self.current_href: str | None = None
        self.current_link_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {key.lower(): value or "" for key, value in attrs}
        tag = tag.lower()
        if tag in {"script", "style", "noscript", "svg"}:
            self.skip = True
        if tag == "title":
            self.in_title = True
        if tag == "a" and attr.get("href"):
            self.current_href = attr.get("href")
            self.current_link_text = []
        if tag == "img" and attr.get("src"):
            self.images.append({"src": attr.get("src", ""), "alt": attr.get("alt", "Imagem sem descricao")})
        if tag in {"video", "source"} and attr.get("src"):
            self.videos.append({"src": attr.get("src", ""), "label": attr.get("type", "video")})
        if tag == "iframe" and attr.get("src") and any(site in attr.get("src", "") for site in ["youtube", "youtu.be", "vimeo"]):
            self.videos.append({"src": attr.get("src", ""), "label": "video incorporado"})
        if tag in {"p", "br", "h1", "h2", "h3", "li", "section", "article"}:
            self.text.append("\n")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in {"script", "style", "noscript", "svg"}:
            self.skip = False
        if tag == "title":
            self.in_title = False
        if tag == "a" and self.current_href:
            label = " ".join("".join(self.current_link_text).split()) or self.current_href
            self.links.append({"href": self.current_href, "text": label[:90]})
            self.current_href = None
            self.current_link_text = []

    def handle_data(self, data: str) -> None:
        if self.skip:
            return
        cleaned = " ".join(data.split())
        if not cleaned:
            return
        if self.in_title:
            self.title.append(cleaned)
        elif self.current_href:
            self.current_link_text.append(cleaned + " ")
        else:
            self.text.append(cleaned + " ")


class PeanutCompact:
    def __init__(self) -> None:
        MODULES_DIR.mkdir(exist_ok=True)
        self.memory = self.load_memory()
        self.running = True
        self.state = self.memory.get("last_state", "bootloader")
        self.battery = int(self.memory.get("battery", random.randint(25, 95)))
        self.ensure_memory()
        self.add_notification("Peanut OS Compact v0.5.5 carregado.", "sistema")
        self.save_memory()

    def ensure_memory(self) -> None:
        defaults = self.default_memory()
        for key, value in defaults.items():
            self.memory.setdefault(key, value)

    def default_memory(self) -> dict[str, Any]:
        return {
            "username": "Usuario Compact",
            "battery": random.randint(25, 95),
            "last_state": "bootloader",
            "boot_count": 0,
            "notifications": [],
            "history": [],
            "secure_boot_unlocked": False,
            "custom_mods_enabled": False,
            "enabled_modules": [],
            "destroyed": False,
            "browser_history": [],
            "browser_bookmarks": ["https://example.com", "https://www.python.org"],
            "browser_touch_mode": True,
            "notes": [],
            "theme": "peanut-cmd",
        }

    def load_memory(self) -> dict[str, Any]:
        if not MEMORY_FILE.exists():
            return self.default_memory()
        try:
            with MEMORY_FILE.open("r", encoding="utf-8") as file:
                data = json.load(file)
            return data if isinstance(data, dict) else self.default_memory()
        except (OSError, json.JSONDecodeError):
            return self.default_memory()

    def save_memory(self) -> None:
        self.memory["battery"] = self.battery
        self.memory["last_state"] = self.state
        try:
            with MEMORY_FILE.open("w", encoding="utf-8") as file:
                json.dump(self.memory, file, ensure_ascii=False, indent=2)
        except OSError:
            print("Aviso: memoria local nao pode ser salva.")

    def stamp(self) -> str:
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def now(self) -> str:
        return datetime.now().strftime("%H:%M")

    def c(self, text: str, color: str) -> str:
        return f"{color}{text}{C.R}"

    def clear(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def pause(self) -> None:
        input("\nPressione ENTER para continuar...")

    def add_history(self, action: str) -> None:
        history = self.memory.setdefault("history", [])
        history.append({"time": self.stamp(), "action": action})
        if len(history) > 80:
            del history[:-80]

    def add_notification(self, message: str, category: str = "geral") -> None:
        notifications = self.memory.setdefault("notifications", [])
        last = notifications[-1]["message"] if notifications else ""
        if last == message:
            return
        notifications.append({"id": len(notifications) + 1, "time": self.stamp(), "category": category, "message": message, "read": False})
        if len(notifications) > 80:
            del notifications[:-80]

    def unread_count(self) -> int:
        return sum(1 for item in self.memory.get("notifications", []) if not item.get("read"))

    def header(self) -> None:
        lock = "UNLOCKED" if self.memory.get("secure_boot_unlocked") else "LOCKED"
        mods = "ON" if self.memory.get("custom_mods_enabled") else "OFF"
        dead = "SIM" if self.memory.get("destroyed") else "NAO"
        print(self.c("=" * 70, C.CY))
        print(self.c(f"{SYSTEM_NAME} - v{VERSION}", C.B + C.Y))
        print(self.c("=" * 70, C.CY))
        print(f"Usuario: {self.memory.get('username')} | Bateria: {self.battery}% | Hora: {self.now()}")
        print(f"Estado: {self.state} | Secure Boot: {lock} | Mods: {mods} | Destruido: {dead}")
        print(f"Notificacoes nao lidas: {self.unread_count()} | Tema: {self.memory.get('theme')}")
        print(self.c("=" * 70, C.CY))
        print()

    def loading(self, title: str, steps: list[str], color: str = C.G, delay: float = 0.18) -> None:
        print(self.c(title, C.B + color))
        spinner = ["|", "/", "-", "\\"]
        for index, step in enumerate(steps):
            print(self.c(f" {spinner[index % 4]} {step}", color))
            time.sleep(delay)
        print()

    def progress(self, label: str, seconds: float = 0.8, color: str = C.CY) -> None:
        total = 26
        print(label)
        for i in range(total + 1):
            filled = "#" * i
            empty = "." * (total - i)
            print(f"\r{self.c('[', color)}{self.c(filled, color)}{empty}{self.c(']', color)} {int(i / total * 100)}%", end="")
            time.sleep(seconds / total)
        print("\n")

    def bootloader_screen(self) -> None:
        while self.running:
            self.clear(); self.state = "bootloader"; self.save_memory(); self.header()
            if self.memory.get("destroyed"):
                self.destroyed_screen(); continue
            print(self.c("BOOTLOADER COMPACT", C.B + C.M))
            print("[1] Boot normal")
            print("[2] Desbloquear Secure Boot")
            print("[3] Custom Mods")
            print("[4] Recovery")
            print("[5] Auto Destruction")
            print("[6] Aba Comandos")
            print("[7] Sair")
            choice = input("\nEscolha: ").strip()
            if choice == "1": self.boot_screen(); self.main_menu()
            elif choice == "2": self.secure_boot_minigame()
            elif choice == "3": self.custom_mods_menu()
            elif choice == "4": self.recovery_mode()
            elif choice == "5": self.auto_destruction()
            elif choice == "6": self.command_center()
            elif choice == "7": self.shutdown()
            else: print("Opcao invalida."); self.pause()

    def boot_screen(self) -> None:
        self.clear(); self.state = "ligando"; self.save_memory(); self.header()
        self.loading("BOOT ANIMATION", ["Lendo memoria local", "Verificando Bootloader", "Preparando apps", "Preparando navegador", "Carregando modulos"], C.CY, 0.2)
        self.load_enabled_modules(); self.progress("Finalizando boot", 0.8, C.G)
        self.state = "ligado"; self.memory["boot_count"] = int(self.memory.get("boot_count", 0)) + 1
        self.add_history("Boot concluido"); self.add_notification("Sistema ligado com navegador v0.5.5.", "boot"); self.save_memory(); self.pause()

    def shutdown(self) -> None:
        self.clear(); self.state = "encerrando"; self.header(); self.progress("Encerrando Peanut OS Compact", 0.6, C.Y)
        self.add_history("Sistema encerrado"); self.state = "desligado"; self.save_memory(); self.running = False

    def main_menu(self) -> None:
        while self.running and self.state == "ligado":
            self.clear(); self.header(); print(self.c("MENU PRINCIPAL", C.B + C.G))
            print("[1] Apps")
            print("[2] Navegador Compact")
            print("[3] Notificacoes")
            print("[4] Memoria")
            print("[5] Recovery")
            print("[6] Reiniciar")
            print("[7] Desligar")
            choice = input("\nEscolha: ").strip()
            if choice == "1": self.apps_menu()
            elif choice == "2": self.browser_app()
            elif choice == "3": self.notifications_menu()
            elif choice == "4": self.memory_menu()
            elif choice == "5": self.recovery_mode(); return
            elif choice == "6": self.boot_screen()
            elif choice == "7": self.shutdown()
            else: print("Opcao invalida."); self.pause()

    def apps_menu(self) -> None:
        apps = [
            ("Navegador Compact", self.browser_app), ("Configuracoes", self.settings_app), ("Loja de Apps Beta", self.store_app),
            ("Notificacoes", self.notifications_menu), ("Memoria", self.memory_menu), ("Informacoes", self.system_info_app),
            ("Calculadora", self.calculator_app), ("Notas", self.notes_app), ("Relogio", self.clock_app), ("Arquivos", self.files_app),
            ("Seguranca", self.security_app), ("Temas", self.themes_app), ("Comandos", self.command_center),
        ]
        while True:
            self.clear(); self.header(); print(self.c("APPS DO SISTEMA", C.B + C.BL))
            for i, (name, _) in enumerate(apps, 1): print(f"[{i}] {name}")
            print("[0] Voltar")
            choice = input("\nAbrir app: ").strip()
            if choice == "0": return
            if choice.isdigit() and 1 <= int(choice) <= len(apps): apps[int(choice)-1][1]()
            else: print("App invalido."); self.pause()

    def browser_app(self) -> None:
        current_url = ""
        current_page: dict[str, Any] | None = None
        while True:
            self.clear(); self.header(); print(self.c("NAVEGADOR COMPACT v0.5.5", C.B + C.CY))
            print("Interface CMD com modo touch: escolha numeros grandes para clicar em links, fotos e videos.")
            print(f"Modo touch: {'ON' if self.memory.get('browser_touch_mode') else 'OFF'}")
            print("[1] Abrir URL")
            print("[2] Favoritos")
            print("[3] Historico")
            print("[4] Pagina demo multimidia")
            print("[5] Alternar modo touch")
            print("[6] Ajuda do navegador")
            print("[0] Voltar")
            choice = input("\nEscolha: ").strip()
            if choice == "1":
                url = input("URL ou pesquisa: ").strip()
                if url:
                    current_url = self.normalize_url(url)
                    current_page = self.fetch_page(current_url)
                    self.page_viewer(current_page, current_url)
            elif choice == "2":
                picked = self.pick_from_list("FAVORITOS", self.memory.get("browser_bookmarks", []))
                if picked: self.page_viewer(self.fetch_page(picked), picked)
            elif choice == "3":
                picked = self.pick_from_list("HISTORICO", list(reversed(self.memory.get("browser_history", []))))
                if picked: self.page_viewer(self.fetch_page(picked), picked)
            elif choice == "4":
                current_url = "compact://demo-media"
                current_page = self.demo_media_page()
                self.page_viewer(current_page, current_url)
            elif choice == "5":
                self.memory["browser_touch_mode"] = not self.memory.get("browser_touch_mode")
                self.save_memory()
            elif choice == "6": self.browser_help()
            elif choice == "0": return
            else: print("Opcao invalida."); self.pause()

    def normalize_url(self, text: str) -> str:
        if text.startswith("compact://"):
            return text
        if "." not in text and not text.startswith(("http://", "https://")):
            query = urllib.parse.quote(text)
            return f"https://duckduckgo.com/html/?q={query}"
        if not text.startswith(("http://", "https://")):
            return "https://" + text
        return text

    def fetch_page(self, url: str) -> dict[str, Any]:
        self.clear(); self.header(); print(self.c("Carregando pagina...", C.CY)); self.progress(url[:65], 0.5, C.CY)
        if url == "compact://demo-media":
            return self.demo_media_page()
        headers = {"User-Agent": "PeanutOSCompact/0.5.5 TerminalBrowser"}
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=12) as response:
                content_type = response.headers.get("content-type", "")
                raw = response.read(600_000)
            final_url = url
            if "text/html" not in content_type and not raw.lower().startswith(b"<!doctype") and b"<html" not in raw[:1000].lower():
                return {"title": "Arquivo de midia", "text": f"Conteudo detectado: {content_type or 'desconhecido'}", "links": [], "images": [], "videos": [{"src": url, "label": content_type or "arquivo"}], "error": ""}
            html = raw.decode("utf-8", errors="replace")
            parser = TerminalPageParser(); parser.feed(html)
            title = " ".join(parser.title).strip() or urllib.parse.urlparse(final_url).netloc or final_url
            text = re.sub(r"\s+", " ", " ".join(parser.text)).strip()
            page = {
                "title": title[:100], "text": text[:12000],
                "links": self.clean_links(parser.links, final_url),
                "images": self.clean_media(parser.images, final_url, "src"),
                "videos": self.clean_media(parser.videos, final_url, "src"),
                "error": "",
            }
            self.remember_browser_url(final_url); return page
        except (urllib.error.URLError, TimeoutError, ValueError, OSError) as error:
            return {"title": "Erro ao carregar", "text": "Nao foi possivel carregar a pagina. Alguns sites bloqueiam navegadores de terminal.", "links": [], "images": [], "videos": [], "error": str(error)}

    def clean_links(self, links: list[dict[str, str]], base: str) -> list[dict[str, str]]:
        result = []
        seen = set()
        for item in links:
            href = urllib.parse.urljoin(base, item.get("href", ""))
            if href.startswith(("http://", "https://", "compact://")) and href not in seen:
                seen.add(href); result.append({"href": href, "text": item.get("text", href)[:80]})
            if len(result) >= 25: break
        return result

    def clean_media(self, media: list[dict[str, str]], base: str, field: str) -> list[dict[str, str]]:
        result = []
        seen = set()
        for item in media:
            src = urllib.parse.urljoin(base, item.get(field, ""))
            if src and src not in seen:
                seen.add(src); result.append({"src": src, "label": item.get("alt") or item.get("label") or "midia"})
            if len(result) >= 20: break
        return result

    def demo_media_page(self) -> dict[str, Any]:
        return {
            "title": "Peanut Demo Media",
            "text": "Pagina local de teste do navegador. Ela simula uma pagina com texto, links, foto e video para testar clique por numero no estilo CMD.",
            "links": [{"text": "Abrir Example", "href": "https://example.com"}, {"text": "Abrir Python", "href": "https://www.python.org"}],
            "images": [{"label": "Foto demo: wallpaper Peanut OS", "src": "compact://image/wallpaper-peanut"}],
            "videos": [{"label": "Video demo: boot animation", "src": "compact://video/boot-animation"}],
            "error": "",
        }

    def page_viewer(self, page: dict[str, Any], url: str) -> None:
        scroll = 0
        while True:
            self.clear(); self.header(); print(self.c(f"{page.get('title', 'Pagina')}", C.B + C.CY)); print(self.c(url, C.D))
            if page.get("error"): print(self.c(f"Erro: {page['error']}", C.RED))
            wrapped = textwrap.wrap(page.get("text") or "Sem texto visivel.", width=76)
            for line in wrapped[scroll:scroll+12]: print(line)
            print("\n" + self.c("-- TOUCH BAR / CMD --", C.Y))
            print("[1] Links  [2] Fotos  [3] Videos  [4] +Scroll  [5] -Scroll")
            print("[6] Favoritar  [7] Recarregar  [8] URL  [0] Voltar")
            choice = input("\nToque/digite: ").strip()
            if choice == "1": self.links_touch(page)
            elif choice == "2": self.media_touch(page, "images")
            elif choice == "3": self.media_touch(page, "videos")
            elif choice == "4": scroll = min(max(0, len(wrapped)-1), scroll + 10)
            elif choice == "5": scroll = max(0, scroll - 10)
            elif choice == "6": self.add_bookmark(url)
            elif choice == "7": page = self.fetch_page(url)
            elif choice == "8":
                new_url = input("Nova URL: ").strip()
                if new_url:
                    url = self.normalize_url(new_url); page = self.fetch_page(url); scroll = 0
            elif choice == "0": return
            else: print("Opcao invalida."); self.pause()

    def links_touch(self, page: dict[str, Any]) -> None:
        links = page.get("links", [])
        if not links:
            print("Nenhum link detectado."); self.pause(); return
        while True:
            self.clear(); self.header(); print(self.c("LINKS CLICAVEIS", C.B + C.G))
            for i, item in enumerate(links, 1): print(f"[{i}] {item['text']}\n    {item['href'][:90]}")
            print("[0] Voltar")
            choice = input("\nClique pelo numero: ").strip()
            if choice == "0": return
            if choice.isdigit() and 1 <= int(choice) <= len(links):
                url = links[int(choice)-1]["href"]
                self.page_viewer(self.fetch_page(url), url); return
            print("Link invalido."); self.pause()

    def media_touch(self, page: dict[str, Any], kind: str) -> None:
        items = page.get(kind, [])
        label = "FOTOS" if kind == "images" else "VIDEOS"
        if not items:
            print(f"Nenhum item em {label.lower()} detectado."); self.pause(); return
        while True:
            self.clear(); self.header(); print(self.c(label, C.B + C.M))
            for i, item in enumerate(items, 1): print(f"[{i}] {item.get('label', 'midia')}\n    {item.get('src', '')[:95]}")
            print("[0] Voltar")
            choice = input("\nAbrir item: ").strip()
            if choice == "0": return
            if choice.isdigit() and 1 <= int(choice) <= len(items):
                self.media_viewer(items[int(choice)-1], kind); return
            print("Item invalido."); self.pause()

    def media_viewer(self, item: dict[str, str], kind: str) -> None:
        self.clear(); self.header(); print(self.c("VISUALIZADOR DE MIDIA", C.B + C.M))
        print(f"Tipo: {'foto' if kind == 'images' else 'video'}")
        print(f"Titulo: {item.get('label', 'midia')}")
        print(f"Fonte: {item.get('src', '')}")
        print()
        if kind == "images":
            print("[ IMAGEM DETECTADA ]")
            print("O terminal CMD nao renderiza imagem real aqui, mas o navegador agora detecta, lista e abre o item como midia navegavel.")
        else:
            print("[ VIDEO DETECTADO ]")
            print("O terminal CMD nao toca video real aqui, mas o navegador identifica players/arquivos de video e mostra o item para navegacao.")
        self.pause()

    def add_bookmark(self, url: str) -> None:
        bookmarks = self.memory.setdefault("browser_bookmarks", [])
        if url not in bookmarks:
            bookmarks.append(url); self.add_notification("Pagina adicionada aos favoritos.", "browser")
        self.save_memory(); print("Favorito salvo."); self.pause()

    def remember_browser_url(self, url: str) -> None:
        history = self.memory.setdefault("browser_history", [])
        if not history or history[-1] != url:
            history.append(url)
        if len(history) > 30: del history[:-30]
        self.save_memory()

    def pick_from_list(self, title: str, items: list[str]) -> str | None:
        while True:
            self.clear(); self.header(); print(self.c(title, C.B + C.Y))
            if not items: print("Lista vazia."); self.pause(); return None
            for i, item in enumerate(items[:20], 1): print(f"[{i}] {item}")
            print("[0] Voltar")
            choice = input("\nEscolha: ").strip()
            if choice == "0": return None
            if choice.isdigit() and 1 <= int(choice) <= min(len(items), 20): return items[int(choice)-1]
            print("Opcao invalida."); self.pause()

    def browser_help(self) -> None:
        self.clear(); self.header(); print(self.c("AJUDA DO NAVEGADOR", C.B + C.CY))
        print("- Digite uma URL ou termo de busca.")
        print("- Links viram botoes numerados para clicar pelo teclado/touch.")
        print("- Fotos e videos sao detectados e abertos no visualizador de midia do terminal.")
        print("- O navegador e textual: nao executa JavaScript e nao renderiza video/foto real dentro do CMD.")
        print("- Sites modernos podem bloquear ou esconder conteudo de navegadores simples.")
        self.pause()

    def secure_boot_minigame(self) -> None:
        self.clear(); self.header(); print(self.c("SECURE BOOT - MINIGAME AVANCADO", C.B + C.Y))
        seq = [random.choice(["A", "B", "X", "Y", "L", "R"]) for _ in range(7)]
        print("Memorize:", " ".join(seq)); time.sleep(3); self.clear(); self.header()
        ans = input("Repita a sequencia: ").upper().split()
        token = random.randint(20, 80); math_answer = token * 2 + 7
        ans2 = input(f"Token matematico {token}*2+7 = ").strip()
        word = random.choice(["PEANUT", "COMPACT", "BOOT", "KERNEL"])
        ans3 = input(f"Digite ao contrario: {word} = ").strip().upper()
        if ans == seq and ans2 == str(math_answer) and ans3 == word[::-1]:
            self.memory["secure_boot_unlocked"] = True; self.add_history("Secure Boot desbloqueado"); print(self.c("DESBLOQUEADO.", C.G))
        else:
            print(self.c("Falhou. Secure Boot continua bloqueado.", C.RED))
        self.save_memory(); self.pause()

    def auto_destruction(self) -> None:
        self.clear(); self.header(); print(self.c("AUTO DESTRUCTION DO PEANUT OS", C.B + C.RED))
        print("Isto e permanente apenas dentro da memoria local do Peanut OS, ate usar Reparo Fix.")
        code = random.randint(1000, 9999); word = "DESTRUIR"; checksum = sum(int(x) for x in str(code))
        if input(f"Digite o codigo {code}: ").strip() != str(code): print("Cancelado."); self.pause(); return
        if input(f"Digite {word} ao contrario: ").strip().upper() != word[::-1]: print("Cancelado."); self.pause(); return
        if input(f"Checksum dos digitos de {code}: ").strip() != str(checksum): print("Cancelado."); self.pause(); return
        self.progress("Aplicando Auto Destruction simulado", 1.2, C.RED)
        self.memory["destroyed"] = True; self.state = "destruido"; self.add_history("Auto Destruction aplicado"); self.save_memory()
        self.pause()

    def destroyed_screen(self) -> None:
        self.clear(); self.header(); print(self.c("PEANUT OS COMPACT BLOQUEADO", C.B + C.RED))
        print("O sistema simulado esta destruido na memoria local.")
        print("Va para Aba Comandos e use /help, depois Reparo Fix.")
        print("[1] Aba Comandos")
        print("[2] Sair")
        choice = input("\nEscolha: ").strip()
        if choice == "1": self.command_center()
        elif choice == "2": self.shutdown()

    def command_center(self) -> None:
        while True:
            self.clear(); self.header(); print(self.c("ABA COMANDOS", C.B + C.Y))
            print("Digite /help para ver comandos.")
            cmd = input("PeanutCMD> ").strip()
            if cmd == "/help":
                print("/help | Reparo Fix | status | apps update | notificacoes limpar | memoria reset | browser limpar | sair")
            elif cmd == "Reparo Fix":
                self.memory["destroyed"] = False; self.state = "bootloader"; self.add_history("Sistema reparado por Reparo Fix"); self.save_memory(); print("Peanut OS reparado.")
            elif cmd == "status": print(json.dumps({"versao": VERSION, "estado": self.state, "destruido": self.memory.get("destroyed")}, ensure_ascii=False, indent=2))
            elif cmd == "apps update": self.apps_update()
            elif cmd == "notificacoes limpar": self.memory["notifications"] = []; self.save_memory(); print("Notificacoes limpas.")
            elif cmd == "memoria reset": self.reset_memory(confirm_word="RESET")
            elif cmd == "browser limpar": self.memory["browser_history"] = []; self.save_memory(); print("Historico do navegador limpo.")
            elif cmd == "sair": return
            else: print("Comando desconhecido.")
            self.pause()

    def custom_mods_menu(self) -> None:
        if not self.memory.get("secure_boot_unlocked"):
            print("Secure Boot bloqueado."); self.pause(); return
        while True:
            self.clear(); self.header(); print(self.c("CUSTOM MODS", C.B + C.M))
            mods = self.list_modules(); enabled = set(self.memory.get("enabled_modules", []))
            print("[1] Ativar/desativar Custom Mods")
            print("[2] Listar modulos")
            print("[3] Habilitar modulo")
            print("[4] Desabilitar modulo")
            print("[5] Testar importacao")
            print("[0] Voltar")
            print(f"Encontrados: {len(mods)} | Habilitados: {len(enabled)}")
            ch = input("\nEscolha: ").strip()
            if ch == "1": self.memory["custom_mods_enabled"] = not self.memory.get("custom_mods_enabled"); self.save_memory()
            elif ch == "2": self.show_modules(mods, enabled)
            elif ch == "3": self.enable_module(mods)
            elif ch == "4": self.disable_module()
            elif ch == "5": self.load_enabled_modules(); self.save_memory(); self.pause()
            elif ch == "0": return

    def list_modules(self) -> list[str]:
        return sorted(p.name for p in MODULES_DIR.glob("*.py") if p.name != "__init__.py")

    def show_modules(self, mods: list[str], enabled: set[str]) -> None:
        self.clear(); self.header(); print("MODULOS")
        for name in mods: print(f"- {name} {'[ON]' if name in enabled else '[OFF]'}")
        self.pause()

    def enable_module(self, mods: list[str]) -> None:
        name = self.pick_from_list("HABILITAR MODULO", mods)
        if name:
            enabled = self.memory.setdefault("enabled_modules", [])
            if name not in enabled: enabled.append(name)
            self.save_memory()

    def disable_module(self) -> None:
        enabled = self.memory.setdefault("enabled_modules", [])
        name = self.pick_from_list("DESABILITAR MODULO", enabled)
        if name in enabled:
            enabled.remove(name); self.save_memory()

    def load_enabled_modules(self) -> None:
        if not self.memory.get("custom_mods_enabled"): return
        for name in self.memory.get("enabled_modules", []):
            path = MODULES_DIR / name
            try:
                spec = importlib.util.spec_from_file_location(path.stem, path)
                if not spec or not spec.loader: continue
                mod = importlib.util.module_from_spec(spec); sys.modules[path.stem] = mod; spec.loader.exec_module(mod)
                if hasattr(mod, "activate"):
                    result = mod.activate(self)
                    if result: self.add_notification(str(result), "mod")
            except Exception as error:
                print(f"Erro no modulo {name}: {error}")

    def recovery_mode(self) -> None:
        while True:
            self.clear(); self.state = "recovery"; self.header(); print(self.c("RECOVERY", C.B + C.RED))
            print("[1] Diagnostico")
            print("[2] Reparo Fix")
            print("[3] Resetar memoria")
            print("[4] Bootloader")
            ch = input("\nEscolha: ").strip()
            if ch == "1": self.system_info_app()
            elif ch == "2": self.memory["destroyed"] = False; self.save_memory(); print("Reparado."); self.pause()
            elif ch == "3": self.reset_memory("RESET")
            elif ch == "4": self.state = "bootloader"; self.save_memory(); return

    def notifications_menu(self) -> None:
        while True:
            self.clear(); self.header(); print(self.c("NOTIFICACOES", C.B + C.CY))
            for item in self.memory.get("notifications", [])[-15:]: print(f"#{item['id']} [{'nova' if not item.get('read') else 'lida'}] {item['category']} - {item['message']}")
            print("[1] Marcar lidas  [2] Limpar  [0] Voltar")
            ch = input("\nEscolha: ")
            if ch == "1":
                for item in self.memory.get("notifications", []): item["read"] = True
                self.save_memory()
            elif ch == "2": self.memory["notifications"] = []; self.save_memory()
            elif ch == "0": return

    def memory_menu(self) -> None:
        self.clear(); self.header(); print(self.c("MEMORIA", C.B + C.Y)); print(json.dumps(self.memory, ensure_ascii=False, indent=2)[:3500]); self.pause()

    def settings_app(self) -> None:
        while True:
            self.clear(); self.header(); print("CONFIGURACOES")
            print("[1] Alterar usuario")
            print("[2] Alternar touch do navegador")
            print("[0] Voltar")
            ch = input("\nEscolha: ")
            if ch == "1":
                name = input("Novo usuario: ").strip()
                if name: self.memory["username"] = name; self.save_memory()
            elif ch == "2": self.memory["browser_touch_mode"] = not self.memory.get("browser_touch_mode"); self.save_memory()
            elif ch == "0": return

    def store_app(self) -> None:
        self.clear(); self.header(); print("LOJA DE APPS BETA")
        print("Catalogo beta: Navegador Compact, Notas, Temas, Arquivos, Modulos locais.")
        print("Instalacao real de apps ainda nao implementada."); self.pause()

    def system_info_app(self) -> None:
        self.clear(); self.header(); print("INFORMACOES")
        print(f"Python: {platform.python_version()}")
        print(f"Host: {platform.system()} {platform.release()} {platform.machine()}")
        print(f"Arquivo memoria: {MEMORY_FILE}")
        print(f"Boots: {self.memory.get('boot_count')}")
        self.pause()

    def calculator_app(self) -> None:
        self.clear(); self.header(); print("CALCULADORA")
        expr = input("Expressao simples: ").strip()
        if re.fullmatch(r"[0-9+\-*/(). %]+", expr):
            try: print("Resultado:", eval(expr, {"__builtins__": {}}, {}))
            except Exception: print("Erro no calculo.")
        else: print("Expressao bloqueada por seguranca.")
        self.pause()

    def notes_app(self) -> None:
        while True:
            self.clear(); self.header(); print("NOTAS")
            for i, note in enumerate(self.memory.get("notes", []), 1): print(f"{i}. {note}")
            print("[1] Nova nota  [2] Limpar  [0] Voltar")
            ch = input("\nEscolha: ")
            if ch == "1":
                note = input("Nota: ").strip()
                if note: self.memory.setdefault("notes", []).append(note); self.save_memory()
            elif ch == "2": self.memory["notes"] = []; self.save_memory()
            elif ch == "0": return

    def clock_app(self) -> None:
        self.clear(); self.header(); print("RELOGIO"); print(f"Agora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"); self.pause()

    def files_app(self) -> None:
        self.clear(); self.header(); print("ARQUIVOS SIMULADOS")
        for path in [MEMORY_FILE, MODULES_DIR, BASE_DIR / "VERSION"]: print(f"- {path}")
        self.pause()

    def security_app(self) -> None:
        self.clear(); self.header(); print("SEGURANCA")
        print(f"Secure Boot desbloqueado: {self.memory.get('secure_boot_unlocked')}")
        print(f"Custom Mods: {self.memory.get('custom_mods_enabled')}")
        print(f"Destruido: {self.memory.get('destroyed')}")
        self.pause()

    def themes_app(self) -> None:
        themes = ["peanut-cmd", "blue-terminal", "green-matrix", "mono"]
        picked = self.pick_from_list("TEMAS", themes)
        if picked: self.memory["theme"] = picked; self.save_memory()

    def apps_update(self) -> None:
        self.progress("Atualizando apps internos simulados", 0.8, C.G)
        self.add_notification("Apps internos atualizados para catalogo v0.5.5.", "apps"); self.save_memory()

    def reset_memory(self, confirm_word: str = "RESET") -> None:
        if input(f"Digite {confirm_word} para resetar: ").strip() == confirm_word:
            self.memory = self.default_memory(); self.battery = self.memory["battery"]; self.save_memory(); print("Memoria resetada.")
        else: print("Cancelado.")
        self.pause()


def main() -> None:
    PeanutCompact().bootloader_screen()


if __name__ == "__main__":
    main()
