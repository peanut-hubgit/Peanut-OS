# Peanut OS Compact v0.5.5 Concept

A v0.5.5 melhora fortemente o Navegador Compact para tornar a experiencia mais proxima de navegar dentro de uma interface textual estilo CMD.

## Destaques

- Navegador Compact atualizado para v0.5.5
- Abertura de URLs reais usando Python puro
- Leitura de paginas HTML
- Extracao de titulo, texto, links, imagens e videos detectados
- Links clicaveis por numero
- Interface touch simulada dentro do terminal
- Visualizador textual de fotos detectadas
- Visualizador textual de videos detectados
- Historico do navegador
- Favoritos do navegador
- Pagina local demo multimidia
- Comando `browser limpar`
- Ajuda interna do navegador

## Importante

O Navegador Compact continua sendo um navegador de terminal. Ele nao renderiza paginas como Chrome, Firefox ou Edge, nao executa JavaScript e nao reproduz video real dentro do CMD/Termux.

O objetivo desta versao e permitir navegacao textual interativa:

```text
abrir pagina -> ler conteudo -> clicar links -> ver midias detectadas -> navegar novamente
```

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
