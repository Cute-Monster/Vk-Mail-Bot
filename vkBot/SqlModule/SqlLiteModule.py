from vkBot.Logger.Logger import Log
import sqlite3
import hashlib


class SqlLiteModule:
    def __init__(self):
        self.log_file = Log(self.__module__)
        self.connection = sqlite3.connect("vkBot/SqlModule/bot.db")
        self.cursor = self.connection.cursor()
        self.seed = "shit"

    def check_table(self):
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
        self.cursor.execute("""
        CREATE TABLE SeenMessages(
        uid integer not null ,
        mess_text text not null 
        )
        """)
        self.connection.commit()
        self.log_file.log_all(3, f"Table SeenMessages created.")

    def add_message(self, uid, message_text):
        # print("her")
        self.cursor.execute(f"""
        INSERT INTO SeenMessages VALUES ({uid}, '{hashlib.md5(bytes(message_text + self.seed, 'utf8')).hexdigest()}');
        """)
        self.connection.commit()
        self.log_file.log_all(3, "Message added.")

    def check_for_message(self, message_text: str):
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
        self.connection = sqlite3.connect("vkBot/SqlModule/bot.db")
        self.log_file.log_all(3, "Reconnected.")

    def close_connection(self):
        self.connection.close()
        self.log_file.log_all(3, "Connection closed.")




