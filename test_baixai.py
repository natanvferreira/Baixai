"""Teste rápido (precisa de internet): python test_baixai.py"""
import tempfile
from pathlib import Path

from baixai import baixar

with tempfile.TemporaryDirectory() as pasta:
    log = []
    falhas = baixar(["https://www.youtube.com/watch?v=jNQXAC9IVRw", "link-invalido"], pasta, log.append)
    print("\n".join(log))
    assert falhas == ["link-invalido"], falhas
    assert any(Path(pasta).iterdir()), "nenhum arquivo baixado"
print("OK")
