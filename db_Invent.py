import sqlite3


class Database:
    """docstring for Database"""

    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS items(id INTEGER PRIMARY KEY, item text, quantity text, "
            "description text, price text)")
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM items")
        rows = self.cur.fetchall()
        return rows

    def insert(self, item, quantity, description, price):
        self.cur.execute("INSERT INTO items VALUES(NULL, ?, ?, ?, ?)", (item, quantity, description, price))
        self.conn.commit()

    def remove(self, id):
        self.cur.execute("DELETE FROM items WHERE id=?", (id,))
        self.conn.commit()

    def update(self, id, item, quantity, description, price):
        self.cur.execute("UPDATE items SET item=?, quantity=?, description=?, price=? WHERE id=?",
                         (item, quantity, description, price, id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()


class Data:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS counts(id INTEGER PRIMARY KEY, count text)")
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM counts")
        rows = self.cur.fetchall()
        return rows

    def insert(self, count):
        self.cur.execute("INSERT INTO counts VALUES(NULL, ?)", count,)
        self.conn.commit()

    def update(self, id, count):
        self.cur.execute("UPDATE counts SET count=? WHERE id=?", count,)
        self.conn.commit()

    def __del__(self):
        self.conn.close()
