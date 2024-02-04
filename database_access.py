from ast import Constant
from asyncio import constants
from ctypes import Union
import pandas as pd
import mysql.connector
import ray
from database_connector import DatabaseConnection

class DatabaseAccess:
    @staticmethod
    def fetch_all_records(table_name):
        '''
        This method fetches all records in table.
        '''
        try:
            connection_object = DatabaseConnection()
            if not (conn := connection_object.connect()):
                return pd.DataFrame()
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            records = cursor.fetchall()
            column_names = [i[0] for i in cursor.description]
            df = pd.DataFrame(records, columns=column_names)
            cursor.close()
            return df
        except mysql.connector.Error as e:
            print(f"Error fetching records from database: {e}")
            return pd.DataFrame()

    @staticmethod
    def get_data_length(table_name) -> int:
        '''
        This method fetches the total count of rows in table.
        '''
        try:
            connection_object = DatabaseConnection()
            if not (conn := connection_object.connect()):
                return None
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            result = cursor.fetchone()[0]
            cursor.close()
            return result
        except mysql.connector.Error as e:
            print(f"Error accessing database: {e}")
            return None

    @staticmethod
    @ray.remote
    def fetch_records(table_name,start_row, end_row) -> pd.DataFrame:
        '''
        This method fetches the rows within given range in table.
        '''
        try:
            connection_object = DatabaseConnection()
            if conn := connection_object.connect():
                cursor = conn.cursor()
                data_query = f'''SELECT * FROM (
                                    SELECT ei.*, ROW_NUMBER() OVER (ORDER BY id) AS rn
                                    FROM {table_name} ei
                                ) AS sub
                                WHERE rn >= {start_row} AND rn <= {end_row}'''
                cursor.execute(data_query)
                records = cursor.fetchall()
                column_names = [i[0] for i in cursor.description]
                df = pd.DataFrame(records, columns=column_names)
                cursor.close()
                return df
            else:
                return pd.DataFrame()
        except mysql.connector.Error as e:
            print(f"Error fetching records from database: {e}")
            return pd.DataFrame()
