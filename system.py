import time,random
from datetime import date

from login import Login


class Session:
    def __init__(self,log):
        self.start_time = time.time()
        self.date = str(date.today())
        self.end_time = None
        self.duration = "NULL"
        self.log = log
        self.session_id = self.__generate()
        self.insert()

    def __generate(self):
        data = self.log.cursor.execute("select sid from sessions ORDER BY sid ").fetchall()
        sess_id = data[len(data)-1][0]+1
        return sess_id

    def insert(self):
        query = "insert into sessions values (:sid, :cid, :date, :dur);"
        self.log.cursor.execute(query,{'sid': self.session_id,'cid':self.log.id,'date':self.date,'dur':self.duration})
        self.log.conn.commit()

    def end_session(self):
        self.end_time = time.time()
        self.duration = (self.end_time - self.start_time)//60.0
        query = "UPDATE sessions set duration = :dur where sid = :sid"
        self.log.cursor.execute(query,{'dur':self.duration,'sid':self.session_id})
        self.log.conn.commit()




class System:
    def __init__(self,log:Login):
        self.log = log
        self.session = None

    def start_session(self):
        self.session = Session(self.log)

    def end_session(self):
        # TODO: end movies and add to session duration
        self.session.end_session()

if __name__ == '__main__':
    l1 = Login("c100","cmput291","./mini-proj.db")
    l1.login()
    s1 = System(l1)
    s1.start_session()
    time.sleep(120)
    s1.end_session()
