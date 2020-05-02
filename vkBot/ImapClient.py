import imapclient
import pyzmail
from Logger import Log


class ImapClient:
    def __init__(self):
        self.imap_link = 'imap.gmail.com'
        self.mail_login = 'gruppa1802@gmail.com'
        self.mail_password = '01012019'
        self.server = imapclient.IMAPClient(self.imap_link)
        self.server.login(self.mail_login, self.mail_password)
        self.new_messages = None
        self.list_of_seen_uids = []
        self.final_array_to_send = []
        self.log_file = Log(self.__module__)
        self.select_inbox_folder()

    def select_inbox_folder(self):
        self.server.select_folder('INBOX', readonly=True)

    def get_unseen_messages(self):
        self.final_array_to_send.clear()
        self.new_messages = self.server.search(['ALL'])
        for uid, msg in self.server.fetch(self.new_messages, 'RFC822').items():
            parsed_message = pyzmail.PyzMessage.factory(msg[b'RFC822'])  # Be sure to change the uid num
            final_mail_inf = "You Have A New Email In The Mailbox:\n" \
                             "From: {} <{}>\n" \
                             "Subject: {}".format(parsed_message.get_address('From')[0],
                                                  parsed_message.get_address('From')[1],
                                                  parsed_message.get_subject())

            self.final_array_to_send.append((uid, final_mail_inf))

    def is_in_list_of_seen(self, value) -> bool:
        for uid in self.list_of_seen_uids:
            if uid == value:
                return True
        return False

    def get_array_of_messages_to_send(self):
        self.get_unseen_messages()
        return self.final_array_to_send

    def clear_final_array_to_send(self):
        self.final_array_to_send.clear()

    def check_final_array_to_send_length(self):
        if self.final_array_to_send.__len__() > 15:
            self.clear_final_array_to_send()
            self.log_file.log_all(3, "final_array_to_send cleared")
