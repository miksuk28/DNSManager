import sqlite3
import config
from contextlib import contextmanager
from uuid import uuid4

class DatabaseConnection:
    def __init__(self):
        self._db_file = config.MANAGER_DB_PATH
        self._conn =    sqlite3.connect(self._db_file, check_same_thread=False)
        # enable primary key constraint, as the default in SQLite is OFF
        self._conn.execute("PRAGMA foreign_keys=ON")
        self._conn.row_factory = sqlite3.Row


    def genid(self):
        return str(uuid4())


    @contextmanager
    def cur(self, commit=True):
        _cur = self._conn.cursor()
        try:
            yield _cur
            if commit:
                self._conn.commit()

        except Exception as e:
            self._conn.rollback()
            print("Re-raising exception within DB manager")
            raise(e)

        finally:
            _cur.close()

    def rows_to_dict(self, obj):
        new_list = []
        for item in obj:
            new_list.append(dict(item))

        return new_list