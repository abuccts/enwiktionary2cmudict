"""Hindi IPA pronunciation module. Implements template {{hi-IPA}}.
Modifiled from https://en.wiktionary.org/wiki/Module:hi-IPA Lua module partially.
"""

from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import re

from .hi_translit import transliterate


correspondences = {
    "ṅ": "ŋ", "g": "ɡ", 
    "c": "t͡ʃ", "j": "d͡ʒ", "ñ": "ɲ",
    "ṭ": "ʈ", "ḍ": "ɖ", "ṇ": "ɳ",
    "t": "t̪", "d": "d̪",
    "y": "j", "r": "ɾ", "v": "ʋ", "l": "l̪",
    "ś": "ʃ", "ṣ": "ʃ", "h": "ɦ",
    "ṛ": "ɽ", "ž": "ʒ", "ḻ": "ɭ", "ġ": "ɡ",
    "q": "k", "x": "kʰ", "ṉ": "n", "ṟ": "ɹ",

    "a": "ə", "ā": "ɑː", "i": "ɪ",
    "ī": "iː", "o": "oː", "e": "eː", "ŕ": "ɾɪ",
    "u": "ʊ", "ū": "uː", "ŏ": "ɔ", "ĕ": "æː",

    "ũ": "ʊ̃", "õ": "õː", "ã": "ə̃", "ā̃": "ɑ̃ː", 

    "ॐ": "oːm", "ḥ": "ʰ",
    # get rid of spaces
    " ": "",
}

identical = "knlsfzθ"
for ch in identical:
    correspondences[ch] = ch

vowels = "aāiīuūoɔɛeæ"
weak_h = "([gjdḍbṛnmaãāā̃eẽiĩīī̃uũūū̃oõː])h"
aspirate = "([kctṭp])"
syllabify_pattern = "([" + vowels + "])" + \
                    "([^" + vowels + "\.]?)" + \
                    "([^" + vowels + "\.]+)" + \
                    "([" + vowels + "])"


def syllabify(text):
    def repl(match):
        a, b, c, d = \
            match.group(1), match.group(2), match.group(3), match.group(4)
        if re.match(weak_h, b + c) or re.match(aspirate + "h", b + " " + c):
            b, c = "", b + c
        if c == "" and b != "":
            c, b = b, ""
        return a + b + "." + c + d

    for count in range(2):
        text = re.sub(syllabify_pattern, repl, text)
    return text

def to_IPA(text):
    translit = transliterate(text)
    if not translit:
        return ""

    translit = re.sub("͠", "̃", translit)
    translit = re.sub("a(̃?)i", r"ɛ\1ː", translit)
    translit = re.sub("a(̃?)u", r"ɔ\1ː", translit)
    translit = re.sub("\-", ".", translit)

    translit = syllabify(translit)
    translit = re.sub("jñ", "gy", translit)
    translit = re.sub("ah", "ɛːʱ", translit)
    translit = re.sub(aspirate + "h", r"\1ʰ", translit)
    translit = re.sub(weak_h, r"\1ʱ", translit)
    translit = re.sub("\.ː", "ː.", translit)

    result = []
    for ch in translit:
        if ch in correspondences.keys():
            result.append(correspondences[ch])
        else:
            result.append(ch)
    return "".join(result)
