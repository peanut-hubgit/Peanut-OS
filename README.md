# Peanut OS

O **Peanut OS** é um projeto educacional de interface e ambiente de sistema desenvolvido em Python. O repositório passa a reunir três edições com objetivos diferentes, compartilhando a mesma identidade e princípios de desenvolvimento.

> **Estado do projeto:** em desenvolvimento. Ainda não existe uma versão estável recomendada para uso como sistema operacional principal.

## Edições

### Peanut OS Compact

Edição leve, simples e econômica, pensada para terminais, computadores modestos, testes rápidos e aprendizado.

- Inicialização rápida
- Baixo consumo de memória
- Interface baseada em terminal
- Aplicativos essenciais
- Compatibilidade com Python 3.10 ou superior

Diretório: [`editions/compact`](editions/compact)

### Peanut OS Touch Interface

Edição experimental voltada a telas sensíveis ao toque, tablets, painéis e dispositivos com interação por gestos.

- Botões e áreas de toque maiores
- Navegação por gestos
- Teclado virtual planejado
- Central de controle adaptada para toque
- Interface responsiva

Diretório: [`editions/touch-interface`](editions/touch-interface)

### Peanut OS Desktop

Edição principal para computadores, com ambiente gráfico, janelas, barra de tarefas, central de controle e aplicativos integrados.

- Área de trabalho
- Sistema de janelas
- Menu de aplicativos
- Configurações e personalização
- Arquitetura modular

Diretório: [`editions/desktop`](editions/desktop)

## Estrutura planejada

```text
Peanut-OS/
├── editions/
│   ├── compact/
│   ├── touch-interface/
│   └── desktop/
├── shared/
├── docs/
├── LICENSE.md
└── README.md
```

A pasta `shared` será usada para componentes reutilizáveis, temas, utilitários e recursos comuns às três edições.

## Princípios do projeto

- Código compreensível e educacional
- Interface própria, sem copiar outros sistemas
- Sem promessas falsas de substituir Windows, Linux, Android ou macOS
- Segurança e transparência nas funções executadas
- Compatibilidade gradual com diferentes dispositivos
- Desenvolvimento aberto à comunidade

## Requisitos gerais

- Python 3.10 ou superior
- Git, para desenvolvimento e contribuição

Dependências opcionais ou específicas serão documentadas dentro de cada edição. Entre as bibliotecas em avaliação estão `rich`, `colorama`, `pyfiglet` e frameworks gráficos adequados para desktop e toque.

## Instalação do Python

### Windows

```powershell
winget install Python.Python.3
```

### macOS

Com Homebrew instalado:

```bash
brew install python
```

### Termux

```bash
pkg update && pkg upgrade -y
pkg install python -y
```

## Roadmap inicial

- [ ] Organizar o código antigo dentro da edição Compact
- [ ] Criar a base compartilhada entre as edições
- [ ] Definir o framework gráfico da edição Desktop
- [ ] Criar protótipo touch-first
- [ ] Adicionar documentação de arquitetura
- [ ] Adicionar testes básicos
- [ ] Publicar versões somente quando houver builds verificadas

## Releases

As releases antigas deixam de representar o estado atual do projeto. Durante esta reorganização, o código deve ser usado diretamente a partir do repositório. Uma nova release só deverá ser publicada quando uma edição tiver instalação, documentação e testes mínimos.

## Licença

O código original do Peanut OS é distribuído sob a **GNU General Public License v3.0 ou posterior — GPL-3.0-or-later**. Consulte [`LICENSE.md`](LICENSE.md).

Dependências, fontes, ícones, imagens e outros componentes de terceiros continuam sujeitos às licenças de seus respectivos autores. Consulte também [`docs/LICENSING.md`](docs/LICENSING.md).

## Créditos

Projeto criado e mantido por **@Peanut**.

## Comunidade

- Discord oficial: [Peanut OS](https://discord.gg/wrSMwXHw)

Contribuições devem explicar claramente o que foi alterado e não podem incluir código malicioso, coleta escondida de dados ou componentes sem licença compatível.
