import vk_api
from vk_api.utils import get_random_id
# from ImapClient import ImapClient
# from Logger import Log
# from SqlLiteModule import SqlLiteModule
from vkBot.Logger.Logger import Log
from vkBot.ImapClient.ImapClient import ImapClient
from vkBot.SqlModule.SqlLiteModule import SqlLiteModule


class VkNotifier:
    def __init__(self, login_method: int, chat_to_send: int, send_only_to_dev: bool):
        self.user_login = ""
        self.user_password = ""
        self.token = '1e415cfb00820bd2be0c44ce3085998e5d73b441fa68cc0edbe152ae5b3babc75f043ca93e441ea7bc52d'
        self.vk_session = None
        self.vk = None
        (self.login_throw_user() if login_method == 2 else self.login_throw_group())
        self.sleep_time = int(15)
        self.dev_vk_id = "198253590"
        self.send_only_to_dev = send_only_to_dev
        self.group_chat_ids = {1: 1,
                               2: 3}  # Mr.Robot -> 1, Test -> 3
        self.group_chat_id = self.group_chat_ids.get(chat_to_send)
        self.log_file = Log(self.__module__)
        self.mail_client = ImapClient()
        self.new_inbox_email = []
        self.counter = 0
        self.db = SqlLiteModule()
        self.db.check_table()

    def check_for_new_messages(self):
        """
        Checking the mailbox for new messages. If found unseen for the bot,
        then notify chat and dev about this message by sending message text of unseen message
        and adding it to the database
        :return:
        """
        new_messages_sent = False
        self.new_inbox_email = self.mail_client.get_array_of_messages_to_send()
        self.new_inbox_email.reverse()
        if not self.new_inbox_email:
            self.no_new_messages()
        else:
            for uid, message_text in self.new_inbox_email:
                # print(f"uid : {uid} : in seen {uid in self.seen_emails_uid}")
                if self.db.check_for_message(message_text)[0] == 0:
                    self.notify(message_text)
                    self.db.add_message(uid, message_text)
                    new_messages_sent = True
            if new_messages_sent:
                self.log_file.log_all(3, "Found unseen messages")
                self.notify("Filter the INBOX folder please ;-)")
                self.counter = 0
            else:
                self.no_new_messages()

    def no_new_messages(self):
        """
        Log and send a message to dev if no new messages have been found
        :return:
        """
        self.counter += 1
        self.log_file.log_all(3, "No unseen messages")
        if self.counter == 6:
            self.counter = 0
            self.send_message_to_dev("No unseen messages\nGoing to sleep :-(")

    def notify(self, text):
        """
        Sending a message to selected chat and dev
        :param text: message text
        :return:
        """
        if not self.send_only_to_dev:
            self.send_message_to_chat(text)

        self.send_message_to_dev(text)

    def login_throw_user(self):
        """
        Login to vk throw user account
        :return:
        """
        self.vk_session = vk_api.VkApi(self.user_login, self.user_password)
        try:
            self.vk = self.vk_session.auth(token_only=True)
        except vk_api.AuthError as error_msg:
            self.log_file.log_all(1, error_msg)

    def login_throw_group(self):
        """
        Login to vk through group bot token
        :return:
        """
        self.vk_session = vk_api.VkApi(token=self.token, scope='messages')
        self.vk = self.vk_session.get_api()

    def send_message_to_dev(self, text):
        """
        Sending message to dev
        :param text: message text
        :return:
        """
        self.vk.messages.send(
            user_id=self.dev_vk_id,
            random_id=get_random_id(),
            message=text
        )

    def send_message_to_chat(self, text):
        """
        Sending message to selected chat
        :param text: message text
        :return:
        """
        self.vk.messages.send(
            peer_id='200000000{}'.format(self.group_chat_id),
            random_id=get_random_id(),
            message=text
        )
