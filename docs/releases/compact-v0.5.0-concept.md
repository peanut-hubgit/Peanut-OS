# Peanut OS Compact v0.5.0 Concept

A v0.5.0 expande o Compact com recursos mais próximos de um mini sistema em terminal: navegador textual real, bateria dinâmica, carregamento, limite de armazenamento e tela de boas-vindas.

## Destaques

- Navegador interno textual e funcional, sem interface gráfica
- Abertura de URLs reais via Python puro
- Leitura básica de título, texto e links da página
- Histórico do navegador salvo na memória local
- Melhorias nos banners e nas cores do terminal
- Bateria que cai com o tempo quando não está carregando
- Modo de carregamento que recupera bateria com o tempo
- Limite de armazenamento simulado de 1 GB de ROM
- Uso de ROM exibido no cabeçalho
- Loja Beta e notas consumindo armazenamento simulado
- Tela de boas-vindas no primeiro uso
- Escolha inicial de nome de usuário
- Escolha inicial de cor principal
- Escolha inicial do modo de energia

## Navegador interno

O navegador é textual e real: ele tenta acessar uma URL usando a biblioteca padrão do Python, extrai título, texto básico e alguns links.

Exemplo:

```text
https://example.com
```

Limitações:

- Não executa JavaScript
- Não renderiza CSS
- Não mostra imagens
- Não substitui um navegador completo
- Algumas páginas modernas podem bloquear ou retornar pouco texto

## Bateria dinâmica

A bateria agora é atualizada com base no tempo salvo em `peanut_memory.json`.

- Sem carregamento: a bateria cai aos poucos
- Com carregamento: a bateria sobe aos poucos
- Com bateria zerada, o boot normal é bloqueado até ativar carregamento

## Armazenamento

O Compact agora simula uma ROM de:

```text
1024 MB
```

O sistema mostra no cabeçalho:

```text
ROM: 64/1024 MB
```

Algumas ações simulam uso de armazenamento, como histórico do navegador, notas e apps da Loja Beta.

## Primeiro uso

Ao iniciar pela primeira vez, o usuário configura:

- nome de usuário
- cor principal
- modo inicial de energia

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
