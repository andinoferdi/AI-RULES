from importlib import import_module


def get(locale: str, key: str) -> str:
    catalogue = import_module(f"shopline.i18n.messages_{locale}").MESSAGES
    return catalogue[key]
