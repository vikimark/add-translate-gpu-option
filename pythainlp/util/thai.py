# -*- coding: utf-8 -*-
"""
Check if it is Thai text
"""
import string

from pythainlp import thai_above_vowels, thai_tonemarks

_DEFAULT_IGNORE_CHARS = string.whitespace + string.digits + string.punctuation
_TH_FIRST_CHAR_ASCII = 3584
_TH_LAST_CHAR_ASCII = 3711


def isthaichar(ch: str) -> bool:
    """Check if a character is a Thai character.

    :param ch: input character
    :type ch: str
    :return: True if ch is a Thai characttr, otherwise False.
    :rtype: bool

    :Example:
    ::

        from pythainlp.util import isthaichar

        isthaichar("ก")  # THAI CHARACTER KO KAI
        # output: True

        isthaichar("๕")  # THAI DIGIT FIVE
        # output: True
    """
    ch_val = ord(ch)
    if ch_val >= _TH_FIRST_CHAR_ASCII and ch_val <= _TH_LAST_CHAR_ASCII:
        return True
    return False


def isthai(text: str, ignore_chars: str = ".") -> bool:
    """Check if every characters in a string are Thai character.

    :param text: input text
    :type text: str
    :param ignore_chars: characters to be ignored, defaults to "."
    :type ignore_chars: str, optional
    :return: True if every characters in the input string are Thai,
             otherwise False.
    :rtype: bool

    :Example:
    ::

        from pythainlp.util import isthai

        isthai("กาลเวลา")
        # output: True

        isthai("กาลเวลา.")
        # output: True

        isthai("กาล-เวลา")
        # output: False

        isthai("กาล-เวลา +66", ignore_chars="01234567890+-.,")
        # output: True

    """
    if not ignore_chars:
        ignore_chars = ""

    for ch in text:
        if ch not in ignore_chars and not isthaichar(ch):
            return False
    return True


def countthai(text: str, ignore_chars: str = _DEFAULT_IGNORE_CHARS) -> float:
    """Find proportion of Thai characters in a given text

    :param text: input text
    :type text: str
    :param ignore_chars: characters to be ignored, defaults to whitespaces,\\
        digits, and puntuations.
    :type ignore_chars: str, optional
    :return: proportion of Thai characters in the text (percent)
    :rtype: float

    :Example:
    ::

        from pythainlp.util import countthai

        countthai("ไทยเอ็นแอลพี 3.0")
        # output: 100.0

        countthai("PyThaiNLP 3.0")
        # output: 0.0

        countthai("ใช้งาน PyThaiNLP 3.0")
        # output: 40.0

        countthai("ใช้งาน PyThaiNLP 3.0", ignore_chars="")
        # output: 30.0
    """
    if not text or not isinstance(text, str):
        return 0.0

    if not ignore_chars:
        ignore_chars = ""

    num_thai = 0
    num_ignore = 0

    for ch in text:
        if ch in ignore_chars:
            num_ignore += 1
        elif isthaichar(ch):
            num_thai += 1

    num_count = len(text) - num_ignore

    if num_count == 0:
        return 0.0

    return (num_thai / num_count) * 100


def display_thai_char(ch: str) -> str:
    """Prefix an underscore (_) to a high-position vowel or a tone mark,
    to ease readability.

    :param ch: input character
    :type ch: str
    :return: "_" + ch
    :rtype: str

    :Example:
    ::

        from pythainlp.util import display_thai_char

        display_thai_char("้")
        # output: "_้"
    """

    if (
        ch in thai_above_vowels
        or ch in thai_tonemarks
        or ch in "\u0e33\u0e4c\u0e4d\u0e4e"
    ):
        # last condition is Sra Aum, Thanthakhat, Nikhahit, Yamakkan
        return "_" + ch
    else:
        return ch
