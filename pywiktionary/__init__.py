"""`Wiktionary pronunciation collector`

A Python toolkit converting pronunciation in enwiktionary xml dump
to cmudict format. Support IPA and X-SAMPA format at present.
"""

from .wiktionary import Wiktionary
from .parser import Parser
from .IPA import IPA


__author__ = "Yifan Xiong"
__version__ = "0.0.2"
__email__ = "abuccts@gmail.com"
