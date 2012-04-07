# -*- coding:utf-8 -*-

import re


PLUS_REGEX = re.compile("^([a-z]*)\+\+$")
MINUS_REGEX = re.compile("^([a-z]*)--$")


def find_plus(body):
    return find(body, PLUS_REGEX)


def find_minus(body):
    return find(body, MINUS_REGEX)


def find(body, regex):
    msg = body.lower()
    try:
        return regex.match(msg).group(1)
    except:
        return None


def main():
    msg1 = """Tanacasino++"""
    msg2 = """tanacasino++"""
    print find_plus(msg1)
    print find_plus(msg2)
    msg3 = """Tanacasino--"""
    msg4 = """tanacasino--"""
    print find_minus(msg3)
    print find_minus(msg4)


if __name__ == '__main__':
    main()
