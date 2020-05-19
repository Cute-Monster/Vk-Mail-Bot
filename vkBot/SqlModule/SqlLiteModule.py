from os.path import abspath
from vkBot.Logger.Logger import Log
import sqlite3
import hashlib


class SqlLiteModule:
    def __init__(self):
        self.log_file = Log(self.__module__)
        self.path_to_db = abspath("vkBot/SqlModule/bot.db")
        self.connection = sqlite3.connect(self.path_to_db)
        self.cursor = self.connection.cursor()
        self.seed = "shit"

    def check_table(self):
        """
        Check if Table SeenMessages exists
        :return:
        """
        # print("test")
        self.cursor.execute(f"""
        SELECT EXISTS(SELECT name FROM sqlite_master WHERE type='table' AND name='SeenMessages') 
        """)
        result = self.cursor.fetchone()
        if result[0] == 0:
            self.create_table()
        else:
            self.log_file.log_all(3, "Table exists.")

    def create_table(self):
        """
        Creates the table SeenMessages
        :return:
        """
        self.cursor.execute("""
        CREATE TABLE SeenMessages(
        uid integer not null ,
        mess_text text not null 
        )
        """)
        self.connection.commit()
        self.log_file.log_all(3, f"Table SeenMessages created.")

    def add_message(self, uid: int, message_text: str):
        """
        Adds the message uid and text to table
        :param uid:
        :param message_text:
        :return:
        """
        # print("her")
        self.cursor.execute(f"""
        INSERT INTO SeenMessages VALUES ({uid}, '{hashlib.md5(bytes(message_text + self.seed, 'utf8')).hexdigest()}');
        """)
        self.connection.commit()
        self.log_file.log_all(3, "Message added.")

    def check_for_message(self, message_text: str):
        """
        Check if message exists in the database
        :param message_text:
        :return:
        """
        # print("hui")
        self.cursor.execute(f"""
            SELECT EXISTS(
                    SELECT mess_text FROM SeenMessages 
                    WHERE mess_text = '{hashlib.md5(bytes(message_text + self.seed, 'utf8')).hexdigest()}')
        """)
        result = self.cursor.fetchone()
        # print("HUI: ", result)
        return result

    def reconnect(self):
        """
        Reconnect to database
        :return:
        """
        self.connection = sqlite3.connect(self.path_to_db)
        self.cursor = self.connection.cursor()
        self.log_file.log_all(3, "Reconnected to database.")

    def close_connection(self):
        """
        Closing connection to database
        :return:
        """
        self.cursor.close()
        self.log_file.log_all(3, "Connection to database closed.")
