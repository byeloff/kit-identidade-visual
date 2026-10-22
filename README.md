# kit-identidade-visual

Skill de agente (Claude Code, Codex e outros que leem `SKILL.md`) para criar ou completar um kit de identidade visual completo: logo em todas as versões, cores com contraste WCAG, tipografia, ícones e favicon, redes sociais, aplicações (ou papelaria, para eventos), guia de marca em HTML e PDF, índice navegável, QA e ZIP de entrega.

O agente segue um processo com aprovação do dono em cada etapa (briefing, exploração, logo e sistema) e um padrão de entrega fixo, com pastas, peças, tamanhos e regras de conteúdo definidos.

## Instalar

Com o [skills CLI](https://github.com/vercel-labs/skills):

```sh
# neste projeto (Claude Code e Codex)
npx skills add byeloff/kit-identidade-visual -a claude-code -a codex

# para o seu usuário, valendo em qualquer pasta
npx skills add byeloff/kit-identidade-visual -g -a claude-code -a codex
```

Ou à mão: copie `skills/kit-identidade-visual/` para `.claude/skills/` (Claude Code) ou `.agents/skills/` (Codex), no projeto ou na sua pasta de usuário.

As peças com imagem (mockups realistas, fotos de aplicação) usam a skill `higgsfield-brandkit`, que precisa de conta na Higgsfield:

```sh
npx skills add higgsfield-ai/skills --skill higgsfield-brandkit -a claude-code -a codex
```

Sem ela, o kit sai completo nas peças vetoriais e sem as fotos.

## Usar

Peça ao agente uma identidade visual, um logo ou uma marca para uma pessoa, um produto ou um evento, ou peça as peças que faltam num kit existente. Por exemplo:

> Cria a identidade visual da Padaria Aurora: padaria de bairro em Campinas, público de famílias, tom acolhedor. O único contato confirmado é o Instagram @padariaaurora.

O agente escreve o `BRIEF-KIT.md`, mostra 3 ou 4 direções para você escolher, fecha logo, paleta e fontes com a sua aprovação e só então gera o kit.

## O que tem aqui

| Arquivo | Para quê |
|---|---|
| `skills/kit-identidade-visual/SKILL.md` | Regras fixas e os passos do processo |
| `skills/kit-identidade-visual/PADRAO-DE-ENTREGA.md` | Lista de pastas, peças, tamanhos e regras de conteúdo do kit |
| `skills/kit-identidade-visual/gerar-index.py` | Gera o `index.html` navegável do kit (igual em todas as marcas) |
| `skills/kit-identidade-visual/index.exemplo.json` | Modelo do `scripts/index.json` que o gerador lê |

O `gerar-index.py` precisa de Python 3 com Pillow e do `rsvg-convert` (`brew install librsvg` no macOS).

## Licença

MIT. Veja [LICENSE](LICENSE).
