# Peanut OS Compact v0.3.0 Concept

A versão **0.3.0 Concept** foca no **Bootloader** e deixa o Compact mais vivo no terminal.

## Destaques

- Bootloader inicial antes do sistema ligar
- Secure Boot simulado bloqueado por padrão
- Minigame para desbloquear Secure Boot
- Custom Mods liberados apenas depois do desbloqueio
- Sistema de módulos `.py` carregados da pasta `editions/compact/modules`
- Módulo de teste incluído: `test_module.py`
- Modo Auto Destruction simulado
- Recovery com reparo do Auto Destruction
- Animações de boot, progresso e encerramento
- Cores ANSI no terminal

## Segurança

Esta versão **não mexe no boot real**, BIOS/UEFI, Secure Boot real, disco, partições, sistema operacional instalado ou arquivos pessoais.

O Auto Destruction é apenas uma simulação dentro do arquivo de memória do Peanut OS. Ele marca o estado interno como destruído e bloqueia o boot simulado até o usuário reparar pelo recovery.

## Como os módulos funcionam

Os módulos ficam em:

```text
editions/compact/modules/
```

Cada módulo deve ser um arquivo `.py` com uma função:

```python
def activate(system):
    # system é a instância do PeanutCompact
    return "Mensagem opcional de notificação"
```

Para usar:

1. Abra o Peanut OS Compact.
2. Entre no Bootloader.
3. Desbloqueie o Secure Boot pelo minigame.
4. Entre em Custom Mods.
5. Ative Custom Mods.
6. Habilite o módulo desejado.
7. Reinicie/ligue o sistema para carregar o módulo.

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
