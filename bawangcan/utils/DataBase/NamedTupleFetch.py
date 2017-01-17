# encoding: utf-8
"""
@version: ??
@author: lizheao
@contact: lizheao940510@gmail.com
@software: PyCharm
@file: NamedTupleFetch.py
@time: 9:38
"""
from collections import namedtuple

from django.db import connection


# settings.configure(DEBUG=True)

def namedtuplefetchall(cursor):
    """
    Return oll rows from a cursor as a namedtuple
    """
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def namedtuplefetchone(cursor):
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    row = cursor.fetchone()
    if row is None:
        return None
    return nt_result(*row)


if __name__ == '__main__':
    with connection.cursor() as cursor:
        a = cursor.execute("SELECT * FROM bawangcan_bawangcanstatus")
        b = namedtuplefetchone(cursor)
        print(b.status.count)
