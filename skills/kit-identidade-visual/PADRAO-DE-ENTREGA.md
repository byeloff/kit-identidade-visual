# Padrão de entrega das identidades visuais

Todo kit fica numa pasta `<nome>-identidade/` e sai com a estrutura abaixo. Quando este documento não detalhar uma peça, siga o kit mais completo que você já tiver neste padrão (dimensões, nomes de arquivo, nível de acabamento, README, guia, QA).

Legenda: **[todas]** obrigatório em toda marca · **[produto]** marcas de produto digital · **[pessoal]** marca pessoal.

## Logo — `logo/`

- `horizontal/`, `vertical/`, `wordmark/`, `simbolo/` **[todas]**: `escuro.svg`, `claro.svg`, `mono.svg`, `mono-branco.svg`, `current-color.svg` (mais as versões de cor da marca que já existirem). Curvas reais, fundo transparente, sem fonte externa.
- `png/` **[todas]**: cada SVG acima em 1x e 4x, transparente.
- `area-protecao.svg/.png` e `reducao-minima.svg/.png` **[todas]**: respiro em unidades do próprio logo e menor tamanho em px e mm, impresso e digital.
- `simbolo/construcao.svg/.png` **[todas]**: geometria do símbolo.
- `grafismo/` **[todas]**: o grafismo próprio da marca (padrão, assinatura, etiqueta, emblema), em SVG e PNG, nas cores da marca e em mono.

## Ícone e favicon

- `icone-app/` **[todas]**: `claro`, `escuro`, `maskable` e as variantes de cor da marca, em SVG e PNG 192, 512 e 1024. Nome de arquivo `<variante>-<tamanho>.png`.
- `favicon/` **[todas]**: `favicon.svg`, `favicon.ico` (16/32/48), PNG 16/32/48/64, `apple-touch-icon.png` (180), `icon-192.png`, `icon-512.png`, `icon-maskable-512.png`, `site.webmanifest` e `integracao.html` com o snippet de `<head>`.

## Cores e tipografia

- `cores/` **[todas]**: `paleta.svg/.png`, `tokens.css`, `tokens.json`, `tailwind.css` (bloco `@theme` do Tailwind 4) e `contraste.json` (matriz WCAG de todas as combinações de texto usadas, com AA/AAA).
- `tipografia/` **[todas]**: `especime.svg/.png` e `fontes.css` (`@font-face` apontando para `_fontes/`).
- `_fontes/` **[todas]**: os arquivos das fontes usadas, com a licença (OFL) ao lado.

## Redes sociais

- `social/` **[todas]**: `avatar` 400×400, `og-image` 1200×630, `capa-apresentacao` 1080×1080, `post-instagram` 1080×1350, `story-instagram` 1080×1920. SVG e PNG.
- `instagram-avatar/` **[todas]**: 3 a 4 variações de avatar (fundos e versões do símbolo), PNG 1080×1080, com README dizendo qual é a principal.
- `linkedin/` **[todas]**: capa 1584×396 e @2x, foto/logo 400×400 e @2x, prévia no perfil. Em `linkedin/facebook/`: capa 1640×624 e @2x, perfil 720×720 e prévia desktop/celular. As fontes HTML/CSS e o `render.mjs` ficam em `linkedin/fonte/`. Marca de produto usa a capa de **página de empresa**.
- `wallpapers/` **[todas]**: desktop 4K (3840×2160), MacBook (3024×1964) e celular (1290×2796), cada um em versões: principal, só símbolo, só grafismo e com grafismos. Fontes em `wallpapers/fonte/`.

## Aplicações — `aplicacoes/`

- **[todas]**: cartão de visita frente e verso (tela) + versões de impressão 90×50 mm com 3 mm de sangria + `cartao-impressao.pdf` de duas páginas; `cabecalho-email`; `assinatura-email.html/.svg/.png`; `wallpaper` 2560×1440; `poster` A3 (SVG, PNG e PDF); `hero-desktop-1440` (1440×900) e `hero-mobile-390` (390×844) como proposta de primeira dobra do site.
- **[produto]**: capa de proposta/apresentação comercial (SVG, PNG, PDF), telas do produto (login, painel principal) e splash, se for app.
- **[pessoal]**: capa de proposta de consultoria, retrato tratado.

## Guia — `guia/`

`guia-de-marca.html` autossuficiente (offline, sem recursos externos), `guia-de-marca.pdf` e `paginas/NN.svg`, com 12 a 14 páginas: capa · conceito · logotipo e versões · construção e área de proteção · redução mínima · símbolo e ícone · cores · contraste · tipografia · grafismo · redes sociais · aplicações · usos incorretos · voz e contato.

## Entrega

- `identidade-visual.png/.svg` **[todas]**: prancha-resumo.
- `index.html` **[todas]**: página de navegação do kit, igual em todas as marcas. Nunca escreva à mão: copie o `gerar-index.py` desta skill para `scripts/gerar-index.py`, crie `scripts/index.json` a partir do `index.exemplo.json` (nome, domínio, descrição, cores e fontes) e chame o script no fim do gerador do kit.
- `README.md` **[todas]**: estrutura em tabela, regras fixas (cores, fontes, grafia do nome), produção/impressão, como regenerar e "Decisões de <dono>" com o que aguarda aprovação.
- `BRIEF-KIT.md` **[todas]**: o briefing que gerou o kit.
- `manifest.json` (inventário com SHA-256) e `qa-report.json` (arquivos, dimensões, SVGs em curvas e sem recursos externos, contraste, grafia do nome, erros e avisos) **[todas]**.
- `scripts/` **[todas]**: gerador determinístico + `verificar-kit.py` (gera o QA e o ZIP) + `requirements.txt`. O gerador lê só arquivos locais do kit.
- `_referencia/` **[todas]**: as imagens aprovadas, preservadas byte a byte.
- `_revisao/` **[todas]**: contatos das páginas do guia, comparações e conferências visuais.
- `_dist/<nome>-identidade.zip` **[todas]**: sem `_dist/`, `_exploracao/`, `_descartado/`, `.git/`, `.venv/`.
- Histórico em `_exploracao/` ou `_descartado/`, preservado e fora do ZIP. Kit versionado em git.

## Regras de conteúdo

- O logo aprovado é a fonte de verdade: reutilize os vetores existentes, nunca redesenhe nem redigite o lettering.
- Paleta e fontes aprovadas não mudam.
- Só use fatos confirmados (nome, domínio, descrição, contatos listados no briefing). Nada de e-mail, telefone, @, preço, cliente, número ou depoimento inventado; dados de telas são exemplos e o README diz isso.
- Textos em pt-BR com acentos corretos; grafia do nome idêntica em todo o kit.
- Peças vetoriais/determinísticas; foto gerada por IA só quando o briefing pedir, sem texto nem logo na imagem.
