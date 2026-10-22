---
name: kit-identidade-visual
description: Cria ou completa um kit de identidade visual num padrão de entrega fixo (logo, cores, tipografia, redes, aplicações ou papelaria, guia, index, QA e ZIP). Use quando pedirem uma identidade visual, logo ou marca para pessoa, produto ou evento, ou as peças que faltam num kit existente.
---

# Kit de identidade visual

O padrão de entrega está em [PADRAO-DE-ENTREGA.md](PADRAO-DE-ENTREGA.md): a lista de pastas, peças, tamanhos e regras de conteúdo. As peças com imagem (mockups realistas, fotos de aplicação) usam a skill `higgsfield-brandkit`.

## Regras fixas

- **Fatos:** só o que o dono confirmou (nome e grafia, domínio, contatos, datas). Nada de e-mail, telefone, @, preço, cliente ou depoimento inventado; o que falta vira campo a preencher no README.
- **Logo aprovado é a fonte de verdade:** reaproveite os vetores e converta texto em curvas por script; nunca redesenhe nem redigite o lettering.
- **Rosto aprovado não muda:** retratos e caricaturas aprovados não são editados por IA depois.
- **Imagem gerada por IA:** sem texto nem logo dentro; o logo entra depois, por composição.
- **pt-BR** com acentos corretos, grafia do nome idêntica em todo o kit.

## Passos

1. **Briefing.** Escreva `BRIEF-KIT.md` com os fatos confirmados, o público, o tom e o que entra no kit. Termina quando o dono confirmou o briefing.
2. **Exploração.** Gere 3 ou 4 direções bem diferentes em pranchas, em `_exploracao/`. O dono escolhe. Termina com a escolha registrada em "Decisões de <dono>" no README.
3. **Logo e sistema.** Vetorize o logo escolhido e feche paleta (com contraste WCAG) e fontes (OFL, arquivos em `_fontes/`). Termina quando o dono aprovou logo, paleta e fontes.
4. **Kit.** Escreva um gerador determinístico em `scripts/` que lê só arquivos locais do kit e produz todas as peças do padrão. Marcas de evento trocam redes e aplicações de marca por papelaria (convite, save the date, cardápio, número de mesa, tags); logo, cores, tipografia, guia, manifesto e QA continuam obrigatórios.
5. **Índice.** Copie [gerar-index.py](gerar-index.py) para `scripts/gerar-index.py`, crie `scripts/index.json` a partir de [index.exemplo.json](index.exemplo.json) (nome, domínio, descrição, cores e fontes) e chame o script no fim do gerador.
6. **QA e entrega.** `scripts/verificar-kit.py` gera `qa-report.json`, `manifest.json` (SHA-256) e `_dist/<nome>-identidade.zip`. Monte folhas de contato em `_revisao/` e olhe cada página do guia. Termina quando o QA tem zero erros, todo item **[todas]** do padrão existe e a revisão visual não achou defeito.
7. **Versão.** Kit em git, repositório privado; `_dist/`, `.venv/` e a exploração pesada ficam fora.

## Gerando com o Codex

Para delegar a geração ao Codex CLI (que também lê `.agents/skills/`):

```bash
codex exec -s workspace-write --skip-git-repo-check -C <pasta-do-kit> -i referencia.png - < BRIEF-KIT.md &
pid=$!; while kill -0 $pid 2>/dev/null; do sleep 30; done
```

Espere pelo PID. `pgrep -f "codex exec"` casa com o próprio comando de espera e nunca termina.
