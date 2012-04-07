# -*- coding:utf-8 -*-

from django.db import models


class Value(models.Model):
    """
    ++
    --
    で評価を管理する
    """
    name = models.CharField(primary_key=True, max_length=30)
    point = models.IntegerField(default=0)

    def __unicode__(self):
        return u"Value: name=%s point=%s" % (self.name, self.point)
