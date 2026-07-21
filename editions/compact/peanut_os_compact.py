from __future__ import annotations
import html.parser, importlib.util, json, os, platform, random, re, sys, time, urllib.request, urllib.error
from datetime import datetime
from pathlib import Path
from typing import Any

VERSION = "0.5.0 Concept"
SYSTEM_NAME = "Peanut OS Compact"
BASE_DIR = Path(__file__).resolve().parent
MEMORY_FILE = BASE_DIR / "peanut_memory.json"
MODULES_DIR = BASE_DIR / "modules"
ROM_LIMIT_MB = 1024

class C:
    R="\033[0m"; B="\033[1m"; D="\033[2m"; RED="\033[31m"; G="\033[32m"; Y="\033[33m"; BL="\033[34m"; M="\033[35m"; CY="\033[36m"; W="\033[37m"

class PageParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(); self.title=[]; self.text=[]; self.links=[]; self.in_title=False; self.skip=False; self.href=None; self.link_text=[]
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if tag in ("script","style","noscript","svg"): self.skip=True
        if tag=="title": self.in_title=True
        if tag=="a" and attrs.get("href"): self.href=attrs["href"]; self.link_text=[]
    def handle_endtag(self, tag):
        if tag in ("script","style","noscript","svg"): self.skip=False
        if tag=="title": self.in_title=False
        if tag=="a" and self.href:
            label=" ".join("".join(self.link_text).split())
            if label: self.links.append((label[:70], self.href))
            self.href=None; self.link_text=[]
        if tag in ("p","br","div","section","article","li","h1","h2","h3"): self.text.append("\n")
    def handle_data(self, data):
        if self.skip: return
        clean=" ".join(data.split())
        if not clean: return
        if self.in_title: self.title.append(clean)
        elif self.href is not None: self.link_text.append(clean)
        else: self.text.append(clean+" ")
    def title_text(self): return " ".join(self.title).strip() or "Sem titulo"
    def body_text(self):
        text="".join(self.text)
        text=re.sub(r"\n\s*\n+","\n\n", text)
        text=re.sub(r"[ \t]+"," ", text)
        return text.strip()

