import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    def __init__(self):
        self.host = 'localhost'
        self.database = 'Piscis'
        self.user = 'piscis_user'
        self.password = 'Piscis@2026'

    def get_connection(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            return connection
        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")
            return None
