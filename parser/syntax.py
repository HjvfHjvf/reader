from pyparsing import *
import re


int_nums = Regex(re.compile(r'[-|+]?\d+'))('integer')
real_nums = Regex(re.compile(r'[-|+]?(\d+)*\.\d+'))('real')
named = Regex(re.compile(r'/[\w\d\.@#\$%\^&*\(\)]+'))('named')
boolean = Regex(re.compile(r'true|false'))('bool')
reference = Regex(re.compile(r'\d+ \d+ R'))('reference')
null = Regex(re.compile(r'null'))('null')


def string():
    s = Forward()('string')
    entry = Regex(re.compile(r'[\w\d]+'))('entry')
    content = Group(entry | s)
    left = Literal('(').suppress()
    right = Literal(')').suppress()
    s << left + ZeroOrMore(content) + right
    return s
s = string()


def array():
    a = Forward()('array')
    left = Literal('[').suppress()
    right = Literal(']').suppress()
    entry = reference | real_nums | int_nums | named | boolean | null | a
    a << left + ZeroOrMore(Group(entry)) + right
    return a
a = array()


def dictionary():
    dct = Forward()('dictionary')
    left = Literal('<<').suppress()
    right = Literal('>>').suppress()
    key = named
    value = reference | real_nums | int_nums | named | boolean | null | a | dct
    entry = Group(key + value)
    dct << left + ZeroOrMore(entry) + right
    return dct
d = dictionary()


def get_int(string):
    return int(string)


def get_float(string):
    return float(string)


def get_name(string):
    return string[1:]


def get_bool(string):
    return True if string == 'true' else False


def get_null(string):
    return None


def get_reference(string):
    l = string.split()
    return int(l[0]), int(l[1]), l[2]


def get_string(tokens):
    for token in tokens:
        if 'entry' in token:
            element = token.entry
        elif 'string' in token:
            element = [e for e in get_string(token.string)]
        print(element)
        yield element


def get_array(tokens):
    for token in tokens:
        if 'reference' in token:
            element = get_reference(token[0])
        elif 'integer' in token:
            element = get_int(token[0])
        elif 'real' in token:
            element = get_float(token[0])
        elif 'named' in token:
            element = get_name(token[0])
        elif 'bool' in token:
            element = get_bool(token[0])
        elif 'null' in token:
            element = None
        elif 'array' in token:
            element = [e for e in get_array(token.array)]
        yield element


def get_dict(tokens):
    for token in tokens:
        key = get_name(token[0])
        if ('named' in token) and (token.named is token[1]):
            value = get_name(token[1])
        elif 'integer' in token:
            value = get_int(token[1])
        elif 'real' in token:
            value = get_float(token[1])
        elif 'dictionary' in token:
            value = dict((k, v) for k, v in get_dict(token.dictionary))
        elif 'bool' in token:
            value = get_bool(token[1])
        elif 'reference' in token:
            value = get_reference(token[1])
        elif 'array' in token:
            value = [e for e in get_array(token.array)]
        elif 'null' in token:
            value = None
        # print(key, '\t', value, '\t', token)
        yield key, value


def build_string(string):
    return [e for e in get_string(string)]


def build_array(string):
    return [e for e in get_array(a.parseString(string))]


def build_dict(string):
    return dict((k, v) for k, v in get_dict(d.parseString(string)))


test = "()"
test_1 = "(kljh345)"
