# Peanut OS Compact

O **Peanut OS Compact** é a edição de terminal do projeto: um **sistema operacional simulado em Python**, com sensação de `.bat`, menu textual, boot, status do sistema, notificações internas e memória armazenada.

Ele não tenta substituir Windows, Linux, Android ou macOS. A ideia é criar uma experiência própria, leve e educacional, como se o usuário estivesse ligando um mini sistema dentro do terminal.

## Versão atual

**v0.2.0 Concept**

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

## Conceito

O Compact funciona como uma interface de sistema por texto:

```text
Peanut OS Compact - v0.2.0 Concept

Usuario: Usuario Compact
Bateria: 30%
Hora: 14:30
Estado do sistema: desligado
Notificacoes nao lidas: 1

[1] Ligar
[2] Entrar em modo recovery
[3] Sair
```

Quando o usuário escolhe **Ligar**, o sistema muda de estado e abre o menu principal. Quando escolhe **Recovery**, entra em um ambiente separado de recuperação, diagnóstico e opções de segurança.

## Incluído na v0.2.0 Concept

- Tela inicial com bateria simulada, hora atual, usuário, estado e notificações não lidas
- Boot textual básico
- Menu inicial
- Menu principal após ligar
- Modo recovery
- Diagnóstico básico
- Reiniciar e desligar simulados
- Sistema de notificações internas
- Central de notificações
- Marcar notificações como lidas
- Criar notificação de teste
- Limpar notificações
- Memória armazenada em `peanut_memory.json`
- Nome de usuário salvo
- Contador de boots
- Histórico simples de eventos
- Reset de memória pelo recovery
- Nenhuma dependência externa obrigatória

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

Esse arquivo é local e não deve ser tratado como banco de dados real.

## Objetivos

- Simular boot, desligamento, reinicialização e estados do sistema
- Ter visual de terminal parecido com `.bat`, mas usando Python
- Mostrar informações como hora, bateria, estado e mensagens do sistema
- Adicionar recursos básicos de OS simulado, como notificações e memória
- Servir como primeira base jogável/testável do Peanut OS
- Rodar em computadores simples e também no Termux/Pydroid, quando possível
- Manter o código simples para aprendizado e evolução

## Estados

- `desligado`
- `ligando`
- `ligado`
- `recovery`
- `reiniciando`
- `encerrando`

## Ideia de fluxo

```text
Estado: desligado

1. Ligar
2. Recovery
3. Sair

Ao ligar:
- mostra animação textual de boot
- lê memória armazenada
- prepara notificações
- muda estado para ligado
- entra no menu principal

No sistema ligado:
- ver informações
- abrir central de notificações
- abrir memória armazenada
- reiniciar
- entrar no recovery
- desligar

No recovery:
- mostra diagnóstico simples
- limpa notificações
- reseta memória
- permite voltar, reiniciar ou sair
```

## Fora do escopo inicial

- Kernel próprio
- Drivers próprios
- Particionamento real
- Alteração real do sistema instalado
- Substituição real do sistema operacional do computador
- Compatibilidade completa com aplicativos de Windows, Linux ou Android
- Notificações reais do sistema hospedeiro

## Requisitos

- Python 3.10+

Dependências opcionais futuras: `colorama`, `rich` e `pyfiglet`. A versão atual roda apenas com Python puro.

## Notas da versão

- [`v0.1.0 Concept`](../../docs/releases/compact-v0.1.0-concept.md)
- [`v0.2.0 Concept`](../../docs/releases/compact-v0.2.0-concept.md)

## Estado

Prova de conceito em evolução. O Compact será tratado como a edição **terminal/simulador de OS em Python**, não apenas como uma versão leve comum.
