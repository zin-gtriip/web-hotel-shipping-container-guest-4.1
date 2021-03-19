import re


def replace_illegal_char(text):
    char2replace = {
        '[@]': '_at_',
        '[.]': '_dot_'
    }
    for from_char, to_char in char2replace.items():
        text = re.sub(from_char, to_char, text)
    return text
