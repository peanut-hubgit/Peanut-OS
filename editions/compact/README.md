# Peanut OS Compact

O **Peanut OS Compact** é a edição de terminal do projeto: um **sistema operacional simulado em Python**, com sensação de `.bat`, menu textual, Bootloader, Secure Boot simulado, Custom Mods próprios, notificações internas, memória armazenada, apps internos e aba de comandos.

Ele não tenta substituir Windows, Linux, Android ou macOS. A ideia é criar uma experiência própria, leve e educacional, como se o usuário estivesse ligando um mini sistema dentro do terminal.

## Versão atual

**v0.4.0 Concept**

Arquivo principal:

```text
editions/compact/peanut_os_compact.py
```

## Como executar

Na raiz do repositório:

```bash
python editions/compact/peanut_os_compact.py
```

No Windows:

```powershell
py editions/compact/peanut_os_compact.py
```

No Termux:

```bash
pkg update && pkg upgrade -y
pkg install python git -y
git clone https://github.com/peanut-hubgit/Peanut-OS.git
cd Peanut-OS
python editions/compact/peanut_os_compact.py
```

## Conceito atual

A v0.4.0 começa pelo **Bootloader**:

```text
Peanut OS Compact - v0.4.0 Concept

Bateria: 30% | Hora: 14:30 | Estado: bootloader
Secure Boot: LOCKED | Custom Mods: OFF | Destruction: NAO
Apps: 12 | Notificacoes nao lidas: 1

BOOTLOADER COMPACT

[1] Boot normal
[2] Desbloquear Secure Boot (minigame avancado)
[3] Custom Mods
[4] Modo Recovery
[5] Auto Destruction permanente do Peanut OS
[6] Aba Comandos
[7] Sair
```

## Incluído na v0.4.0 Concept

- Bootloader inicial antes do sistema ligar
- Secure Boot com minigame mais interativo e mais difícil
- Auto Destruction com minigame próprio
- Auto Destruction persistente dentro da memória local do Peanut OS
- Aba Comandos com `/help`
- Comando `Reparo Fix` para reparar o Peanut OS após Auto Destruction
- Atualização de apps internos do sistema
- 12 apps internos iniciais
- App de Configurações
- App de Loja de Apps Beta
- Custom Mods próprios do Peanut OS
- Importação real de módulos `.py` locais
- Módulo de teste em `editions/compact/modules/test_module.py`
- Animações de carregamento, boot, barra de progresso e encerramento
- Cores ANSI no terminal
- Sistema de notificações internas
- Memória armazenada em `peanut_memory.json`
- Nenhuma dependência externa obrigatória

## Apps internos

1. Configurações
2. Loja de Apps Beta
3. Notificações
4. Memória
5. Informações
6. Calculadora
7. Notas
8. Relógio
9. Arquivos
10. Segurança
11. Temas
12. Comandos

## Aba Comandos

Comandos disponíveis:

```text
/help
Reparo Fix
status
apps update
notificacoes limpar
memoria reset
sair
```

O comando mais importante da v0.4.0 é:

```text
Reparo Fix
```

Ele repara o estado de Auto Destruction e libera o boot novamente.

## Custom Mods

Os módulos ficam em:

```text
editions/compact/modules/
```

Cada módulo deve ser um arquivo `.py` com uma função:

```python
def activate(system):
    return "Mensagem opcional para notificação"
```

O objeto `system` representa a instância do Peanut OS Compact. O módulo pode adicionar histórico, notificações e alterar dados da memória simulada.

Fluxo para usar módulos:

1. Abra o Peanut OS Compact.
2. Desbloqueie o Secure Boot pelo minigame.
3. Entre em Custom Mods.
4. Ative Custom Mods.
5. Habilite um módulo.
6. Reinicie/ligue o sistema para carregar os módulos ativados.

## Auto Destruction permanente do Peanut OS

O Auto Destruction é permanente **apenas dentro da memória local do Peanut OS Compact**.

Ele não destrói aparelho real, disco, partição, sistema operacional, boot real, BIOS/UEFI ou arquivos pessoais.

Depois de ativado, o boot simulado fica bloqueado até o usuário entrar na aba Comandos e digitar:

```text
Reparo Fix
```

## Memória armazenada

Ao executar, o Compact cria automaticamente o arquivo:

```text
editions/compact/peanut_memory.json
```

Esse arquivo guarda dados simples da simulação, como:

- nome do usuário
- bateria simulada
- último estado salvo
- quantidade de boots
- notificações
- histórico básico de eventos
- estado do Secure Boot
- Custom Mods ativados
- módulos habilitados
- estado do Auto Destruction
- apps internos
- histórico de atualização de apps
- tema selecionado

Esse arquivo é local e não deve ser tratado como banco de dados real.

## Objetivos

- Simular boot, desligamento, reinicialização e estados do sistema
- Ter visual de terminal parecido com `.bat`, mas usando Python
- Criar uma experiência de Bootloader própria
- Permitir mods locais controlados dentro da simulação
- Mostrar informações como hora, bateria, estado e mensagens do sistema
- Adicionar apps internos simples e úteis
- Servir como primeira base jogável/testável do Peanut OS
- Rodar em computadores simples e também no Termux/Pydroid, quando possível
- Manter o código simples para aprendizado e evolução

## Roadmap

- [ ] Melhorar estabilidade da memória local
- [ ] Criar mais apps internos
- [ ] Melhorar Loja de Apps Beta
- [ ] Criar sistema de atualização de módulos
- [ ] Melhorar os minigames do Bootloader
- [ ] Criar documentação para desenvolvedores de módulos
- [ ] Lançar a **v1.0 estável** com pelo menos **30 funcionalidades**

## Estados

- `desligado`
- `bootloader`
- `ligando`
- `ligado`
- `recovery`
- `reiniciando`
- `encerrando`
- `destruido`

## Fora do escopo inicial

- Kernel próprio
- Drivers próprios
- Particionamento real
- Alteração real do sistema instalado
- Substituição real do sistema operacional do computador
- Compatibilidade completa com aplicativos de Windows, Linux ou Android
- Notificações reais do sistema hospedeiro
- Desbloqueio de Secure Boot real
- Alterações reais de boot, BIOS, UEFI ou Android

## Requisitos

- Python 3.10+

Dependências opcionais futuras: `colorama`, `rich` e `pyfiglet`. A versão atual roda apenas com Python puro.

## Notas da versão

- [`v0.1.0 Concept`](../../docs/releases/compact-v0.1.0-concept.md)
- [`v0.2.0 Concept`](../../docs/releases/compact-v0.2.0-concept.md)
- [`v0.3.0 Concept`](../../docs/releases/compact-v0.3.0-concept.md)
- [`v0.4.0 Concept`](../../docs/releases/compact-v0.4.0-concept.md)

## Estado

Prova de conceito em evolução. A v0.4.0 transforma o Bootloader em centro do sistema, adiciona a aba Comandos e começa a estruturar o Peanut OS Compact como um mini sistema com apps internos.
