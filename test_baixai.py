"""Teste rápido (precisa de internet e FFmpeg): python test_baixai.py"""
import tempfile
from pathlib import Path

from baixai import baixar

VIDEO = "https://www.youtube.com/watch?v=jNQXAC9IVRw"

with tempfile.TemporaryDirectory() as pasta:
    log = []
    falhas = baixar([VIDEO, "link-invalido"], pasta, log.append)
    print("\n".join(log))
    assert falhas == ["link-invalido"], falhas
    assert any(Path(pasta).iterdir()), "nenhum arquivo baixado"

with tempfile.TemporaryDirectory() as pasta:
    log = []
    assert baixar([VIDEO], pasta, log.append, mp3=True) == []
    print("\n".join(log))
    assert [p.suffix for p in Path(pasta).iterdir()] == [".mp3"]
print("OK")
