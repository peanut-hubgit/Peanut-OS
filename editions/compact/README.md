# Peanut OS Compact

O **Peanut OS Compact** é a edição de terminal do projeto: um **sistema operacional simulado em Python**, com sensação de `.bat`, menu textual, Bootloader, Secure Boot simulado, Custom Mods próprios, notificações internas, memória armazenada, apps internos, navegador textual real e aba de comandos.

Ele não tenta substituir Windows, Linux, Android ou macOS. A ideia é criar uma experiência própria, leve e educacional, como se o usuário estivesse ligando um mini sistema dentro do terminal.

## Versão atual

**v0.5.0 Concept**

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

A v0.5.0 começa com uma tela de boas-vindas no primeiro uso e depois entra pelo Bootloader:

```text
Peanut OS Compact - v0.5.0 Concept

Usuario: Peanut | Hora: 14:30 | Estado: bootloader
Bateria: 74% ███░ | ROM: 64/1024 MB (6%)
Secure Boot: LOCKED | Custom Mods: OFF | Destruction: NAO

BOOTLOADER COMPACT

[1] Boot normal
[2] Desbloquear Secure Boot
[3] Custom Mods
[4] Recovery
[5] Auto Destruction
[6] Comandos
[7] Carregamento
[8] Sair
```

## Incluído na v0.5.0 Concept

- Tela de boas-vindas no primeiro uso
- Escolha de nome de usuário
- Escolha de cor principal
- Escolha de modo inicial de energia
- Navegador interno textual e funcional
- Abertura de URLs reais usando Python puro
- Extração básica de título, texto e links de páginas HTML
- Histórico do navegador salvo localmente
- Bateria dinâmica que cai com o tempo
- Modo de carregamento que recupera bateria com o tempo
- Bloqueio de boot normal quando a bateria está zerada e não está carregando
- Limite de armazenamento simulado de 1 GB de ROM
- Uso de ROM exibido no cabeçalho
- Consumo simulado de armazenamento por notas, histórico do navegador e apps da Loja Beta
- Melhorias nos banners e nas cores do terminal
- App Navegador adicionado ao menu de apps
- Comandos `carregar on` e `carregar off`

## Navegador interno

O navegador interno é real no sentido de que tenta acessar URLs pela internet usando a biblioteca padrão do Python.

Ele consegue:

- abrir URLs `http://` e `https://`
- mostrar título da página
- mostrar texto básico extraído do HTML
- listar alguns links encontrados
- salvar histórico local

Limitações:

- não renderiza interface gráfica
- não executa JavaScript
- não renderiza CSS
- não mostra imagens
- algumas páginas modernas podem bloquear ou retornar pouco conteúdo

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
13. Navegador

## Aba Comandos

Comandos disponíveis:

```text
/help
Reparo Fix
status
apps update
notificacoes limpar
memoria reset
carregar on
carregar off
sair
```

O comando mais importante continua sendo:

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

- primeiro uso concluído
- nome do usuário
- cor principal
- bateria e modo de carregamento
- limite e uso de ROM simulada
- último estado salvo
- quantidade de boots
- notificações
- histórico básico de eventos
- estado do Secure Boot
- Custom Mods ativados
- módulos habilitados
- estado do Auto Destruction
- apps instalados pela Loja Beta
- histórico do navegador
- notas

Esse arquivo é local e não deve ser tratado como banco de dados real.

## Objetivos

- Simular boot, desligamento, reinicialização e estados do sistema
- Ter visual de terminal parecido com `.bat`, mas usando Python
- Criar uma experiência de Bootloader própria
- Permitir mods locais controlados dentro da simulação
- Mostrar informações como hora, bateria, estado e mensagens do sistema
- Adicionar apps internos simples e úteis
- Ter um navegador textual funcional para testes reais
- Simular bateria, carregamento e limite de armazenamento
- Servir como primeira base jogável/testável do Peanut OS
- Rodar em computadores simples e também no Termux/Pydroid, quando possível
- Manter o código simples para aprendizado e evolução

## Roadmap

- [ ] Melhorar estabilidade da memória local
- [ ] Melhorar o navegador textual com histórico clicável
- [ ] Criar favoritos do navegador
- [ ] Criar mais apps internos
- [ ] Melhorar Loja de Apps Beta
- [ ] Criar sistema de atualização de módulos
- [ ] Melhorar os minigames do Bootloader
- [ ] Criar documentação para desenvolvedores de módulos
- [ ] Lançar a **v1.0 estável** com pelo menos **30 funcionalidades reais de apps/sistema**

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
- [`v0.5.0 Concept`](../../docs/releases/compact-v0.5.0-concept.md)
