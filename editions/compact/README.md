# Peanut OS Compact

O **Peanut OS Compact** é a edição de terminal do projeto: um **sistema operacional simulado em Python**, com sensação de `.bat`, menu textual, Bootloader, Secure Boot simulado, Custom Mods, notificações internas e memória armazenada.

Ele não tenta substituir Windows, Linux, Android ou macOS. A ideia é criar uma experiência própria, leve e educacional, como se o usuário estivesse ligando um mini sistema dentro do terminal.

## Versão atual

**v0.3.0 Concept**

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

## Conceito atual

A v0.3.0 começa pelo **Bootloader**:

```text
Peanut OS Compact - v0.3.0 Concept

Bateria: 30% | Hora: 14:30 | Estado: bootloader
Secure Boot: LOCKED | Custom Mods: OFF | Destruction: NAO

BOOTLOADER COMPACT

[1] Boot normal
[2] Desbloquear Secure Boot (minigame)
[3] Custom Mods
[4] Modo Recovery
[5] Auto Destruction simulado
[6] Sair
```

## Incluído na v0.3.0 Concept

- Bootloader inicial antes do sistema ligar
- Secure Boot simulado bloqueado por padrão
- Minigame de desbloqueio do Secure Boot
- Custom Mods liberados somente após o desbloqueio
- Importação real de módulos `.py` locais
- Módulo de teste em `editions/compact/modules/test_module.py`
- Auto Destruction simulado dentro da memória do Peanut OS
- Recovery com opção de reparar o Auto Destruction
- Animações de carregamento, boot, barra de progresso e encerramento
- Cores ANSI no terminal
- Sistema de notificações internas
- Memória armazenada em `peanut_memory.json`
- Nenhuma dependência externa obrigatória

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
2. Entre no Bootloader.
3. Desbloqueie o Secure Boot pelo minigame.
4. Entre em Custom Mods.
5. Ative Custom Mods.
6. Habilite um módulo.
7. Reinicie/ligue o sistema para carregar os módulos ativados.

## Auto Destruction simulado

O Auto Destruction **não destrói aparelho real, disco, partição, sistema operacional, boot real, BIOS/UEFI ou arquivos pessoais**.

Ele apenas marca o arquivo de memória do Peanut OS como destruído. Depois disso, o boot simulado fica bloqueado até o usuário entrar no Recovery e reparar.

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
- estado do Auto Destruction simulado

Esse arquivo é local e não deve ser tratado como banco de dados real.

## Objetivos

- Simular boot, desligamento, reinicialização e estados do sistema
- Ter visual de terminal parecido com `.bat`, mas usando Python
- Criar uma experiência de Bootloader própria
- Permitir mods locais controlados dentro da simulação
- Mostrar informações como hora, bateria, estado e mensagens do sistema
- Servir como primeira base jogável/testável do Peanut OS
- Rodar em computadores simples e também no Termux/Pydroid, quando possível
- Manter o código simples para aprendizado e evolução

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

## Estado

Prova de conceito em evolução. A v0.3.0 estabelece o Bootloader como a nova porta de entrada do Peanut OS Compact.
