# -*- coding:utf-8 -*-
"""
name++
でポイントアップ

name--
でポイントダウン

nameに使えるのは英字のみ。大文字小文字のケースは無視される。

TODO コードがださいからなおす
TODO 複数行のメッセージの場合に未対応.
TODO +++とかで100ポイントとか
"""

# stblibs
import logging
import re
import threading
# thirdparty libs
from skypehub.handlers import on_message
# original libs
from models import Value


PLUS_REGEX = re.compile("^([a-z]*)\+\+$")
MINUS_REGEX = re.compile("^([a-z]*)--$")


LOG = logging.getLogger('skypebot.value')
DB_LOCK = threading.Lock()


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


def update_value(name, update):
    with DB_LOCK:
        value, created = Value.objects.get_or_create(name=name)
        value.point = value.point + update
        value.save()
    return value


def update(message, target, point):
    value = update_value(target, point)
    message.Chat.SendMessage(u"%s (通算 %s ポイント)" % (value.name, value.point))


def plus(message):
    target = find_plus(message.Body)
    if target is not None:
        LOG.debug(u"%s is point plus ++", target)
        update(message, target, 1)


def minus(message):
    target = find_minus(message.Body)
    if target is not None:
        LOG.debug(u"%s is point minus --", target)
        update(message, target, -1)


def receiver(handler, message, status):
    # メッセージ受信したときのみ
    if status != 'RECEIVED':
        return
    plus(message)
    minus(message)


# レシーバを登録
on_message.connect(receiver)
