# Peanut OS Compact

O **Peanut OS Compact** é a edição de terminal do projeto: um sistema operacional simulado em Python, com sensação de `.bat`/CMD, Bootloader, comandos, apps internos, memória local e navegador textual interativo.

Ele não tenta substituir Windows, Linux, Android ou macOS. A ideia é criar uma experiência própria, leve e educacional, como se o usuário estivesse ligando um mini sistema dentro do terminal.

## Versão atual

**v0.5.5 Concept**

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

Para atualizar no Termux:

```bash
cd Peanut-OS
git pull
python editions/compact/peanut_os_compact.py
```

## Conceito atual

A v0.5.5 mantém o Bootloader e melhora o **Navegador Compact** para navegar por páginas usando uma interface textual parecida com CMD:

```text
NAVEGADOR COMPACT v0.5.5

[1] Abrir URL
[2] Favoritos
[3] Historico
[4] Pagina demo multimidia
[5] Alternar modo touch
[6] Ajuda do navegador
[0] Voltar
```

Dentro de uma página, o navegador mostra texto extraído, links, fotos e vídeos detectados. A navegação acontece por números grandes, simulando clique/touch dentro do terminal.

## Incluído na v0.5.5 Concept

- Navegador Compact melhorado
- Abertura de URLs reais usando Python puro
- Leitura de páginas HTML
- Extração de título e texto
- Links clicáveis por número
- Detecção de imagens por tags HTML
- Detecção de vídeos e players incorporados
- Visualizador textual de fotos detectadas
- Visualizador textual de vídeos detectados
- Favoritos do navegador
- Histórico do navegador
- Página demo multimídia local
- Modo touch simulado no navegador
- Comando `browser limpar`
- Ajuda interna do navegador

## Limitações do navegador

O navegador do Peanut OS Compact é propositalmente textual. Ele **não renderiza imagem real dentro do CMD/Termux**, não executa JavaScript, não toca vídeo real e não interpreta CSS como navegadores gráficos.

Ele suporta navegação textual:

```text
abrir página -> ler conteúdo -> clicar links -> detectar fotos/vídeos -> navegar de novo
```

Sites modernos podem bloquear navegadores simples ou retornar pouco conteúdo.

## Apps internos

1. Navegador Compact
2. Configurações
3. Loja de Apps Beta
4. Notificações
5. Memória
6. Informações
7. Calculadora
8. Notas
9. Relógio
10. Arquivos
11. Segurança
12. Temas
13. Comandos

## Comandos disponíveis

```text
/help
Reparo Fix
status
apps update
notificacoes limpar
memoria reset
browser limpar
sair
```

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

Esse arquivo guarda dados simples da simulação, como nome do usuário, bateria, notificações, histórico, notas, favoritos, histórico do navegador, mods ativados e estado do Bootloader.

## Roadmap

- [ ] Melhorar estabilidade da memória local
- [ ] Melhorar o navegador textual para suportar mais tipos de página
- [ ] Criar favoritos com categorias
- [ ] Melhorar Loja de Apps Beta
- [ ] Criar sistema de atualização de módulos
- [ ] Criar documentação para desenvolvedores de módulos
- [ ] Lançar a **v1.0 estável** com pelo menos **30 funcionalidades reais de apps/sistema**

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
- [`v0.5.5 Concept`](../../docs/releases/compact-v0.5.5-concept.md)
