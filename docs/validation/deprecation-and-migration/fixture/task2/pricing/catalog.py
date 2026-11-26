from decimal import Decimal

# Unit prices in rupiah. DISCONTINUED items stay listed so old orders can be read.
PRICES = {
    "KOPI-250": Decimal("48500"),
    "KOPI-1000": Decimal("172000"),
    "GULA-500": Decimal("12500.50"),
    "SUSU-1L": Decimal("21333.33"),
    "CUP-12OZ": Decimal("1250.25"),
    "FILTER-100": Decimal("37999.50"),
}
DISCONTINUED = {"TEH-100", "SIRUP-750"}
