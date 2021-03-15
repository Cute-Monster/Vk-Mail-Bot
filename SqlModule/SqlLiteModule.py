from os.path import abspath
from os import getenv
from Logger.Logger import Log
import sqlite3
import hashlib
import sentry_sdk

sentry_sdk.init(
    "https://eca61270fe5e4ceeb1046ad58ad7333e@o402810.ingest.sentry.io/5264523"
)


class SqlLiteModule:
    def __init__(self):
        self.log_file = Log(self.__class__)
        self.path_to_db = abspath("db/bot.db")
        self.connection = sqlite3.connect(self.path_to_db)
        self.cursor = self.connection.cursor()
        self.seed = getenv("DB_Seed")

    def check_table(self):
        """
        Check if Table SeenMessages exists
        :return:
        """

        self.cursor.execute(
            f"""
        SELECT EXISTS(
            SELECT name FROM sqlite_master WHERE type='table' AND name='SeenMessages'
        ) 
        """
        )
        result = self.cursor.fetchone()
        if not result[0]:
            self.create_table()
        else:
            self.log_file.log_all(3, "Table exists.")

    def create_table(self):
        """
        Creates the table SeenMessages
        :return:
        """

        self.cursor.execute(
            """
        CREATE TABLE SeenMessages(
            uid integer not null ,
            mess_text text not null 
        )
        """
        )
        self.connection.commit()
        self.log_file.log_all(3, "Table SeenMessages created.")

    def add_message(self, uid, message_text):
        # type: (int, str) -> None
        """
        Adds the message uid and text to table
        :param uid: Uid of the message
        :param message_text: Text of the message
        :return:
        """

        self.cursor.execute(
            f"""
        INSERT INTO SeenMessages 
        VALUES
            ({uid}, '{hashlib.md5(
            bytes(message_text + self.seed, 'utf8')
        ).hexdigest()}');
        """
        )
        self.connection.commit()
        self.log_file.log_all(3, "Message added.")

    def check_for_message(self, message_text):
        # type: (str) -> int
        """
        Check if message exists in the database
        :param message_text:
        :return:
        """

        self.cursor.execute(
            f"""
            SELECT EXISTS(
                    SELECT mess_text FROM SeenMessages 
                    WHERE mess_text = '{hashlib.md5(bytes(message_text + self.seed, 'utf8')).hexdigest()}')
        """
        )
        result: int = self.cursor.fetchone()[0]
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
