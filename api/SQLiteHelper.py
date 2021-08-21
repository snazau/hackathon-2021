from __future__ import absolute_import, division, print_function, unicode_literals

import sqlite3
import datetime
from threading import Lock

__version__ = "0.1.0"

list_hs_ids = """
    SELECT *
    FROM hs
"""

list_transactions_by_id = """
    SELECT *
    FROM hs
    WHERE HsId = QUERY_NAME;
"""

lock = Lock()


class SQLiteHelper:
    def __init__(self, db='app.db'):
        self.db = db

    def get_time(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def list_hs_ids(self):
        lock.acquire()
        try:
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()
            cursor.execute(list_hs_ids)

            rows = cursor.fetchall()

            ids = list(set([row[0] for row in rows]))
            return ids

        finally:
            lock.release()

    def get_transactions_by_id(self, hs_id):
        lock.acquire()
        try:
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()
            cursor.execute(list_transactions_by_id.replace("QUERY_NAME", '"' + str(hs_id) + '"'))

            rows = cursor.fetchall()
            transaction_ids = list(set([row[1] for row in rows]))

            return transaction_ids

        finally:
            lock.release()


if __name__ == '__main__':
    db_helper = SQLiteHelper(db="./app.db")
    ids = db_helper.list_hs_ids()
    transactions = db_helper.get_transactions_by_id(ids[0])
    print("ids", ids)
    print("transactions", transactions)
