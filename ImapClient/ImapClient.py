import os

import imapclient
import pyzmail
from Logger.Logger import Log
import sentry_sdk
sentry_sdk.init("https://eca61270fe5e4ceeb1046ad58ad7333e@o402810.ingest.sentry.io/5264523")


class ImapClient:
    """
    Class representing connection to mailbox
    """

    def __init__(self):
        self.imap_link = os.getenv("Mail_Link")
        self.mail_login = os.getenv("Mail_Login")
        self.mail_password = os.getenv("Mail_Password")
        self.final_list_to_send = []
        self.log_file = Log(self.__class__)

    def get_all_messages(self):
        """
        Fetch,parse and add the parsed message with his (uid, email_info) to list of messages from a selected folder
        :return:
        """

        self.final_list_to_send.clear()

        try:
            with imapclient.IMAPClient(self.imap_link, 993) as server:
                server.login(self.mail_login, self.mail_password)
                server.select_folder("INBOX")

                for uid, msg in server.fetch(server.search(), 'RFC822').items():
                    message_factory = pyzmail.PyzMessage.factory(msg[b'RFC822'])  # Be sure to change the uid num
                    content_type = message_factory.smart_parser(message_factory).get_content_type()
                    msg_text = ""
                    if message_factory.text_part is None:
                        msg_text += "No text provided :-("
                    else:
                        msg_text_part = message_factory.text_part.get_payload().decode(
                            message_factory.text_part.charset
                        ).splitlines()
                        for i in range(0, len(msg_text_part) - 1):
                            try:
                                if msg_text_part[i + 1].startswith("От:") \
                                        or msg_text_part[i+1].startswith("> От:") \
                                        or msg_text_part[i + 1].startswith("From:") \
                                        or msg_text_part[i + 1].__contains__(
                                    f"<{message_factory.smart_parser(message_factory).get('Delivered-To')}>") \
                                        or msg_text_part[i + 1].__contains__("[image: ") \
                                        or msg_text_part[i+1].startswith("Отправлено с iPhone") \
                                        or msg_text_part[i+1].__contains__("Начало переадресованного сообщения"):
                                    msg_text += msg_text_part[i] + " "
                                    break
                                else:
                                    msg_text += msg_text_part[i] + " "
                            except IndexError as index_error:
                                self.log_file.log_all(2, index_error)

                    final_mail_inf = "You Have A New Email In The Mailbox:\n" \
                                     f"From: {message_factory.smart_parser(message_factory).get('From')}\n" \
                                     f"Subject: {message_factory.get_subject()}\n" \
                                     f"Text: {msg_text if msg_text else 'No'}\n" \
                                     f"Attachments: {'Yes' if content_type == 'multipart/mixed' or 'multipart/related' else 'No'} "
                    self.final_list_to_send.append({
                        "uid": uid,
                        "msg_text": final_mail_inf
                    })
        except imapclient.IMAPClient.Error as imap_error:
            self.log_file.log_all(1, str(imap_error))
            self.get_all_messages()

    def get_array_of_messages_to_send(self) -> list:
        """
        Getting messages with a flag ['All'] from selected mail folder
        :return :list of tuples (uid, email_info) get from selected mail folder
        """

        self.get_all_messages()
        return self.final_list_to_send
