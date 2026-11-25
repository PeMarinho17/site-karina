import os
import sys
from pathlib import Path

import pytest
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import preparar_fotos as pf  # noqa: E402

CR3_VERTICAL = Path("F:/DCIM/100CANON/_MG_9736.CR3")
CR3_HORIZONTAL = Path("F:/DCIM/100CANON/_MG_9734.CR3")


def test_exportar_gera_grande_e_mini_com_lado_maior_certo(tmp_path):
    img = Image.new("RGB", (4000, 3000), "gray")
    item = pf.exportar(img, "teste", "ensaios", tmp_path)
    grande = Image.open(tmp_path / item["grande"])
    mini = Image.open(tmp_path / item["mini"])
    assert max(grande.size) == 1600
    assert max(mini.size) == 600
    assert (item["w"], item["h"]) == grande.size
    assert item["categoria"] == "ensaios"
    assert item["grande"] == "assets/fotos/grande/teste.webp"


def test_exportar_nao_amplia_foto_pequena(tmp_path):
    img = Image.new("RGB", (800, 1200), "gray")
    item = pf.exportar(img, "pequena", "eventos", tmp_path)
    assert (item["w"], item["h"]) == (800, 1200)


@pytest.mark.skipif(not CR3_VERTICAL.exists(), reason="cartão SD não conectado")
def test_extrair_prvw_aplica_rotacao_da_camera():
    vertical = pf.extrair_prvw(CR3_VERTICAL)
    horizontal = pf.extrair_prvw(CR3_HORIZONTAL)
    assert vertical.height > vertical.width
    assert horizontal.width > horizontal.height
