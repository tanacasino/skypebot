# -*- coding:utf-8 -*-
"""
#katsuo on
で土佐弁講座を定期的につぶやく
#katsuo off
で土佐弁講座を終了する
"""

# stblibs
import logging
import random
from time import time
import threading
# thirdparty libs
from django.conf import settings
from skypehub.handlers import on_message, on_time
# original libs
from models import KatsuoRoom


# TODO DBでマスタデータ管理すべし
KATSUO_MESSAGES = [
        u"これがSkypeかえ(これがSkypeですか？)",
        u"まっことようできちゅう(本当によくできてる)",
        u"ちゃがまったがやけど(壊れましたけど)",
        u"そんなんゆうたちいかんちや(そんなこと言ってもだめだよ)",
        u"ことうたちや(疲れた)",
        u"こじゃんとうまい！(すごくおいしい)",
        u"しっちゅうよ(知ってるよ)",
        u"やりゆうよー(やってるよ)",
        u"しらんちや(知らないよ)",
        u"何しゆうが？(何してるの？)",
        u"おれ金ないきにゃあ(俺お金ないからなぁ)",
        u"なんなが？(何？)",
        u"めっちゃむかつくがやけど(すごくむかつくんですけど)",
        u"わりことしの顔しちゅうな(いたずらっ子の顔をしてるね)",
        u"ようせんちや(そんなことできません)",
        ]

POLL_INTERVAL = getattr(settings, 'SKYPE_KATSUO_POLL_INTERVAL', 60)
LOG = logging.getLogger('skypebot.katsuo')

DB_LOCK = threading.Lock()


def random_select():
    index = random.randint(0, len(KATSUO_MESSAGES) - 1)
    return KATSUO_MESSAGES[index]


def receiver(handler, message, status):
    LOG.debug(u"Received Message: %s %s " % (message, status))
    LOG.debug(u"Chat.Name=%s" % message.Chat.Name)
    # NOTE Chat.Name は チャットルームの名前
    # メッセージ受信したときのみ
    if status != 'RECEIVED':
        return
    body = message.Body.lower()
    if "#katsuo on" in body:  # TODO 正規表現でやりたい
        with DB_LOCK:
            room, created = KatsuoRoom.objects.get_or_create(
                                                   name=message.Chat.Name)
            if room.enable:
                LOG.debug(u"すでに開始されている。Room=%s", message.Chat.Name)
                return
            room.enable = True
            room.save()
        LOG.debug(room)
        LOG.debug(u"土佐弁講座を開始します。Room=%s" % message.Chat.Name)
        # NOTE メッセージの名前
        message.Chat.SendMessage(u"土佐弁講座を開始します。")
    elif "#katsuo off" in body:
        with DB_LOCK:
            room, created = KatsuoRoom.objects.get_or_create(
                                                   name=message.Chat.Name)
            if room.enable:
                room.enable = False
                room.save()
            else:
                LOG.debug(u"すでに終了している。Room=%s", message.Chat.Name)
                return
        LOG.debug(room)
        LOG.debug(u"土佐弁講座を終了します。Room=%s", message.Chat.Name)
        message.Chat.SendMessage(u"土佐弁講座を終了します。")


def on_time_handler(handler, time):
    try:
        rooms = KatsuoRoom.objects.filter(enable=True)
        if not rooms:
            LOG.debug("No rooms")
            return
        msg = random_select()
        LOG.debug("select message %s", msg)
        for room in rooms:
            LOG.debug(u"土佐弁講座 : Room=%s", room)
            handler.skype.Chat(room.name).SendMessage(u"土佐弁講座\n%s" % msg)
    except Exception as e:
        LOG.error(e)
    finally:
        handler.connect(on_time_handler, time + POLL_INTERVAL)


# レシーバを登録
on_message.connect(receiver)
on_time.connect(on_time_handler, time() + 5)  # 5秒後の時刻に動作するように設定
