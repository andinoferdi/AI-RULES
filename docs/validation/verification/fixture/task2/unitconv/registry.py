import json
from functools import lru_cache
from pathlib import Path

_DATA = Path(__file__).with_name("data") / "units.json"


@lru_cache(maxsize=1)
def _units():
    return json.loads(_DATA.read_text(encoding="utf-8"))


def convert_by_name(value, from_unit, to_unit):
    """Convert between linear units listed in data/units.json (factor to the base unit)."""
    units = _units()
    source, target = units[from_unit], units[to_unit]
    if source["dimension"] != target["dimension"]:
        raise ValueError(f"cannot convert {from_unit} to {to_unit}")
    return value * source["factor"] / target["factor"]
