import json
import os
from threading import Lock

_TRANSLATIONS = {}
_LOCK = Lock()

TRANSLATION_DIR = os.path.dirname(os.path.abspath(__file__))


def _load_translations(lang):
    with _LOCK:
        if lang not in _TRANSLATIONS:
            path = os.path.join(TRANSLATION_DIR, f"{lang}.json")
            try:
                with open(path, "r", encoding="utf-8") as f:
                    _TRANSLATIONS[lang] = json.load(f)
            except FileNotFoundError:
                _TRANSLATIONS[lang] = {}
        return _TRANSLATIONS[lang]


def tr(key, lang, **kwargs):
    """
    Usage: tr('some_key', 'en', name='John')
    """
    translations = _load_translations(lang)
    text = translations.get(key)
    if text is None:
        # fallback to English
        if lang != 'en':
            translations_en = _load_translations('en')
            text = translations_en.get(key, f"[No translation: {key}]")
        else:
            text = f"[No translation: {key}]"
    try:
        return text.format(**kwargs)
    except Exception:
        return text 