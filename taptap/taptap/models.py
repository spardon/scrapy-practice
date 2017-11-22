#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
from config import MONGO_URI
from mongokit import Connection, Document

mongo = Connection(MONGO_URI)


@mongo.register
class TaptapAppData(Document):
    """
        app 相关信息
    """
    __collection__ = 'taptap_data'
    __database__ = 'app_data'

    structure = {
        'name': basestring,
        'produce': basestring,
        'kind': basestring,
        'rating': basestring,
        'lables': list,
        'rank_kind': basestring,
        'created_at': datetime.datetime,
        'updated_at': datetime.datetime
    }

    indexes = [
        {'fields': 'name'},
        {'fields': 'rating'}
    ]


TaptapModel = mongo.TaptapAppData
