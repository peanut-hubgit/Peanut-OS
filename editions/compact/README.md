# Peanut OS Compact

O **Peanut OS Compact** é a edição de terminal do projeto: um **sistema operacional simulado em Python**, com sensação de `.bat`, menu textual, boot, status do sistema e comandos simples.

Ele não tenta substituir Windows, Linux, Android ou macOS. A ideia é criar uma experiência própria, leve e educacional, como se o usuário estivesse ligando um mini sistema dentro do terminal.

## Conceito

O Compact deve funcionar como uma interface de sistema por texto:

```text
Peanut OS Compact

Bateria: 30%
Hora: 14:30
Estado do sistema: desligado

[1] Ligar
[2] Entrar em modo recovery
[3] Sair
```

Quando o usuário escolhe **Ligar**, o sistema muda de estado e abre o menu principal. Quando escolhe **Recovery**, entra em um ambiente separado de recuperação, diagnóstico e opções de segurança.

## Objetivos

- Simular boot, desligamento, reinicialização e estados do sistema
- Ter visual de terminal parecido com `.bat`, mas usando Python
- Mostrar informações como hora, bateria, estado e mensagens do sistema
- Servir como primeira base jogável/testável do Peanut OS
- Rodar em computadores simples e também no Termux/Pydroid, quando possível
- Manter o código simples para aprendizado e evolução

## Estados planejados

- `desligado`
- `ligando`
- `ligado`
- `recovery`
- `reiniciando`
- `encerrando`

## Escopo inicial

- Tela inicial com bateria, hora e estado do sistema
- Menu de boot
- Opção de ligar o sistema
- Modo recovery
- Menu principal após ligar
- Relógio e informações básicas
- Configurações simples
- Notas simples
- Calculadora simples
- Simulação de desligar e reiniciar

## Ideia de fluxo

```text
Estado: desligado

1. Ligar
2. Recovery
3. Sair

Ao ligar:
- mostra animação textual de boot
- muda estado para ligado
- entra no menu principal

No recovery:
- mostra diagnóstico simples
- permite voltar, reiniciar ou sair
```

## Fora do escopo inicial

- Kernel próprio
- Drivers próprios
- Particionamento real
- Alteração real do sistema instalado
- Substituição real do sistema operacional do computador
- Compatibilidade completa com aplicativos de Windows, Linux ou Android

## Requisitos planejados

- Python 3.10+
- Dependências opcionais: `colorama`, `rich` e `pyfiglet`

A primeira versão deve conseguir rodar apenas com Python puro. As dependências opcionais entram apenas para melhorar aparência.

## Estado

Planejamento corrigido. O Compact será tratado como a edição **terminal/simulador de OS em Python**, não apenas como uma versão leve comum.