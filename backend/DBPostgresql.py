import psycopg2

class DBPostgresql:
    db = "postgres"
    user = "postgres"
    passwd = "buwangchuxin"
    host = "127.0.0.1"
    port = "5432"
    conn = None
    cur = None

    def connects(self):
        try:
            self.conn = psycopg2.connect(database=self.db, user=self.user, password=self.passwd, host=self.host,
                                         port=self.port)
        except:
            print("connect database failed")
        else:
            print("database connected")

    def getcursor(self):
        if self.conn is None:
            print("not connected")
            return
        self.cur = self.conn.cursor()

    def execcteSelectSQL(self,sqlstmt):
        if self.cur is None:
            print("not connected")
            return
        self.cur.execute(sqlstmt)
        res = self.cur.fetchall()
        print(res)
        return (res)

    def execcteCUDSQL(self,sqlstmt):
        if self.cur is None:
            print("not connected")
            return
        self.cur.execute(sqlstmt)
        # print("success")

    def commit(self):
        if self.conn is None:
            print("not connected")
            return
        self.conn.commit()

    def close(self):
        if self.conn is None:
            print("not connected")
            return
        self.conn.close()

db = DBPostgresql()
db.connects()
db.getcursor()

if __name__ == '__main__':
    db = DBPostgresql()
    db.connects()
    db.getcursor()
    db.execcteSelectSQL("select * from f_inc_fin('2019-05-31','2019-06-21')")
    db.commit()
    db.close()
