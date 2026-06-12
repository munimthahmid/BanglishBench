#!/usr/bin/env python3
"""Small deterministic Bangla-to-Latin romanization helper.

This is a bootstrap utility for pilot construction, not a publication-quality
transliteration system. Generated Banglish should be treated as unverified.
"""

from __future__ import annotations

import re
import unicodedata


INHERENT = "\ue000"
VIRAMA = "\u09cd"
NUKTA = "\u09bc"

INDEPENDENT_VOWELS = {
    "\u0985": "o",
    "\u0986": "a",
    "\u0987": "i",
    "\u0988": "i",
    "\u0989": "u",
    "\u098a": "u",
    "\u098b": "ri",
    "\u098c": "li",
    "\u098f": "e",
    "\u0990": "oi",
    "\u0993": "o",
    "\u0994": "ou",
}

VOWEL_SIGNS = {
    "\u09be": "a",
    "\u09bf": "i",
    "\u09c0": "i",
    "\u09c1": "u",
    "\u09c2": "u",
    "\u09c3": "ri",
    "\u09c4": "ri",
    "\u09c7": "e",
    "\u09c8": "oi",
    "\u09cb": "o",
    "\u09cc": "ou",
}

CONSONANTS = {
    "\u0995": "k",
    "\u0996": "kh",
    "\u0997": "g",
    "\u0998": "gh",
    "\u0999": "ng",
    "\u099a": "ch",
    "\u099b": "chh",
    "\u099c": "j",
    "\u099d": "jh",
    "\u099e": "n",
    "\u099f": "t",
    "\u09a0": "th",
    "\u09a1": "d",
    "\u09a2": "dh",
    "\u09a3": "n",
    "\u09a4": "t",
    "\u09a5": "th",
    "\u09a6": "d",
    "\u09a7": "dh",
    "\u09a8": "n",
    "\u09aa": "p",
    "\u09ab": "f",
    "\u09ac": "b",
    "\u09ad": "bh",
    "\u09ae": "m",
    "\u09af": "j",
    "\u09b0": "r",
    "\u09b2": "l",
    "\u09b6": "sh",
    "\u09b7": "sh",
    "\u09b8": "s",
    "\u09b9": "h",
    "\u09dc": "r",
    "\u09dd": "rh",
    "\u09df": "y",
    "\u09ce": "t",
}

NUKTA_CONSONANTS = {
    "\u09a1": "r",
    "\u09a2": "rh",
    "\u09af": "y",
}

MARKS = {
    "\u0981": "n",
    "\u0982": "ng",
    "\u0983": "h",
}

DIGITS = {
    "\u09e6": "0",
    "\u09e7": "1",
    "\u09e8": "2",
    "\u09e9": "3",
    "\u09ea": "4",
    "\u09eb": "5",
    "\u09ec": "6",
    "\u09ed": "7",
    "\u09ee": "8",
    "\u09ef": "9",
}

PUNCT = {
    "\u0964": ".",
    "\u0965": ".",
    "\u09f7": "",
}


def _postprocess_common_artifacts(text: str) -> str:
    """Clean up high-confidence artifacts from the bootstrap romanizer."""

    replacements = [
        (r"\bdb", "dw"),
        (r"\boja(?=[a-z])", "a"),
        (r"\bboijnanik\b", "boigganik"),
        (r"\bkhadyoke\b", "khaddoke"),
        (r"\bkhadyer\b", "khadder"),
        (r"\bkhadye\b", "khadde"),
        (r"\bkhady\b", "khaddo"),
        (r"\bdurotber\b", "durotter"),
        (r"\bdurotb\b", "durotto"),
        (r"\bgurutbopurn\b", "guruttopurn"),
        (r"\bdharokotb\b", "dharokotto"),
        (r"\btottb\b", "totto"),
        (r"\btboron\b", "tworon"),
        (r"\btbok\b", "twok"),
    ]
    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text


def _resolve_inherent_vowels(text: str) -> str:
    out: list[str] = []
    for idx, ch in enumerate(text):
        if ch != INHERENT:
            out.append(ch)
            continue

        next_ch = text[idx + 1] if idx + 1 < len(text) else ""
        if next_ch and next_ch.isalpha():
            out.append("o")

    return "".join(out)


def romanize_bangla(text: str) -> str:
    """Return a rough Latin-script rendering of Bangla text."""

    text = unicodedata.normalize("NFC", text)
    out: list[str] = []
    i = 0
    while i < len(text):
        ch = text[i]
        nxt = text[i + 1] if i + 1 < len(text) else ""
        nxt2 = text[i + 2] if i + 2 < len(text) else ""
        nxt3 = text[i + 3] if i + 3 < len(text) else ""

        if ch in INDEPENDENT_VOWELS:
            out.append(INDEPENDENT_VOWELS[ch])
            i += 1
            continue

        if ch in NUKTA_CONSONANTS and nxt == NUKTA:
            base = NUKTA_CONSONANTS[ch]
            if nxt2 in VOWEL_SIGNS:
                out.append(base + VOWEL_SIGNS[nxt2])
                i += 3
                continue
            if nxt2 == VIRAMA:
                out.append(base)
                i += 3
                continue
            out.append(base + INHERENT)
            i += 2
            continue

        if ch in CONSONANTS:
            base = CONSONANTS[ch]
            if nxt == VIRAMA and nxt2 == "\u09af":
                if nxt3 in VOWEL_SIGNS:
                    out.append(base + "y" + VOWEL_SIGNS[nxt3])
                    i += 4
                    continue
                out.append(base + "y" + INHERENT)
                i += 3
                continue
            if nxt in VOWEL_SIGNS:
                out.append(base + VOWEL_SIGNS[nxt])
                i += 2
                continue
            if nxt == VIRAMA:
                out.append(base)
                i += 2
                continue
            out.append(base + INHERENT)
            i += 1
            continue

        if ch in VOWEL_SIGNS:
            out.append(VOWEL_SIGNS[ch])
        elif ch in MARKS:
            out.append(MARKS[ch])
        elif ch in DIGITS:
            out.append(DIGITS[ch])
        elif ch in PUNCT:
            out.append(PUNCT[ch])
        elif ch == NUKTA:
            pass
        elif ch == VIRAMA:
            pass
        else:
            out.append(ch)
        i += 1

    romanized = _resolve_inherent_vowels("".join(out))
    romanized = _postprocess_common_artifacts(romanized)
    romanized = re.sub(r"[ \t]+", " ", romanized)
    romanized = re.sub(r" *\n *", "\n", romanized)
    return romanized.strip()


def romanize_noisy(text: str) -> str:
    """Deterministic lightweight noisy variant for later pilot ablations."""

    text = romanize_bangla(text)
    replacements = [
        ("bh", "v"),
        ("ph", "f"),
        ("sh", "s"),
        ("chh", "ch"),
        ("kh", "k"),
        ("oi", "oy"),
    ]
    for src, dst in replacements:
        text = text.replace(src, dst)
    return text


if __name__ == "__main__":
    import sys

    print(romanize_bangla(sys.stdin.read()))
