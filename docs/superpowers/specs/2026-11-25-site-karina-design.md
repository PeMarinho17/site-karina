# Site de fotografia — Karina Coutinho (@fractalume)

## Intenção
Site para quem quer contratar a Karina: pessoas (ensaios, eventos, casamentos) e produtoras / sets de cinema (still e making-of). Nada de publicidade. Ação principal: pedir orçamento pelo WhatsApp depois de ver a galeria.

## Objetivos
- Galeria por categoria (Ensaios, Eventos, Casamentos) com visualização em tela cheia.
- Serviços: Ensaios, Eventos, Casamentos, Still de set / making-of.
- Contato: WhatsApp (67) 99237-9876 com mensagem pronta por serviço; e-mail karina.coutinho@ufms.br; Campo Grande/MS; Instagram @fractalume.

## Não-objetivos / anti-objetivos
- Sem publicidade, sem loja, sem login, sem formulário com back-end.
- Fugir do visual genérico (gradiente, cards iguais, sombras).

## Restrições
- Estética do PDF: papel claro texturizado, serifa alta e condensada, fonte de máquina de escrever, detalhe vermelho-tijolo.
- Fotos do cartão SD sem edição (aceito pelo cliente): só rotação e redimensionamento. Casamento entra como prévia.
- Set de cinema sem fotos ainda: só texto.

## Abordagens
1. **HTML/CSS/JS puro, sem build (escolhida)** — leve, hospedagem grátis (GitHub Pages/Netlify), trocar fotos = pasta + script.
2. Astro — organizado para galerias grandes, mas traz build e dependências sem necessidade.
3. Wix/Squarespace — edição pela própria Karina, mas mensalidade, template preso e não dá para montar daqui.

## Decidido
Uma página rolando: Capa → Galeria (abas) → Serviços → Sobre → Contato. Pasta `E:\site-karina`.

## Calls do builder (minhas)
- Fontes Google: serifa condensada (tipo "Bodoni Moda"/"Playfair" condensada) + monoespaçada de máquina de escrever.
- Fotos em WebP, ~1600px no lado maior, com miniaturas; script Python de preparação em `tools/`.
- Texto do "Sobre" é provisório até a Karina mandar o dela.
