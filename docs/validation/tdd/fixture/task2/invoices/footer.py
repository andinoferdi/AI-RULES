"""Legal footer printed under every invoice."""

COMPANY = "CV Sinar Kertas"
NPWP = "01.234.567.8-901.000"


def footer() -> str:
    return f"{COMPANY} - NPWP {NPWP}"
