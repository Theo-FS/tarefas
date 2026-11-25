from os import getenv
from pathlib import Path

import mysql.connector as mc
from dotenv import load_dotenv
from mysql.connector import Error


class Database:
    def __init__(self):
        # Localiza o .env na raiz do projeto (3 níveis acima de src/tarefas/models/database.py)
        env_path = Path(__file__).resolve().parents[3] / '.env'
        load_dotenv(dotenv_path=env_path, override=True)

        self.host = getenv('DB_HOST', 'localhost')
        self.username = getenv('DB_USER', 'root')
        self.password = getenv('DB_PASSWORD', '')
        self.database = getenv('DB_NAME', 'tarefas')
        self.port = int(getenv('DB_PORT', '3306'))
        self.connection = None
        self.cursor = None

    def conectar(self):
        try:
            self.connection = mc.connect(
                host=self.host,
                database=self.database,
                user=self.username,
                password=self.password,
                port=self.port,
                ssl_disabled=False  # Exigido pelo TiDB Cloud
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
        except Error as e:
            print(f'Erro de conexão: {e}')
            self.connection = None
            self.cursor = None

    def desconectar(self):
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def __enter__(self):
        self.conectar()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.desconectar()

    def executar(self, sql, params=None):
        if not self.connection or not self.cursor:
            return None
        try:
            self.cursor.execute(sql, params)
            if self.cursor.description:
                return self.cursor.fetchall()
            self.connection.commit()
            return self.cursor.rowcount
        except Error as e:
            print(f'Erro de execução: {e}')
            if self.connection:
                self.connection.rollback()
            return None