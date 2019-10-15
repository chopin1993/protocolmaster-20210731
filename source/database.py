#encoding:utf-8
import os
import sqlite3
import datetime


class EsDatabase(object):
    def __init__(self,name):
        self.name = name
        self.conn = sqlite3.connect(name)
        self.create_table()
        self.idx = 0

    def create_table(self):
        sql = 'CREATE TABLE IF NOT EXISTS thermal_table (idx int,desciption varchar(20),tag varchar(20),data BLOB,img BLOB,save_date date)'
        cursor = self.conn.cursor()
        cursor.execute(sql)

    def append_sample(self, idx, description, tag, data, img):
        cursor = self.conn.cursor()
        time_str = str(datetime.datetime.now())
        cursor.execute("insert into thermal_table values(?,?,?,?,?,?)",
                       (idx, description, tag, sqlite3.Binary(data), sqlite3.Binary(img),time_str))
        self.conn.commit()

    def get_sample_images(self):
        cursor = self.conn.cursor()
        sql = 'select * from thermal_table'
        cursor.execute(sql)
        while True:
            values = cursor.fetchone()
            if None == values:
                break
            yield values
        cursor.close()

    def __del__(self):
        self.conn.close()





