import os
import pymysql.cursors

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_SCHEMA = os.getenv("DB_SCHEMA")
DB_PORT = int(os.getenv("DB_PORT"))


class MySQLConnection:
    def __init__(self):
        connection = pymysql.connect(host = DB_HOST,
                                    user = DB_USER, 
                                    password = DB_PASSWORD, 
                                    db = DB_SCHEMA,
                                    port = DB_PORT,
                                    charset = 'utf8mb4',
                                    cursorclass = pymysql.cursors.DictCursor,
                                    autocommit = True)
        self.connection = connection
    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Running Query:", query)
                cursor.execute(query, data)
                if query.lower().find("insert") >= 0:
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    result = cursor.fetchall()
                    return result
                else:
                    self.connection.commit()
            finally:
                self.connection.close() 
def connectToMySQL():
    return MySQLConnection()

