import re
import time

from . import log
from .catalog import STRINGS, TEMPLATES

COMPILE_SECONDS = 0.0005  # parsing and validating a template costs about half a millisecond
TOKEN = re.compile(r"\{\{(t:)?(\w+)\}\}")


class Compiled:
    def __init__(self, name, locale, parts):
        self.name = name
        self.locale = locale
        self.parts = parts  # list of (is_field, text)

    def render(self, context):
        out = []
        for is_field, text in self.parts:
            out.append(str(context.get(text, "")) if is_field else text)
        return "".join(out)


def compile_template(name, locale):
    end = time.perf_counter() + COMPILE_SECONDS
    while time.perf_counter() < end:
        pass
    source = TEMPLATES[name]
    strings = STRINGS[locale]
    parts = []
    position = 0
    for match in TOKEN.finditer(source):
        parts.append((False, source[position:match.start()]))
        if match.group(1):
            parts.append((False, strings[match.group(2)]))
        elif match.group(2) == "template":
            parts.append((False, name))
        else:
            parts.append((True, match.group(2)))
        position = match.end()
    parts.append((False, source[position:]))
    return Compiled(name, locale, parts)


_compiled = {}


def render(name, locale, context, request_id):
    key = (name, locale, request_id)
    compiled = _compiled.get(key)
    if compiled is None:
        compiled = compile_template(name, locale)
        _compiled[key] = compiled
    log.event("render", request_id=request_id, template=name, locale=locale)
    return compiled.render(context)
