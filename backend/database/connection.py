import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    def __init__(self):
        # Em um projeto real, escondemos isso em um arquivo .env depois!
        self.host = 'localhost'
        self.database = 'nome_do_seu_banco' # Ex: piscis_db
        self.user = 'root'
        self.password = 'sua_senha_do_mysql'

    def get_connection(self):
        """Abre a porta com o banco de dados e retorna a conexão."""
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