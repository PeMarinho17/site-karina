# Site Karina Coutinho — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Site de uma página com galeria por categoria, serviços e orçamento pelo WhatsApp para a fotógrafa Karina Coutinho (@fractalume).

**Architecture:** HTML/CSS/JS estático, sem build. Um script Python (`tools/preparar_fotos.py`) gera as fotos WebP e o `assets/fotos.json` que a galeria lê. Fotos de origem: imagens do PDF + prévias JPEG embutidas nos CR3 do cartão SD.

**Tech Stack:** HTML, CSS, JS vanilla; Python 3 + Pillow + PyMuPDF só para preparar fotos (venv fora do site); Google Fonts.

**Spec:** `docs/superpowers/specs/2026-11-25-site-karina-design.md`

## Global Constraints
- WhatsApp: `5567992379876`; e-mail `karina.coutinho@ufms.br`; local "Campo Grande/MS"; Instagram `@fractalume`.
- Categorias da galeria: `ensaios`, `eventos`, `casamentos`. Serviços: Ensaios, Eventos, Casamentos, Still de set / making-of. Nada de publicidade.
- Paleta: papel `#ecebe8`, tinta `#1d1b19`, tijolo `#9b2c1f`. Serifa alta condensada + monoespaçada de máquina de escrever.
- Fotos: WebP, lado maior 1600 px (grande) e 600 px (miniatura), rotação EXIF aplicada.
- Funciona em 375 px de largura sem rolagem horizontal.

## Review Focus
- Foto do CR3 deitada (orientação só no EXIF/CR3) → precisa aparecer em pé. Teste em Task 1.
- Link do WhatsApp com acento/espaço na mensagem → precisa estar codificado (`encodeURIComponent`). Verificado em Task 3.
- Lightbox aberto no celular → fecha com toque fora/Esc e navega com setas/swipe. Verificado em Task 4.
- Galeria com muitas fotos → miniaturas com `loading="lazy"` e `width/height`, sem pulo de layout. Verificado em Task 4.
- JS falhando ou desativado → contato e serviços continuam visíveis (são HTML estático). Verificado em Task 4.

---

### Task 1: Preparação das fotos

**Files:**
- Create: `tools/preparar_fotos.py`, `tools/selecao.json`, `tests/test_preparar_fotos.py`
- Gera: `assets/fotos/{grande,mini}/*.webp`, `assets/fotos.json`

**Interfaces:**
- Produces: `assets/fotos.json` = `[{"id": str, "categoria": "ensaios"|"eventos"|"casamentos"|"capa", "grande": str, "mini": str, "w": int, "h": int}]`
- `extrair_prvw(caminho_cr3: str) -> PIL.Image` (prévia JPEG + orientação do CR3 aplicada); `exportar(img, id) -> dict`.

- [ ] Teste: `exportar` de imagem 4000×3000 gera grande com lado maior 1600 e mini 600; `extrair_prvw` de uma foto vertical conhecida retorna `h > w`.
- [ ] Rodar `python -m pytest tests -q` → falha.
- [ ] Implementar; `selecao.json` lista por categoria os arquivos escolhidos (PDF páginas + nomes CR3).
- [ ] Rodar testes → passa; rodar script → `fotos.json` com as 4 categorias.
- [ ] Commit.

### Task 2: Estrutura e estilo (`index.html`, `css/site.css`)
Seções: `#capa`, `#galeria`, `#servicos`, `#sobre`, `#contato`, rodapé. Textura de papel via SVG `feTurbulence` inline (sem imagem extra).
- [ ] Verificação: abrir no navegador, screenshot desktop e 375 px; sem rolagem horizontal.
- [ ] Commit.

### Task 3: WhatsApp por serviço
`linkWhatsApp(servico: string) -> string` em `js/site.js` → `https://wa.me/5567992379876?text=` + `encodeURIComponent("Oi Karina! Vim pelo site e queria um orçamento de " + servico + ".")`. Cada card de serviço e o botão de contato usam isso; `href` estático de fallback no HTML.
- [ ] Verificação: inspecionar `href` gerado para "Still de set / making-of".
- [ ] Commit.

### Task 4: Galeria e lightbox (`js/site.js`)
Abas por categoria leem `assets/fotos.json`; lightbox com Esc, setas, swipe e clique fora.
- [ ] Verificação no navegador: trocar abas, abrir/fechar lightbox, navegar; console sem erros; desktop e 375 px.
- [ ] Commit.
