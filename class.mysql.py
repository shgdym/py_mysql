#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pymysql
from const import const

__author__ = 'shgdym'

class MySql:
    def __init__(self, host=const.DB_HOST, user=const.DB_USER, password=const.DB_PASS, db=const.DB_NAME, port=const.DB_PORT):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.port = port
        self.cache = []
        self.connect()

    def connect(self):
        if 'cursor' in locals().keys():
            pass
        else:
            self.dbconn = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db, port=self.port, charset='utf8mb4')
            self.cursor = self.dbconn.cursor()

    def getRows(self, query_sql):
        self.cursor.execute(query_sql)
        results = self.cursor.fetchall()
        return results

    def getFirstRow(self, query_sql):
        res = self.getRows(query_sql)
        if len(res) == 0:
            return ""
        return res[0]

    def getFirstRowColumn(self, query_sql):
        row = self.getFirstRow(query_sql)
        if row == "":
            return ""
        return row[0]

    def query(self, query_sql):
        try:
            self.cursor.execute(query_sql)
            self.dbconn.commit()
        except:

            filename = 'test_text.txt'
            with open(filename, 'a') as file_object:
                file_object.write(query_sql)
    def isTableExists(self, table_name):
        if table_name in self.cache:
            return True
        sql = "SHOW TABLES LIKE '"+table_name+"'"
        t = self.getFirstRow(sql)
        if t:
            self.cache.append(t[0])
            return True
        return False
    
    def getCreateTableSql(self, table_name):
        sql = "SHOW CREATE TABLE `"+table_name+"`"
        first_row = self.getFirstRow(sql)
        return first_row[1]
    
    def duplicateTable(self, default_tb, new_tb):
        create_sql = self.getCreateTableSql(default_tb)
        search_text = "CREATE TABLE `"+default_tb+"`"

        if search_text not in create_sql:
            import sys
            try:
                sys.exit(0)
            except:
                print('die')
        new_str = "CREATE TABLE `"+ new_tb +"`"
        self.query(create_sql.replace(search_text, new_str, 1))

				
    def close(self):
        self.cursor.close()
