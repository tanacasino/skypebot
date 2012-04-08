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


def get_point(message):
    target = find(message.Body, PLUS_REGEX)
    if target is not None:
        return target, 1
    target = find(message.Body, MINUS_REGEX)
    if target is not None:
        return target, -1
    return None, 0


def receiver(handler, message, status):
    # メッセージ受信したときのみ
    if status != 'RECEIVED':
        return
    target, point = get_point(message)
    if target is not None:
        value = update_value(target, point)
        msg = u"%s scored %s (通算: %s)" % (target, point, value.point)
        LOG.debug(msg)
        message.Chat.SendMessage(msg)


# レシーバを登録
on_message.connect(receiver)
