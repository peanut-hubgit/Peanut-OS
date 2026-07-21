# Peanut OS Compact v0.1.0 Concept

Primeira versão conceitual do **Peanut OS Compact**.

Esta versão não tenta substituir um sistema operacional real. Ela apresenta apenas o conceito inicial: um mini ambiente de sistema simulado em terminal, feito em Python, com aparência parecida com menus `.bat`, mas com estrutura em código Python.

## Incluído

- Tela inicial com bateria simulada, hora atual e estado do sistema
- Estados básicos:
  - desligado
  - ligando
  - ligado
  - recovery
  - reiniciando
  - encerrando
- Menu inicial:
  - ligar
  - entrar em modo recovery
  - sair
- Menu principal após boot
- Modo recovery básico
- Diagnóstico básico
- Informações do sistema hospedeiro

## Como executar

Na raiz do repositório:

```bash
python editions/compact/peanut_os_compact.py
```

No Windows, também funciona com:

```powershell
py editions/compact/peanut_os_compact.py
```

## Requisitos

- Python 3.10 ou superior
- Nenhuma dependência externa obrigatória

## Limitações

- A bateria é simulada.
- O sistema não altera configurações reais do computador.
- Não possui kernel próprio, drivers, área de trabalho real ou aplicativos avançados.
- Não é uma build estável; é apenas uma prova de conceito.

## Próximos passos planejados

- Criar tela de bloqueio textual
- Adicionar usuário e senha simulados
- Adicionar configurações básicas
- Melhorar o recovery
- Criar mini aplicativos de terminal
- Adicionar temas de texto
