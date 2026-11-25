"""Gera as fotos do site (WebP) e assets/fotos.js a partir do PDF do portfólio e dos RAW (.CR3).

Uso: python tools/preparar_fotos.py <portfolio.pdf> <pasta DCIM>
A lista de fotos fica em tools/selecao.json:
  "pdf:<xref>"            imagem embutida no PDF
  "cr3:<pasta>/<arquivo>" prévia JPEG embutida no RAW, sem a extensão
"""
import io
import json
import struct
import sys
from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).resolve().parents[1]
LADO_GRANDE = 1600
LADO_MINI = 600
TAG_ORIENTACAO = 0x0112
ROTACAO = {3: Image.Transpose.ROTATE_180, 6: Image.Transpose.ROTATE_270, 8: Image.Transpose.ROTATE_90}


def _orientacao_tiff(tiff: bytes) -> int:
    ordem = "<" if tiff[:2] == b"II" else ">"
    (ifd,) = struct.unpack(ordem + "I", tiff[4:8])
    (n,) = struct.unpack(ordem + "H", tiff[ifd:ifd + 2])
    for i in range(n):
        tag, _tipo, _qtd, valor = struct.unpack(ordem + "HHIH", tiff[ifd + 2 + 12 * i: ifd + 12 + 12 * i])
        if tag == TAG_ORIENTACAO:
            return valor
    return 1


def extrair_prvw(caminho_cr3: Path) -> Image.Image:
    """Prévia JPEG (~1620 px) embutida no CR3, já na orientação em que foi fotografada."""
    cabeca = Path(caminho_cr3).read_bytes()[:3_000_000]
    inicio = cabeca.index(b"\xff\xd8", cabeca.index(b"PRVW"))
    fim = cabeca.index(b"\xff\xd9", inicio) + 2
    img = Image.open(io.BytesIO(cabeca[inicio:fim]))
    img.load()
    cmt1 = cabeca.find(b"CMT1")
    orientacao = _orientacao_tiff(cabeca[cmt1 + 4:cmt1 + 4096]) if cmt1 >= 0 else 1
    return img.transpose(ROTACAO[orientacao]) if orientacao in ROTACAO else img


def _salvar(img: Image.Image, lado: int, destino: Path) -> Image.Image:
    copia = img.convert("RGB")
    copia.thumbnail((lado, lado), Image.Resampling.LANCZOS)
    destino.parent.mkdir(parents=True, exist_ok=True)
    copia.save(destino, "WEBP", quality=82, method=6)
    return copia


def exportar(img: Image.Image, id_foto: str, categoria: str, raiz: Path = RAIZ) -> dict:
    grande = f"assets/fotos/grande/{id_foto}.webp"
    mini = f"assets/fotos/mini/{id_foto}.webp"
    salva = _salvar(img, LADO_GRANDE, raiz / grande)
    _salvar(img, LADO_MINI, raiz / mini)
    return {"id": id_foto, "categoria": categoria, "grande": grande, "mini": mini, "w": salva.width, "h": salva.height}


def _abrir(origem: str, pdf, dcim: Path) -> tuple[str, Image.Image]:
    tipo, ref = origem.split(":", 1)
    if tipo == "pdf":
        dados = pdf.extract_image(int(ref))["image"]
        return f"pdf-{ref}", Image.open(io.BytesIO(dados))
    if tipo == "cr3":
        return ref.split("/")[-1].lower().strip("_"), extrair_prvw(dcim / f"{ref}.CR3")
    raise ValueError(f"origem desconhecida: {origem}")


def main(caminho_pdf: str, dcim: str) -> None:
    import pymupdf

    pdf = pymupdf.open(caminho_pdf)
    selecao = json.loads((RAIZ / "tools" / "selecao.json").read_text(encoding="utf-8"))
    _, papel = _abrir(selecao.pop("papel"), pdf, Path(dcim))
    _salvar(papel, 1400, RAIZ / "assets" / "papel.webp")
    fotos = []
    for categoria, origens in selecao.items():
        for origem in origens:
            id_foto, img = _abrir(origem, pdf, Path(dcim))
            fotos.append(exportar(img, id_foto, categoria))
    conteudo = "window.FOTOS = " + json.dumps(fotos, indent=1) + ";\n"
    (RAIZ / "assets" / "fotos.js").write_text(conteudo, encoding="utf-8")
    print(f"{len(fotos)} fotos geradas")


if __name__ == "__main__":
    main(*sys.argv[1:3])
