# Peanut OS Compact v0.2.0 Concept

Primeira evolução do Peanut OS Compact após o conceito inicial. Esta versão mantém o estilo de mini OS em terminal, mas adiciona persistência simples e uma central de notificações.

## Novidades

- Sistema de notificações internas
- Contador de notificações não lidas no cabeçalho
- Central de notificações no menu principal
- Opção de marcar notificações como lidas
- Opção de criar notificação de teste
- Opção de limpar notificações
- Memória armazenada em arquivo local `peanut_memory.json`
- Salvamento de nome do usuário
- Salvamento de bateria simulada
- Registro de quantidade de boots
- Histórico simples de eventos do sistema
- Menu próprio de memória armazenada
- Recovery com opção de limpar notificações e resetar memória

## Arquivo principal

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

## Arquivo gerado ao executar

```text
editions/compact/peanut_memory.json
```

Esse arquivo guarda dados locais da simulação. Ele não é obrigatório para baixar o projeto, pois será recriado automaticamente se não existir.

## Limitações

- Ainda é uma simulação educacional em terminal
- Não substitui um sistema operacional real
- A bateria é simulada
- A memória armazenada é um JSON local simples
- As notificações são internas do Peanut Compact, não notificações reais do Windows/Linux/macOS

## Status

Versão conceitual básica, pronta para testes manuais.
