import sqlite3

# function replaced with sqlite3.Row
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# TODO make a basic method to get data from the message table
class Baza:
    def __init__(self, db_file = 'data.db', create_tables = False):
        print('init db')
        self.con = sqlite3.connect(db_file)
        self.cur_none = self.con.cursor()
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()

        if create_tables:
            self.cur.execute('''CREATE TABLE IF NOT EXISTS messages (
                id INTEGER,
                channel_id INTEGER,
                message TEXT,
                timestamp TEXT,
                UNIQUE(id, channel_id)
            )''')
            # TODO create table alert with toponymy, message id and id
            self.cur.execute('''CREATE TABLE IF NOT EXISTS channels (
                channel_id INTEGER PRIMARY KEY,
                city TEXT,
                channel_name TEXT,
                latest_readed INTEGER
            )''')
            self.cur.execute('''CREATE TABLE IF NOT EXISTS dictionary (
                id INTEGER PRIMARY KEY,
                word TEXT,
                type TEXT
            )''')

    # replaced with ini file
    def get_configuration(self, config_name):
        print('get configuration')
        self.cur.execute('SELECT api_id, api_hash FROM configuration WHERE name = ?', (config_name,))
        return self.cur.fetchone()

    def insert_message(self, message_id, channel_id, message, timestamp):
        self.cur.execute('''INSERT OR IGNORE INTO messages (id, channel_id, message, timestamp) VALUES(?, ?, ?, ?)''', (message_id, channel_id, message, timestamp))
        self.con.commit()

    def insert_channel(self, id, city, title):
        self.cur.execute('''INSERT OR IGNORE INTO channels(channel_id, city, channel_name) VALUES(?, ?, ?)''', (id, city, title))
        self.con.commit()

    def get_cursor(self, raw = True):
        return self.cur if raw else self.cur_none

    def get_message(self):
        pass

    def get_channels(self, city = ''):
        if city != '':
            self.cur.execute('''SELECT channel_id, city FROM channels WHERE city = ?''', (city, ))
            return self.cur.fetchone()
        else:
            self.cur.execute('''SELECT channel_id, city FROM channels''')
            return self.cur.fetchall()

    def commit(self):
        self.con.commit()

    def close(self):
        self.con.close()


# main block used only for development purpose
if __name__ == '__main__':
    db = Baza()
    cur = db.get_cursor()
    cur.execute('''select * from messages''')
    print(cur.fetchall())
    cur.execute('select api_id, api_hash, comment from configuration where name = ?', ('pars2022',))
    config = cur.fetchone()
    print(config.keys())
    print(config['comment'])
    def t_norm(x):
        d = dict()
        for i in x.keys():
            d[i] = x[i]
        return d
    cur.execute('SELECT name, type FROM sqlite_master')
    tables = cur.fetchall()
    t_mapped = list(map(t_norm, tables))
    print(t_mapped)
    db.close()
