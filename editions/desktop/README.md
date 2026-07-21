# Peanut OS Desktop

O **Peanut OS Desktop** é a edição principal para computadores, com ambiente gráfico próprio e arquitetura modular.

## Objetivos

- Criar uma experiência de desktop coerente
- Separar interface, aplicativos e serviços internos
- Permitir personalização sem comprometer estabilidade
- Reaproveitar componentes compartilhados entre edições
- Manter o projeto compreensível para estudantes e colaboradores

## Recursos planejados

- Área de trabalho
- Barra de tarefas
- Menu de aplicativos
- Sistema de janelas
- Central de controle
- Tela de bloqueio
- Aplicativo de configurações
- Calculadora, notas e explorador experimental
- Temas, cores e papéis de parede
- Suporte básico a múltiplos idiomas

## Arquitetura planejada

```text
src/
├── shell/
├── apps/
├── services/
├── ui/
└── assets/
```

Os módulos compartilhados deverão ficar na pasta `shared` da raiz do repositório.

## Segurança

A edição Desktop não deverá executar comandos administrativos escondidos, coletar dados sem consentimento ou alterar o sistema hospedeiro sem informar claramente o usuário.

## Estado

Fase de planejamento e definição de arquitetura. Ainda não há build estável.
