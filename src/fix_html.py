import re

HTML_ENTITIES = {
    "lt": "<",
    "gt": ">",
    "amp": "&",
    "quot": "\"",
    "apos": "'"
}

_entity_re = re.compile(r"&(#x?[0-9a-fA-F]+|\w+);")

def unescape_html(text: str) -> str:
    def replace_entity(match):
        entity = match.group(1)
        if entity.startswith("#x"):
            try:
                return chr(int(entity[2:], 16))
            except ValueError:
                return match.group(0)
        elif entity.startswith("#"):
            try:
                return chr(int(entity[1:]))
            except ValueError:
                return match.group(0)
        else:
            return HTML_ENTITIES.get(entity, match.group(0))
    
    return _entity_re.sub(replace_entity, text)
