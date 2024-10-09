# select * from kalahi_2021.emp_attendance ea 
import mysql.connector
from datetime import datetime
import os
import cv2

class DbConnection:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host=os.getenv('DB_HOST'),  # Get host from .env
            user=os.getenv('DB_USER'),  # Get user from .env
            password=os.getenv('DB_PASSWORD')  # Get password from .env
        )
        self.mycursor = self.mydb.cursor()

    def insert(self, data, frame):
        print('mode => ', data[0])
        print('id => ', data[1])
        print('time => ', data[2])
        print('created_at => ', data[3])

        user_done = f"""
                            SELECT *
                            FROM kalahi_2021.emp_attendance ea 
                            WHERE ea.id_number = '{data[1]}' 
                            AND DATE(ea.created_at) = '{data[3].date()}';
                        """
        

        self.mycursor.execute(user_done)
        result = self.mycursor.fetchone()
        if result is not None:
            print(f"result entry = ", result)
            print('has result')
            time_mode_done = f"""
                                SELECT ea.{data[0]} 
                                FROM kalahi_2021.emp_attendance ea 
                                WHERE ea.id_number = '{data[1]}' 
                                AND DATE(ea.created_at) = '{data[3].date()}';
                            """
            self.mycursor.execute(time_mode_done)
            result = self.mycursor.fetchone()
            print(f"result entry time = ", result)
            if result is None or result[0] is None:
                print('----> no timde_mode')
                picture_path = self.save_picture(data[1], data[0], frame)
                query = f"""
                    update kalahi_2021.emp_attendance ea
                    set ea.{data[0]} = %s, ea.picture_path_{data[0]} = %s
                    where ea.id_number = %s
                """
                self.mycursor.execute(query, (data[2], picture_path, data[1]))
                result = self.mydb.commit()
            else:
                print('------> already time_mode')

        else:
            print('no user done')
            picture_path = self.save_picture(data[1], data[0], frame)
            query = f"""
                        INSERT IGNORE INTO kalahi_2021.emp_attendance (id_number , {data[0]}, created_at, picture_path_{data[0]}) 
                        VALUES (%s, %s,%s, %s)
                    """
            self.mycursor.execute(query, (data[1], data[2], data[3], picture_path))
            self.mydb.commit()
#         INSERT INTO kalahi_2021.emp_attndance (id_number , check_in , break_out, break_in, check_out , created_at) 
# VALUES ('11-111111', '08:00:00', '12:00:00', '13:00:00', '24:00:00', '2024-10-08 15:16:52')
    def fetch_latest_entries(self, limit=5):
        limit_5_attendes = f'select * from kalahi_2021.emp_attendance ea order by ea.created_at desc  limit {limit}'
        self.mycursor.execute(limit_5_attendes)
        result = self.mycursor.fetchall()
        return result
    
    def save_picture(self,id_number,time_mode, frame):
        # Ensure the 'pictures' directory exists
        folder_path = f'app_attendance_pictures/{datetime.now().date()}/{time_mode}'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        #Create a unique file name with a timestamp
        file_name = f'{folder_path}/{id_number},{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'

        # Save the current frame as a PNG file
        cv2.imwrite(file_name, frame)
        print(f'Frame saved as {file_name}')
        return file_name
        


    