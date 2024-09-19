import mysql.connector
from datetime import datetime

class MyDatabase:
    def __init__(self, host, user, password, db_name, table_name) -> None:
        self.mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        self.db_name = db_name
        self.table_name = table_name
        self.mycursor = self.mydb.cursor()
        print(self.mydb)

    def initialize_database(self):
        self.mycursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_name}")
        print(f'database name: {self.db_name}')

    def initialize_table(self):
        self.mycursor.execute(f"CREATE TABLE IF NOT EXISTS {self.db_name}.{self.table_name} (id VARCHAR(255) PRIMARY KEY, name VARCHAR(255), time_in TIME, time_out TIME, created_at DATETIME)")
        print(f'table name: {self.table_name}')
    
    def insert_data(self, id, name):
        current_time = datetime.now()
        time = current_time.time()

        query = f"INSERT IGNORE INTO {self.db_name}.{self.table_name} (id, name, time_in, created_at) VALUES (%s, %s, %s, %s)"

        self.mycursor.execute(query, (id, name, time, current_time))
        self.mydb.commit()
        print(id)
        print(name)
        print(time)
        print(current_time.date())
        print(current_time)

    def update_data(self, id, name):
        current_time = datetime.now()
        time = current_time.time()

        query = f"UPDATE {self.db_name}.{self.table_name} SET time_out = %s WHERE id LIKE %s AND name LIKE %s"
        self.mycursor.execute(query, (time, id, name))
        self.mydb.commit()
        print(self.mycursor.rowcount, "record(s) affected")

    def check_duplicate(self):
        pass
