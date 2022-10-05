from dataclasses import dataclass
from frontend.config import Config
import mysql.connector as MySQL
from mysql.connector import errorcode
from datetime import datetime

class Data:
    cursor = None
    cnx = None

    def __init__(self):
        try:
            self.cnx = MySQL.connect(
                user=Config.DB_CONFIG["user"],
                password=Config.DB_CONFIG["password"],
                host=Config.DB_CONFIG["host"],
                database=Config.DB_CONFIG["database"]
            )
        except MySQL.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        print("DB connection success.")

        self.cursor = self.cnx.cursor()

    def add_entry(self, key, filename):
        now = datetime.now()
        fixed_now = now.strftime('%Y-%m-%d %H:%M:%S')

        query = """
                INSERT INTO `pairs` (`key`,`filename`,`upload_time`)
                VALUES ("{}", "{}", "{}");
                """.format(key, filename, fixed_now)

        print(query)

        self.cursor.execute(query)
        self.cnx.commit()
        
    def inspect_all_entries(self):
        query = """
                SELECT * FROM `pairs`;
                """
        self.cursor.execute(query)
        data = self.cursor.fetchall()

        # print(data)
        return data

    def search_key(self, key):
        query = """
                SELECT * FROM `pairs` WHERE `key`="{}";
                """.format(key)

        self.cursor.execute(query)
        data = self.cursor.fetchall()

        print("searched data :", data)
        return data