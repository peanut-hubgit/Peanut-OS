# Peanut OS Compact v0.4.0 Concept

A v0.4.0 expande o Peanut OS Compact com foco em Bootloader, comandos internos, apps do sistema e destruição local persistente dentro da simulação.

## Destaques

- Secure Boot com minigame mais interativo e mais difícil
- Auto Destruction com minigame próprio
- Auto Destruction agora persistente na memória local do Peanut OS
- Nova aba Comandos
- Comando `/help`
- Comando `Reparo Fix` para reparar o Peanut OS após Auto Destruction
- Atualização de apps internos do sistema
- 12 apps internos iniciais
- Loja de Apps Beta
- App de Configurações
- Mais animações de carregamento e progresso
- Mais uso de cores ANSI no terminal
- Remoção de comparações com projetos externos no texto do sistema

## Apps internos adicionados

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

## Comandos disponíveis

```text
/help
Reparo Fix
status
apps update
notificacoes limpar
memoria reset
sair
```

## Auto Destruction

O Auto Destruction é permanente somente dentro da memória local do Peanut OS Compact. Ele não altera sistema real, boot real, BIOS/UEFI, Android, Windows, disco, partições ou drivers.

Para reparar:

```text
/help
Reparo Fix
```

## Arquivo principal

```text
editions/compact/peanut_os_compact.py
```

## Como executar

```bash
python editions/compact/peanut_os_compact.py
```

No Windows:

```powershell
py editions/compact/peanut_os_compact.py
```
