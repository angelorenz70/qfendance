import mysql.connector
from datetime import datetime

class MyDatabase:
    def __init__(self, host, user, password, db_name, table_name, table_name1, table_name2) -> None:
        self.mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        self.db_name = db_name
        self.table_name = table_name
        self.table_name1 = table_name1
        self.table_name2 = table_name2
        self.mycursor = self.mydb.cursor()
        print(self.mydb)

    def initialize_database(self):
        self.mycursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_name}")
        print(f'database name: {self.db_name}')

    def initialize_tables(self):
        self.mycursor.execute(f"CREATE TABLE IF NOT EXISTS {self.db_name}.{self.table_name} (id INT AUTO_INCREMENT PRIMARY KEY, student_id VARCHAR(255), name VARCHAR(255), time_in TIME, break_out TIME, break_in TIME, time_out TIME, created_at DATETIME)")
        self.mycursor.execute(f"CREATE TABLE IF NOT EXISTS {self.db_name}.{self.table_name1} (id INT AUTO_INCREMENT PRIMARY KEY, student_id VARCHAR(255),  name VARCHAR(255), undertime DECIMAL(10,2))")
        self.mycursor.execute(f"CREATE TABLE IF NOT EXISTS {self.db_name}.{self.table_name2} (id INT AUTO_INCREMENT PRIMARY KEY, student_id VARCHAR(255),  name VARCHAR(255), undertime DECIMAL(10,2), date DATE, remarks VARCHAR(255))")
        print('-------Tables Created---------')
        print(f'table name: {self.table_name}')
        print(f'table name: {self.table_name1}')
        print(f'table name: {self.table_name2}')
    
    def insert_data(self, id, name, time_mode):
        print('ENTER INSERT DATA')
        current_time = datetime.now()
        time = current_time.time()

        # query = f"INSERT IGNORE INTO {self.db_name}.{self.table_name} (id, name, time_in, created_at) VALUES (%s, %s, %s, %s)"        
        query = f"""
                    INSERT INTO {self.db_name}.{self.table_name} (student_id, name, {time_mode}, created_at)
                    SELECT %s, %s, %s, %s
                    FROM DUAL
                    WHERE NOT EXISTS (
                        SELECT 1 FROM {self.db_name}.{self.table_name} 
                        WHERE student_id = %s AND DATE(created_at) = CURDATE()
                    )
                """
        
        self.mycursor.execute(query, (id, name, time, current_time, id))
        self.mydb.commit()

    def update_data(self, student_id, name, time_mode):
        print('ENTER UPDATE DATA FUCTION')
        current_time = datetime.now()
        time = current_time.time()
        print("TIME MODE at UPDATE DATA FUNCTION => ", time_mode)

        if not self.if_done(student_id=student_id, date=current_time.date(), time_mode=time_mode):
            print("ENTER NOT IF EXIST 1")
            # query = f"UPDATE {self.db_name}.{self.table_name} SET time_out = %s WHERE student_id LIKE %s AND name LIKE %s"
            query = f"""
                        UPDATE {self.db_name}.{self.table_name}
                        SET {time_mode} = %s
                        WHERE student_id = %s
                        AND name = %s
                        AND DATE(created_at) = CURDATE()
                    """

            self.mycursor.execute(query, (time, student_id, name))
            self.mydb.commit()
            print(self.mycursor.rowcount, "record(s) affected")
            # print(self.if_done(student_id=student_id, date=datetime.now().date()), time_mode)
            print(f'UPDATE {time_mode}')
        else:
            print("ENTER IF EXIST 1")
            # print('naabot ko dria')
            print(f'CREATE {time_mode}')
            self.insert_data(student_id, name,time_mode)


    def calculate_undertime(self, student_id, date):
        result = self.get_one_entry_attendance(student_id=student_id, date=date)
        print(result)
        if result is not None:    
            name = result[2]
            time_in = result[3]
            break_out = result[4]
            break_in = result[5]
            time_out = result[6]

            #check if there is a none in time_in, break_out, break_int then the undertime is 4hours
            if time_in != None and break_out != None and break_in != None and time_out != None:
                # Calculate work duration (time_out - break_in) + (break_out - time_in)
                morning_hours = break_out - time_in
                afternoon_hours = time_out - break_in
                total_work_time = morning_hours + afternoon_hours

                # Convert total work time to hours
                total_hours = total_work_time.total_seconds() / 3600

                # Check if it is less than 4 hours
                if round(total_hours, 2) < 4.00:
                    undertime = float(4 - total_hours)
                    undertime = round(undertime, 2)
                    
                    if_exist = self.if_exist(student_id=student_id, table=self.table_name1)                
                    if if_exist:
                        print('-------------------1')
                        # print(f'student is exist in table {self.table_name1} - {undertime}')
                        self.update_to_table_students_users(student_id=student_id, undertime=undertime)
                        self.insert_undertime_to_table(student_id=student_id, name=name, undertime=undertime, table=self.table_name2)
                    else:
                        print('-------------------2')
                        # print(f'student is not exist in table {self.table_name1}')
                        self.insert_undertime_to_table(student_id=student_id, name=name, undertime=undertime, table=self.table_name1)
                        self.insert_undertime_to_table(student_id=student_id, name=name, undertime=undertime, table=self.table_name2)
                else:
                    if_exist = self.if_exist(student_id=student_id, table=self.table_name1) 
                    print('if exist = ',if_exist )  
                    undertime = 0             
                    if if_exist:
                        print('-------------------3')
                        # print(f'student is exist in table {self.table_name1} - {undertime}')
                        self.update_to_table_students_users(student_id=student_id, undertime=undertime)
                        self.insert_undertime_to_table(student_id=student_id, name=name, undertime=undertime, table=self.table_name2)
                    else:
                        print('-------------------4')
                        # print(f'student is not exist in table {self.table_name1}')
                        self.insert_undertime_to_table(student_id=student_id, name=name, undertime=undertime, table=self.table_name1)
                        self.insert_undertime_to_table(student_id=student_id, name=name, undertime=undertime, table=self.table_name2)

            else:
                if_exist = self.if_exist(student_id=student_id, table=self.table_name1)   
                undertime = 4         
                remarks = []
                if time_in == None:
                    remarks.append('time in')
                if break_out == None:
                    remarks.append('break out')
                if break_in == None:
                    remarks.append('break in')
                remarks = ' , '.join(remarks)

                print(remarks)

                if if_exist:
                    print('-------------------5')
                    # print(f'student is exist in table {self.table_name1} - {undertime}')
                    self.update_to_table_students_users(student_id=student_id, undertime=undertime)
                    self.insert_undertime_to_table(student_id=student_id, name=name, undertime=undertime, table=self.table_name2, remarks=remarks)
                else:
                    print('-------------------6')
                    # print(f'student is not exist in table {self.table_name1}')
                    self.insert_undertime_to_table(student_id=student_id, name=name, undertime=undertime, table=self.table_name1)
                    self.insert_undertime_to_table(student_id=student_id, name=name, undertime=undertime, table=self.table_name2, remarks=remarks)

    def get_one_entry_attendance(self, student_id, date):
        print('ENTER GET ONE ENTRY ATTENDACE FUNCTION')
        # query = f'SELECT * FROM {self.db_name}.{self.table_name} WHERE student_id = {student_id} and created_at = {date}'
        query = f"""
                    SELECT * FROM {self.db_name}.{self.table_name}
                    WHERE student_id = '{student_id}' AND DATE(created_at) = '{date}'
                """
        self.mycursor.execute(query)
        result = self.mycursor.fetchone()
        # print('my query = ', query)
        # print('query result = ',result)
        return result

    def if_exist(self, student_id, table, date = None):
        if table == self.table_name:
            pass
        elif table == self.table_name1:
            student_exist = f"""
                                SELECT COUNT(*)
                                FROM {self.db_name}.{self.table_name1} 
                                WHERE student_id = '{student_id}'
                            """
            self.mycursor.execute(student_exist)
            count = self.mycursor.fetchone()
            count = count[0]
            print('if exist result => ', count)
            return count > 0

    def insert_undertime_to_table(self,student_id, name, undertime, table=None, remarks = None):
        if table == self.table_name1:
            query = f"""
                        INSERT INTO {self.db_name}.{self.table_name1} (student_id, name, undertime)
                        VALUES (%s, %s, %s)
                    """
            self.mycursor.execute(query, (student_id ,name, undertime))
            
        elif table == self.table_name2 and remarks is None:
            query = f"""
                        INSERT INTO {self.db_name}.{self.table_name2} (student_id, name, undertime, date)
                        VALUES (%s, %s, %s, %s)
                    """
            self.mycursor.execute(query, (student_id ,name, undertime, datetime.now().date()))
        else:
            query = f"""
                        INSERT INTO {self.db_name}.{self.table_name2} (student_id, name, undertime, date, remarks)
                        VALUES (%s, %s, %s, %s, %s)
                    """
            self.mycursor.execute(query, (student_id ,name, undertime, datetime.now().date(), remarks))
        self.mydb.commit()

    def update_to_table_students_users(self,student_id, undertime):
        print(f'update to table user => student_id => {student_id}, undertime => {undertime}')
        query = f"""
                    UPDATE {self.db_name}.{self.table_name1}
                    SET undertime = undertime + %s
                    WHERE student_id = %s
                """

        self.mycursor.execute(query, (undertime,student_id))
        self.mydb.commit()
        
    def if_done(self, student_id, date, time_mode):
        print('TIME MODE at IF DONE FUNCTION => ', time_mode)
        

        result = self.get_one_entry_attendance(student_id=student_id, date=date)

        print('result', result)
        print(result is not None)

        if result is not None:
            if time_mode == 'time_in':
                return result[3] is not None
            elif time_mode == 'break_out':
                return result[4] is not None
            elif time_mode == 'break_in':
                return result[5] is not None
            elif time_mode == 'time_out':
                return result[6] is not None
            
        if not self.if_exist(student_id, self.table_name1):
            print('ENTER NOT IF EXIST 2')
            return True

    def check_duplicate(self):
        pass
