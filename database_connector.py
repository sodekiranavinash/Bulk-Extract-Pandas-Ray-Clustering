from asyncio import constants
import mysql.connector
import os
from constants import constants


class DatabaseConnection:
    def __init__(self):
        self.host = constants.DB_HOST
        self.user = constants.DB_USER
        self.password = constants.DB_PASSWORD
        self.database = constants.DB_NAME
        self.conn = None

    def connect(self):
        '''
        This method establishes connection returns con object.
        '''
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return self.conn
        except mysql.connector.Error as e:
            print(f"Error connecting to the database: {e}")
            return None

    def close(self):
        '''
        This method acts as wrapper for closing connection.
        '''
        if self.conn:
            self.conn.close()
