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
        self.mycursor.execute(f"CREATE TABLE IF NOT EXISTS {self.db_name}.{self.table_name} (id INT AUTO_INCREMENT PRIMARY KEY, student_id VARCHAR(255), name VARCHAR(255), time_in TIME, break_out TIME, break_in TIME, time_out TIME, created_at DATETIME)")
        print(f'table name: {self.table_name}')
    
    def insert_data(self, id, name):
        current_time = datetime.now()
        time = current_time.time()

        # query = f"INSERT IGNORE INTO {self.db_name}.{self.table_name} (id, name, time_in, created_at) VALUES (%s, %s, %s, %s)"        
        query = f"""
                    INSERT INTO {self.db_name}.{self.table_name} (student_id, name, time_in, created_at)
                    SELECT %s, %s, %s, %s
                    FROM DUAL
                    WHERE NOT EXISTS (
                        SELECT 1 FROM {self.db_name}.{self.table_name} 
                        WHERE student_id = %s AND DATE(created_at) = CURDATE()
                    )
                """



        self.mycursor.execute(query, (id, name, time, current_time, id))
        self.mydb.commit()
        print(id)
        print(name)
        print(time)
        print(current_time.date())
        print(current_time)

    def update_data(self, id, name, time_mode):
        current_time = datetime.now()
        time = current_time.time()

        # query = f"UPDATE {self.db_name}.{self.table_name} SET time_out = %s WHERE student_id LIKE %s AND name LIKE %s"
        query = f"""
                    UPDATE {self.db_name}.{self.table_name}
                    SET {time_mode} = %s
                    WHERE student_id = %s
                    AND name = %s
                    AND DATE(created_at) = CURDATE()
                """

        self.mycursor.execute(query, (time, id, name))
        self.mydb.commit()
        print(self.mycursor.rowcount, "record(s) affected")

    def check_duplicate(self):
        pass
