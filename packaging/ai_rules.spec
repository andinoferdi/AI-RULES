# PyInstaller release spec for the standalone AI-RULES control plane.
from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files

ROOT = Path(SPECPATH).parent
datas = []
for package in ("ai_rules.catalog", "ai_rules.profiles", "ai_rules.release"):
    datas.extend(collect_data_files(package))

a = Analysis(
    [str(ROOT / "packaging" / "entrypoint.py")],
    pathex=[str(ROOT / "src")],
    datas=datas,
    hiddenimports=["questionary"],
    name="ai-rules",
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    name="ai-rules",
    console=True,
    strip=False,
    upx=False,
)
