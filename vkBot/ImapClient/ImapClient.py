import imapclient
import pyzmail
# from Logger import Log
from vkBot.Logger.Logger import Log

class ImapClient:
    def __init__(self):
        self.imap_link = 'imap.gmail.com'
        # self.mail_login = 'runtov.constantin@gmail.com'
        # self.mail_password = '4apFMCRyB8a4pTD'
        self.mail_login = 'gruppa1802@gmail.com'
        self.mail_password = '01012019'
        self.server = imapclient.IMAPClient(self.imap_link)
        self.login_to_mailbox()
        self.new_messages = None
        self.list_of_seen_uids = []
        self.final_list_to_send = []
        self.log_file = Log(self.__module__)
        self.select_inbox_folder()

    def login_to_mailbox(self):
        """
        Login to the mailbox
        :return:
        """
        self.server.login(self.mail_login, self.mail_password)

    def logout_from_mailbox(self):
        self.server.logout()

    def logout(self):
        self.server.logout()

    def select_inbox_folder(self):
        """
        Selecting folder with a name 'INBOX'
        :return:
        """
        self.server.select_folder('INBOX', readonly=True)

    def get_all_messages(self):
        """
        Fetch,parse and add the parsed message with his (uid, email_info) to list of messages from a selected folder
        :return:
        """
        self.final_list_to_send.clear()
        try:
            self.new_messages = self.server.search(['All'])
            # print(self.new_messages, sep="\n")
            for uid, msg in self.server.fetch(self.new_messages, 'RFC822').items():
                parsed_message = pyzmail.PyzMessage.factory(msg[b'RFC822'])  # Be sure to change the uid num
                final_mail_inf = "You Have A New Email In The Mailbox:\n" \
                                 "From: {} <{}>\n" \
                                 "Subject: {}\n" \
                                 "Text: \n{}".format(parsed_message.get_address('From')[0],
                                                     parsed_message.get_address('From')[1],
                                                     parsed_message.get_subject(),
                                                     parsed_message.text_part.get_payload().decode(
                                                         parsed_message.text_part.charset))
                # print(uid)
                self.final_list_to_send.append((uid, final_mail_inf))
        except imapclient.IMAPClient.Error as imap_error:
            self.log_file.log_all(1, str(imap_error))
            # self.server = imapclient.IMAPClient(self.imap_link)
            self.reconnect()
            self.get_all_messages()

    def is_in_list_of_seen(self, value) -> bool:
        for uid in self.list_of_seen_uids:
            if uid == value:
                return True
        return False

    def reconnect(self):
        """
        Reconnect to mailbox using known host,username and password
        :return:
        """
        try:
            self.server = imapclient.IMAPClient(self.imap_link)
            self.login_to_mailbox()
            self.select_inbox_folder()
            self.log_file.log_all(3, "Successfully reconnected.")
        except imapclient.IMAPClient.Error as error:
            self.log_file.log_all(1, f"Reconnection failed. {str(error)}")
            self.reconnect()

    def get_array_of_messages_to_send(self) -> list:
        """
        Getting messages with a flag ['All'] from selected mail folder
        :return :list of tuples (uid, email_info) get from selected mail folder
        """
        self.get_all_messages()
        return self.final_list_to_send

    def logout_from_mail(self):
        """
        Logout from the mailbox
        :return:
        """
        self.server.close_folder()
        self.server.logout()
        self.log_file.log_all(3, "Logout from mailbox :(")
