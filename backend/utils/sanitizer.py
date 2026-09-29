import re
_REPLACEMENTS = {"\u2018":"'","\u2019":"'","\u201c":'"',"\u201d":'"',"\u2013":"-","\u2014":"-","\u2026":"...","\u00a0":" "}
def sanitize_text(text):
    text = text or ""
    for old, new in _REPLACEMENTS.items(): text = text.replace(old, new)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+\n", "\n", text)
    return re.sub(r"\n{4,}", "\n\n\n", text).strip()
