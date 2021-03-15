import os
from typing import List, Dict, Any, Union

import imapclient
import pyzmail

from Logger.Logger import Log
import sentry_sdk

sentry_sdk.init(
    "https://eca61270fe5e4ceeb1046ad58ad7333e@o402810.ingest.sentry.io/5264523"
)


class ImapClient:
    """
    Class representing connection to mailbox
    """

    def __init__(self):
        self.__imap_link: str = os.getenv("MAIL_LINK")
        self.__mail_login: str = os.getenv("MAIL_USERNAME")
        self.__mail_password: str = os.getenv("MAIL_PASSWORD")
        self.__final_list_to_send: List[
            Dict[str, Union[int, Any]]
        ] = []
        self.__log_file: Log = Log(self.__class__)

    def __get_all_messages(self):
        # type: (ImapClient) -> None
        """
        Fetch,parse and add the parsed message with his (uid, email_info) to list of messages from a selected folder
        :return:
        """

        self.__final_list_to_send.clear()

        try:
            with imapclient.IMAPClient(self.__imap_link, 993) as server:
                server.login(self.__mail_login, self.__mail_password)
                server.select_folder("INBOX")

                for uid, msg in server.fetch(server.search([u'UNSEEN']), "RFC822").items():
                    # Be sure to change the uid num
                    message_factory: pyzmail.PyzMessage = pyzmail.PyzMessage.factory(
                        msg[b"RFC822"]
                    )
                    content_type: str = message_factory.smart_parser(
                        message_factory
                    ).get_content_type()
                    msg_text: str = ""
                    if message_factory.text_part is None:
                        msg_text += "No text provided :-("
                    else:
                        msg_text_part = (
                            message_factory.text_part.get_payload()
                            .decode(message_factory.text_part.charset)
                            .splitlines()
                        )
                        for idx in range(0, len(msg_text_part) - 1):
                            try:
                                if (
                                    msg_text_part[idx + 1].startswith("От:")
                                    or msg_text_part[idx + 1].startswith("> От:")
                                    or msg_text_part[idx + 1].startswith("From:")
                                    or msg_text_part[idx + 1].__contains__(
                                        f"<{message_factory.smart_parser(message_factory).get('Delivered-To')}>"
                                    )
                                    or msg_text_part[idx + 1].__contains__("[image: ")
                                    or msg_text_part[idx + 1].startswith(
                                        "Отправлено с iPhone"
                                    )
                                    or msg_text_part[idx + 1].__contains__(
                                        "Начало переадресованного сообщения"
                                    )
                                ):
                                    msg_text += msg_text_part[idx] + " "
                                    break
                                else:
                                    msg_text += msg_text_part[idx] + " "
                            except IndexError as index_error:
                                self.__log_file.log_all(2, index_error)

                    final_mail_inf: str = (
                        "You Have A New Email In The Mailbox:\n"
                        f"From: {message_factory.smart_parser(message_factory).get('From')}\n"
                        f"Subject: {message_factory.get_subject()}\n"
                        f"Text: {msg_text if msg_text else 'No'}\n"
                        f"Attachments: {'Yes' if content_type == ('multipart/mixed' or 'multipart/related') else 'No'} "
                    )
                    self.__final_list_to_send.append(
                        {"uid": uid, "msg_text": final_mail_inf}
                    )
        except imapclient.IMAPClient.Error as imap_error:
            self.__log_file.log_all(1, str(imap_error))
            self.__get_all_messages()

    def get_array_of_messages_to_send(self):
        # type: (ImapClient) -> List[dict]
        """
        Getting messages with a flag ['All'] from selected mail folder
        :return :list of tuples (uid, email_info) get from selected mail folder
        """

        self.__get_all_messages()
        self.__final_list_to_send.reverse()
        return self.__final_list_to_send