class PeanutCompact:
    def __init__(self):
        MODULES_DIR.mkdir(exist_ok=True)
        self.memory=self.load()
        self.running=True
        self.state=self.memory.get("last_state","desligado")
        self.schema()
        self.tick_battery()
        if not self.memory["notifications"]:
            self.notify("Peanut OS Compact pronto.","sistema")
        self.save()

    def defaults(self)->dict[str,Any]:
        now=time.time()
        return {
            "first_setup_done":False,"username":"Usuario Compact","accent":"cyan",
            "battery":random.randint(45,95),"charging":False,"last_battery_update":now,
            "rom_limit_mb":ROM_LIMIT_MB,"storage_used_mb":64,
            "last_state":"desligado","boot_count":0,"notifications":[],"history":[],
            "secure_boot_unlocked":False,"custom_mods_enabled":False,"enabled_modules":[],
            "destroyed":False,"bootloader_attempts":0,"notes":[],"browser_history":[],
            "installed_beta_apps":[],"apps_last_update":"nunca"
        }

    def schema(self):
        d=self.defaults()
        for k,v in d.items(): self.memory.setdefault(k,v)
        self.memory["battery"]=int(self.memory.get("battery",70))
        self.memory["storage_used_mb"]=int(self.memory.get("storage_used_mb",64))
        self.memory["rom_limit_mb"]=int(self.memory.get("rom_limit_mb",ROM_LIMIT_MB))

    def load(self):
        if MEMORY_FILE.exists():
            try:
                with MEMORY_FILE.open("r",encoding="utf-8") as f: data=json.load(f)
                if isinstance(data,dict): return {**self.defaults(),**data}
            except Exception: pass
        return self.defaults()

    def save(self):
        self.memory["last_state"]=self.state
        with MEMORY_FILE.open("w",encoding="utf-8") as f: json.dump(self.memory,f,ensure_ascii=False,indent=2)

    def color(self, text, col): return f"{col}{text}{C.R}"
    def accent(self):
        return {"cyan":C.CY,"green":C.G,"yellow":C.Y,"blue":C.BL,"magenta":C.M,"white":C.W}.get(self.memory.get("accent"),C.CY)
    def clear(self): os.system("cls" if os.name=="nt" else "clear")
    def pause(self): input("\nPressione ENTER para continuar...")
    def now(self): return datetime.now().strftime("%H:%M")
    def stamp(self): return datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    def hist(self,msg):
        h=self.memory.setdefault("history",[]); h.append({"time":self.stamp(),"action":msg}); del h[:-50]
    def notify(self,msg,cat="geral"):
        n=self.memory.setdefault("notifications",[])
        n.append({"id":len(n)+1,"time":self.stamp(),"category":cat,"message":msg,"read":False}); del n[:-60]
    def unread(self): return sum(1 for n in self.memory["notifications"] if not n.get("read"))
    def storage_pct(self): return min(100,int((self.memory["storage_used_mb"]/max(1,self.memory["rom_limit_mb"]))*100))
    def add_storage(self,mb,reason):
        if self.memory["storage_used_mb"]+mb>self.memory["rom_limit_mb"]:
            self.notify(f"ROM cheia: nao foi possivel salvar {reason}.","armazenamento"); self.save(); return False
        self.memory["storage_used_mb"]+=mb; return True

    def tick_battery(self):
        now=time.time(); last=float(self.memory.get("last_battery_update",now)); elapsed=max(0,int(now-last))
        if elapsed<1: return
        if self.memory.get("charging"):
            gain=elapsed//35
            if gain: self.memory["battery"]=min(100,self.memory["battery"]+gain); self.memory["last_battery_update"]=now
        else:
            loss=elapsed//90
            if loss: self.memory["battery"]=max(0,self.memory["battery"]-loss); self.memory["last_battery_update"]=now
        if self.memory["battery"]<=5 and not self.memory.get("charging"): self.notify("Bateria critica. Ative carregamento.","energia")

    def battery_icon(self):
        b=self.memory["battery"]
        if self.memory.get("charging"): return "⚡"
        return "████" if b>=75 else "███░" if b>=50 else "██░░" if b>=25 else "█░░░" if b>=10 else "░░░░"

    def banner(self,title):
        a=self.accent(); w=68
        print(self.color("╔"+"═"*(w-2)+"╗",a))
        print(self.color("║"+f" {title} ".center(w-2)+"║",a+C.B))
        print(self.color("╚"+"═"*(w-2)+"╝",a))

    def header(self):
        self.tick_battery()
        a=self.accent()
        lock="UNLOCKED" if self.memory["secure_boot_unlocked"] else "LOCKED"
        mods="ON" if self.memory["custom_mods_enabled"] else "OFF"
        print(self.color("═"*70,a))
        print(self.color(f"{SYSTEM_NAME} - v{VERSION}",C.B+C.Y))
        print(self.color("═"*70,a))
        print(f"Usuario: {self.memory['username']} | Hora: {self.now()} | Estado: {self.state}")
        print(f"Bateria: {self.memory['battery']}% {self.battery_icon()} | ROM: {self.memory['storage_used_mb']}/{self.memory['rom_limit_mb']} MB ({self.storage_pct()}%)")
        print(f"Secure Boot: {lock} | Custom Mods: {mods} | Destruction: {'SIM' if self.memory['destroyed'] else 'NAO'}")
        print(f"Notificacoes nao lidas: {self.unread()}")
        print(self.color("═"*70,a)); print()

    def progress(self,label,seconds=.8,col=None):
        col=col or self.accent(); print(label)
        for i in range(25):
            print("\r["+self.color("█"*i,col)+"░"*(24-i)+f"] {int(i/24*100)}%",end=""); time.sleep(seconds/25)
        print("\n")

    def welcome(self):
        self.clear(); self.banner("BEM-VINDO AO PEANUT OS COMPACT")
        print("Primeiro uso detectado. Configure seu mini sistema.\n")
        name=input("Nome de usuario: ").strip() or "Usuario Compact"
        colors=["cyan","green","yellow","blue","magenta","white"]
        for i,c in enumerate(colors,1): print(f"[{i}] {c}")
        ch=input("\nCor principal: ").strip()
        accent=colors[int(ch)-1] if ch.isdigit() and 1<=int(ch)<=len(colors) else "cyan"
        print("\n[1] Normal\n[2] Carregando")
        self.memory["charging"]=input("Modo inicial: ").strip()=="2"
        self.memory["username"]=name; self.memory["accent"]=accent; self.memory["first_setup_done"]=True
        self.notify(f"Bem-vindo, {name}. Perfil inicial criado.","setup"); self.hist("Primeiro uso concluido"); self.save()
        self.progress("Aplicando personalizacoes"); self.pause()

    def bootloader(self):
        if not self.memory["first_setup_done"]: self.welcome()
        while self.running:
            self.clear(); self.state="bootloader"; self.save(); self.header()
            if self.memory["destroyed"]: self.destroyed_screen(); return
            self.banner("BOOTLOADER COMPACT")
            print("[1] Boot normal\n[2] Desbloquear Secure Boot\n[3] Custom Mods\n[4] Recovery\n[5] Auto Destruction\n[6] Comandos\n[7] Carregamento\n[8] Sair")
            op=input("\nOpcao: ").strip()
            if op=="1": self.boot(); self.main_menu()
            elif op=="2": self.secure_game()
            elif op=="3": self.mods_menu()
            elif op=="4": self.recovery()
            elif op=="5": self.auto_destroy()
            elif op=="6": self.commands()
            elif op=="7": self.toggle_charge()
            elif op=="8": self.shutdown()
            else: self.pause()

    def boot(self):
        if self.memory["battery"]<=0 and not self.memory["charging"]:
            print("Bateria zerada. Ative carregamento."); self.pause(); return
        self.clear(); self.state="ligando"; self.hist("Boot iniciado"); self.save(); self.header()
        for s in ["Verificando memoria","Checando ROM de 1 GB","Sincronizando bateria","Carregando apps","Preparando navegador","Importando modulos"]:
            print(self.color("> "+s,self.accent())); time.sleep(.18)
        self.load_modules(); self.progress("Finalizando boot",.9,C.G)
        self.state="ligado"; self.memory["boot_count"]+=1; self.notify("Peanut OS ligado.","boot"); self.hist("Boot concluido"); self.save(); self.pause()

    def main_menu(self):
        while self.running and self.state=="ligado":
            self.clear(); self.header(); self.banner("MENU PRINCIPAL")
            print("[1] Apps\n[2] Navegador interno\n[3] Notificacoes\n[4] Memoria/ROM\n[5] Comandos\n[6] Reiniciar\n[7] Recovery\n[8] Desligar")
            op=input("\nOpcao: ").strip()
            if op=="1": self.apps()
            elif op=="2": self.browser()
            elif op=="3": self.notifications()
            elif op=="4": self.memory_app()
            elif op=="5": self.commands()
            elif op=="6": self.reboot()
            elif op=="7": self.recovery()
            elif op=="8": self.shutdown()

    def apps(self):
        names=["Configuracoes","Loja Beta","Notificacoes","Memoria","Informacoes","Calculadora","Notas","Relogio","Arquivos","Seguranca","Temas","Comandos","Navegador"]
        funcs=[self.settings,self.store,self.notifications,self.memory_app,self.info,self.calc,self.notes,self.clock,self.files,self.security,self.themes,self.commands,self.browser]
        while True:
            self.clear(); self.header(); self.banner("APPS DO SISTEMA")
            for i,n in enumerate(names,1): print(f"[{i}] {n}")
            print("[0] Voltar"); op=input("\nApp: ").strip()
            if op=="0": return
            if op.isdigit() and 1<=int(op)<=len(funcs): funcs[int(op)-1]()

    def browser(self):
        while True:
            self.clear(); self.header(); self.banner("NAVEGADOR TEXTUAL REAL")
            print("Digite URL real. Ex: https://example.com\n[h] Historico | [v] Voltar")
            url=input("\nURL: ").strip()
            if url.lower()=="v": return
            if url.lower()=="h": self.browser_history(); continue
            if not url: continue
            if not url.startswith(("http://","https://")): url="https://"+url
            self.open_url(url)

    def open_url(self,url):
        self.clear(); self.header(); self.banner("CARREGANDO PAGINA"); print(url)
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"PeanutOSCompact/0.5"})
            with urllib.request.urlopen(req,timeout=10) as r:
                raw=r.read(180000); ctype=r.headers.get("Content-Type","desconhecido")
            p=PageParser(); p.feed(raw.decode("utf-8",errors="replace"))
            title=p.title_text(); body=p.body_text()[:3500] or "(Sem texto legivel.)"
            self.memory["browser_history"].append({"time":self.stamp(),"url":url,"title":title}); del self.memory["browser_history"][:-20]
            self.add_storage(1,"historico do navegador"); self.hist("Navegador abriu "+url); self.save()
            self.clear(); self.header(); self.banner("PAGINA CARREGADA")
            print(f"URL: {url}\nTitulo: {title}\nTipo: {ctype}\n"); print(body)
            if p.links[:10]:
                print("\nLinks:")
                for i,(label,href) in enumerate(p.links[:10],1): print(f"{i}. {label} -> {href}")
        except (urllib.error.URLError, TimeoutError, ValueError) as e:
            print(self.color(f"Erro ao abrir pagina: {e}",C.RED))
        self.pause()

    def browser_history(self):
        self.clear(); self.header(); self.banner("HISTORICO DO NAVEGADOR")
        for item in self.memory["browser_history"][-10:]: print(f"- {item['time']} | {item['title']}\n  {item['url']}")
        self.pause()

    def settings(self):
        while True:
            self.clear(); self.header(); self.banner("CONFIGURACOES")
            print("[1] Nome\n[2] Cor\n[3] Carregamento\n[4] Voltar")
            op=input("\nOpcao: ").strip()
            if op=="1":
                n=input("Novo nome: ").strip()
                if n: self.memory["username"]=n; self.save()
            elif op=="2": self.choose_color()
            elif op=="3": self.toggle_charge()
            elif op=="4": return

    def choose_color(self):
        colors=["cyan","green","yellow","blue","magenta","white"]
        for i,c in enumerate(colors,1): print(f"[{i}] {c}")
        op=input("Cor: ").strip()
        if op.isdigit() and 1<=int(op)<=len(colors): self.memory["accent"]=colors[int(op)-1]; self.save()

    def toggle_charge(self):
        self.memory["charging"]=not self.memory["charging"]; self.notify("Carregamento "+("ativado" if self.memory["charging"] else "desativado"),"energia"); self.save(); self.pause()

    def store(self):
        apps=["Peanut Paint CLI","Mini Agenda","Gerador de Senhas","Leitor RSS futuro"]
        while True:
            self.clear(); self.header(); self.banner("LOJA DE APPS BETA")
            inst=set(self.memory["installed_beta_apps"])
            for i,a in enumerate(apps,1): print(f"[{i}] {a} - {'instalado' if a in inst else 'disponivel'}")
            print("[5] Atualizar apps\n[0] Voltar")
            op=input("\nOpcao: ").strip()
            if op=="0": return
            if op=="5": self.update_apps()
            elif op.isdigit() and 1<=int(op)<=len(apps):
                app=apps[int(op)-1]
                if app not in inst and self.add_storage(12,app): self.memory["installed_beta_apps"].append(app); self.notify(app+" instalado.","loja"); self.save()

    def update_apps(self):
        self.progress("Atualizando apps",1,C.G); self.memory["apps_last_update"]=self.stamp(); self.notify("Apps atualizados.","apps"); self.save()

    def notifications(self):
        while True:
            self.clear(); self.header(); self.banner("NOTIFICACOES")
            for n in self.memory["notifications"][-12:]: print(f"#{n['id']} [{'lida' if n.get('read') else 'nova'}] {n['category']} - {n['message']}")
            print("\n[1] Marcar lidas\n[2] Teste\n[3] Limpar\n[4] Voltar")
            op=input("\nOpcao: ").strip()
            if op=="1":
                for n in self.memory["notifications"]: n["read"]=True
                self.save()
            elif op=="2": self.notify("Notificacao de teste.","teste"); self.save()
            elif op=="3": self.memory["notifications"]=[]; self.save()
            elif op=="4": return

    def memory_app(self):
        while True:
            self.clear(); self.header(); self.banner("MEMORIA E ROM")
            print(f"ROM simulada: {self.memory['storage_used_mb']}/{self.memory['rom_limit_mb']} MB ({self.storage_pct()}%)")
            print(f"Boots: {self.memory['boot_count']} | Historico: {len(self.memory['history'])}")
            print("[1] Historico\n[2] Liberar 50 MB cache\n[3] Resetar memoria\n[4] Voltar")
            op=input("\nOpcao: ").strip()
            if op=="1":
                for h in self.memory["history"][-20:]: print(f"- {h['time']}: {h['action']}")
                self.pause()
            elif op=="2": self.memory["storage_used_mb"]=max(64,self.memory["storage_used_mb"]-50); self.save()
            elif op=="3": self.reset_memory(); return
            elif op=="4": return

    def info(self):
        self.clear(); self.header(); self.banner("INFORMACOES")
        print(f"Python: {platform.python_version()}\nHospedeiro: {platform.system()} {platform.release()}\nMaquina: {platform.machine()}\nMemoria: {MEMORY_FILE}")
        self.pause()

    def calc(self):
        self.clear(); self.header(); self.banner("CALCULADORA")
        expr=input("Conta: ")
        if re.fullmatch(r"[0-9+\-*/(). ]+",expr):
            try: print("Resultado:",eval(expr,{"__builtins__":{}},{}))
            except Exception as e: print("Erro:",e)
        else: print("Expressao bloqueada.")
        self.pause()

    def notes(self):
        while True:
            self.clear(); self.header(); self.banner("NOTAS")
            for i,n in enumerate(self.memory["notes"][-8:],1): print(f"{i}. {n}")
            print("[1] Nova\n[2] Limpar\n[3] Voltar")
            op=input("\nOpcao: ")
            if op=="1":
                n=input("Nota: ").strip()
                if n and self.add_storage(1,"nota"): self.memory["notes"].append(n[:200]); self.save()
            elif op=="2": self.memory["notes"]=[]; self.save()
            elif op=="3": return

    def clock(self): self.clear(); self.header(); self.banner("RELOGIO"); print(datetime.now().strftime("%d/%m/%Y %H:%M:%S")); self.pause()
    def files(self):
        self.clear(); self.header(); self.banner("ARQUIVOS")
        for p in sorted(BASE_DIR.iterdir()): print(f"- {p.name} ({'pasta' if p.is_dir() else 'arquivo'})")
        self.pause()
    def security(self): self.clear(); self.header(); self.banner("SEGURANCA"); print(json.dumps({k:self.memory[k] for k in ["secure_boot_unlocked","custom_mods_enabled","destroyed","bootloader_attempts"]},indent=2)); self.pause()
    def themes(self): self.clear(); self.header(); self.banner("TEMAS"); self.choose_color(); self.pause()

    def commands(self):
        while True:
            self.clear(); self.header(); self.banner("COMANDOS")
            cmd=input("Digite /help: ").strip()
            if cmd=="/help": print("/help\nReparo Fix\nstatus\napps update\nnotificacoes limpar\nmemoria reset\ncarregar on\ncarregar off\nsair"); self.pause()
            elif cmd=="Reparo Fix": self.memory["destroyed"]=False; self.state="bootloader"; self.notify("Sistema reparado.","reparo"); self.save(); self.pause()
            elif cmd=="status": self.info()
            elif cmd=="apps update": self.update_apps()
            elif cmd=="notificacoes limpar": self.memory["notifications"]=[]; self.save()
            elif cmd=="memoria reset": self.reset_memory(); return
            elif cmd=="carregar on": self.memory["charging"]=True; self.save()
            elif cmd=="carregar off": self.memory["charging"]=False; self.save()
            elif cmd=="sair": return
            else: print("Comando desconhecido."); self.pause()

    def recovery(self):
        self.state="recovery"; self.save()
        while True:
            self.clear(); self.header(); self.banner("RECOVERY")
            print("[1] Diagnostico\n[2] Reparo Fix\n[3] Limpar notificacoes\n[4] Resetar memoria\n[5] Voltar")
            op=input("\nOpcao: ")
            if op=="1": self.info()
            elif op=="2": self.memory["destroyed"]=False; self.save()
            elif op=="3": self.memory["notifications"]=[]; self.save()
            elif op=="4": self.reset_memory(); return
            elif op=="5": self.state="desligado"; self.save(); return

    def secure_game(self):
        self.clear(); self.header(); self.banner("SECURE BOOT CHALLENGE")
        seq=[random.choice(["A","B","X","Y","L","R"]) for _ in range(7)]
        print("Memorize:", " ".join(seq)); time.sleep(2.6); self.clear()
        if input("Sequencia: ").upper().split()!=seq: return self.secure_fail()
        a,b,c=random.randint(6,18),random.randint(2,9),random.randint(10,40)
        if input(f"({a} x {b}) + {c} = ").strip()!=str(a*b+c): return self.secure_fail()
        word=random.choice(["PEANUT","COMPACT","BOOT","SYSTEM"])
        if input(f"Digite {word} ao contrario: ").upper().strip()!=word[::-1]: return self.secure_fail()
        self.memory["secure_boot_unlocked"]=True; self.hist("Secure Boot desbloqueado"); self.notify("Secure Boot desbloqueado.","bootloader"); self.save(); self.progress("Validando token",1,C.G); self.pause()
    def secure_fail(self): self.memory["bootloader_attempts"]+=1; self.notify("Falha no Secure Boot.","bootloader"); self.save(); print("Falha."); self.pause()

    def mods_menu(self):
        while True:
            self.clear(); self.header(); self.banner("CUSTOM MODS")
            if not self.memory["secure_boot_unlocked"]: print("Secure Boot bloqueado."); self.pause(); return
            mods=sorted(p.name for p in MODULES_DIR.glob("*.py") if p.name!="__init__.py")
            print("[1] Ativar/desativar\n[2] Listar\n[3] Habilitar\n[4] Desabilitar\n[5] Testar\n[6] Voltar")
            op=input("\nOpcao: ")
            if op=="1": self.memory["custom_mods_enabled"]=not self.memory["custom_mods_enabled"]; self.save()
            elif op=="2": print("\n".join(mods) or "Nenhum modulo."); self.pause()
            elif op=="3":
                name=input("Modulo: ").strip()
                if name in mods and name not in self.memory["enabled_modules"]: self.memory["enabled_modules"].append(name); self.save()
            elif op=="4":
                name=input("Modulo: ").strip()
                if name in self.memory["enabled_modules"]: self.memory["enabled_modules"].remove(name); self.save()
            elif op=="5": self.load_modules(); self.pause()
            elif op=="6": return

    def load_modules(self):
        if not self.memory["custom_mods_enabled"]: print(self.color("Custom Mods desativado.",C.D)); return
        for mf in self.memory["enabled_modules"]:
            path=MODULES_DIR/mf
            if not path.exists(): continue
            try:
                spec=importlib.util.spec_from_file_location(path.stem,path); mod=importlib.util.module_from_spec(spec); sys.modules[path.stem]=mod; spec.loader.exec_module(mod)
                if hasattr(mod,"activate"):
                    res=mod.activate(self); print("Modulo carregado:",mf)
                    if res: self.notify(str(res),"mod")
            except Exception as e: print("Erro no modulo",mf,e)

    def auto_destroy(self):
        self.clear(); self.header(); self.banner("AUTO DESTRUCTION")
        code=str(random.randint(1000,9999)); word=random.choice(["DESTRUIR","COMPACT","PEANUT"]); total=sum(map(int,code))
        print("Bloqueio permanente apenas dentro do Peanut OS. Reparo: Comandos > Reparo Fix\n")
        print("Codigo:",code)
        ok=input("Codigo: ").strip()==code and input(f"{word} ao contrario: ").upper().strip()==word[::-1] and input("Soma dos digitos: ").strip()==str(total)
        if ok: self.memory["destroyed"]=True; self.state="destruido"; self.save(); self.progress("Bloqueando instancia local",1.2,C.RED)
        else: print("Cancelado.")
        self.pause()

    def destroyed_screen(self):
        while self.running and self.memory["destroyed"]:
            self.clear(); self.state="destruido"; self.header(); self.banner("PEANUT OS BLOQUEADO")
            print("Use Comandos e digite: Reparo Fix")
            print("[1] Comandos\n[2] Sair")
            op=input("\nOpcao: ")
            if op=="1": self.commands()
            elif op=="2": self.shutdown()

    def reboot(self): self.state="reiniciando"; self.save(); self.progress("Reiniciando",.8); self.boot()
    def shutdown(self): self.state="encerrando"; self.save(); self.progress("Encerrando",.7,C.Y); self.state="desligado"; self.save(); self.running=False
    def reset_memory(self):
        if input("Digite RESET: ")=="RESET":
            self.memory=self.defaults(); self.state="desligado"; self.notify("Memoria recriada.","recovery"); self.save()
        self.pause()

def main(): PeanutCompact().bootloader()
if __name__=="__main__": main()
