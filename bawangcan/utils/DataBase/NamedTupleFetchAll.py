# encoding: utf-8
"""
@version: ??
@author: lizheao
@contact: lizheao940510@gmail.com
@software: PyCharm
@file: NamedTupleFetchAll.py
@time: 9:38
"""
from collections import namedtuple


def namedtuplefetchall(cursor):
    """
    Return oll rows from a cursor as a namedtuple
    """
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]
