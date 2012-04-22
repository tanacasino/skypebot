# -*- coding:utf-8 -*-
"""
name++
でポイントアップ

name--
でポイントダウン

+++ :  10 point
--- : -10 point

nameに使えるのは英字のみ。大文字小文字のケースは無視される。

TODO 複数行のメッセージの場合に未対応.
TODO 漢字も使いたい人がいるぽい
"""

# stblibs
import logging
import re
import threading
# thirdparty libs
from skypehub.handlers import on_message
# original libs
from models import Value

REGEX = re.compile("^([a-z]*)(\+{2,3}|-{2,3})$")
POINTS = {'++': 1, '+++': 10, '--': -1, '---': -10}

LOG = logging.getLogger('skypebot.value')
DB_LOCK = threading.Lock()


def find(body, regex):
    msg = body.lower()
    try:
        name = regex.match(msg).group(1)
        operator = regex.match(msg).group(2)
        return name, operator
    except:
        return None, None


def update_value(name, update):
    with DB_LOCK:
        value, created = Value.objects.get_or_create(name=name)
        value.point = value.point + update
        value.save()
    return value


def get_point(message):
    name, operator = find(message.Body, REGEX)
    if name is None:
        return None, 0
    return name, POINTS[operator]


def receiver(handler, message, status):
    # メッセージ受信したときのみ
    if status != 'RECEIVED':
        return
    LOG.debug(u"Recieved Message: %s" % message.Body)
    target, point = get_point(message)
    if target is not None:
        value = update_value(target, point)
        msg = u"%s scored %s (通算: %s)" % (target, point, value.point)
        LOG.debug(msg)
        message.Chat.SendMessage(msg)


# レシーバを登録
on_message.connect(receiver)
