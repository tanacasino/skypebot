# -*- coding:utf-8 -*-

from django.db import models


class KatsuoRoom(models.Model):
    """
    土佐弁講座をするチャットルームをDBで管理するためのモデル
    """
    name = models.CharField(primary_key=True, max_length=1000)
    enable = models.BooleanField(default=False)

    def __unicode__(self):
        return u"KatsuoRoom: name=%s enable=%s" % (self.name, self.enable)
