from backend.config import Config
import mysql.connector as MySQL
from datetime import datetime
from mysql.connector import errorcode


class Data:
    cursor = None
    cnx = None

    def __init__(self):
        try:
            #connect to database
            self.cnx = MySQL.connect(
                user = Config.DB_CONFIG["user"],
                password = Config.DB_CONFIG["password"],
                host = Config.DB_CONFIG["host"],
                database = Config.DB_CONFIG["database"]
            )
        except MySQL.Error as err:
            #add database error code
            if err.errno == errocode.ER_ACCESS_DENIED_ERROR:
                print("Something wrong with user name and password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        
        #initialize cursor of database
        self.cursor = self.cnx.cursor()

        print("Backend DB Connection Success.")

    #get the data from the configuration table
    def get_config_data(self):
        #select the latest configuraiton from the database
        query = """
                SELECT * FROM configuration WHERE id = (
                    SELECT MAX(id) From configuration
                )
                """
        self.cursor.execute(query)
        print("Query Executed")
        data = self.cursor.fetchall()
        return data
    
    #insert into the configuration database
    #capacity: the capacity of the memcache
    #policy: 0 for Random Replacement, 1 for Least Recently Used
    def insert_config_data(self,capacity,policy):

        query = """
                INSERT INTO `configuration` (`capacity`,`replacePolicy`)
                VALUES("{}","{}");
        """.format(capacity,policy)

        self.cursor.execute(query)
        self.cnx.commit()
        












    
        
    


        