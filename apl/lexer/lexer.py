"""
Language lexer definition
"""
import re

from apl.tokens import token_type
from apl.tokens import regex_type
from apl.tokens import tokens
from apl.tokens.tokens import Token


def is_skip_char(char, input_str, current):
    """
    Check if the given char is at the given current position in the given input_str

    :param char: character to skip
    :param input_str: input string to check
    :param current: input string index to check
    :return: tuple (char_to_eat, None)
    """
    return 1 if input_str[current] == char else 0, None


def is_single_char_token(typename, value, input_str, current):
    """
    Check if 'value' is located at 'current' position in 'input_str'

    :param typename: Token type generate
    :param value: Value to check
    :param input_str: input string checked
    :param current: index in input_str
    :return: (1, Token(typename, value)) if input_str[current] == value
             (0, None) otherwise
    """
    if value == input_str[current]:
        return 1, Token(typename, value)
    else:
        return 0, None


def is_pattern_token(typename, pattern, input_str, current):
    """
    Check if 'pattern' is found at 'current' in 'input_str' and create Token of type 'typename'

    :param typename: token typename
    :param pattern: regex pattern to match
    :param input_str: input string to check
    :param current: index to check regex
    :return: (char_to_eat, Token(typename, pattern matched) if the given pattern is found
             (0, None)
    """
    sub_str = input_str[current:]
    match = re.match(pattern, sub_str)
    if match:
        val = match.group()
        return len(val), Token(typename, val)
    else:
        return 0, None


def get_matching_func_list():
    func_list = []
    for typename, match_type, regex in tokens.TOKEN_REGEX:
        if match_type == regex_type.SKIP:
            func_list.append(lambda s, c, r=regex: is_skip_char(r, s, c))
        elif match_type == regex_type.SINGLE_CHAR:
            func_list.append(lambda s, c, r=regex, t=typename: is_single_char_token(t, r, s, c))
        elif match_type == regex_type.PATTERN:
            func_list.append(lambda s, c, r=regex, t=typename: is_pattern_token(t, r, s, c))
    return func_list


class TokenMatchingError(Exception):
    pass


class Lexer:
    """
    Lexer tokenizing input string
    """

    text = str()
    index = int()
    matching_func_list = []

    def __init__(self, text):
        """
        Construct a lexer for the given input string

        :param text: program input string
        """
        self.text = text
        self.index = 0
        self.matching_func_list = get_matching_func_list()

    def error(self):
        raise TokenMatchingError('No matching token at index %s' % self.index)

    def get_next_token(self):
        """
        Get next token from input string

        :return: Next Token from string
        """
        if self.index == len(self.text):
            return Token(token_type.EOF, '\0')
        for f in self.matching_func_list:
            consumed, token = f(self.text, self.index)
            if consumed > 0:
                self.index += consumed
                if token:
                    return token
        self.error()

    @staticmethod
    def tokenize(input_str):
        """
        Convert input string to token list

        :param input_str: string to tokenize
        :return: list of Token matching with input string
        """
        func_list = get_matching_func_list()
        token_list = []

        index = 0
        end = False
        error = False
        error_messages = []

        while not (end or error):
            match = False
            for f in func_list:
                consumed, token = f(input_str, index)
                if consumed > 0:
                    match = True
                    index += consumed
                    if token is not None:
                        token_list.append(token)
                    break
            error = not match
            end = index == len(input_str)
        if error:
            error_messages.append("No matching token @ index:" + str(index))
            error_messages.append("\t" + input_str)
            error_messages.append("\t" + index * " " + "^")
        return token_list, error_messages



