# from datetime import datetime
# import os
# if __name__ == '__main__':
#
#     # test = {'test':1,
#     #         'B':2}
#     # test.update([('A', 3)])
#     # test.update([('A', 4)])
#     # print(datetime.now().minute)
#     # print(datetime.now().minute*60)
#     # print(datetime.now().second)
#     # print(3600-(datetime.now().minute*60))
#
#     # send_to_dev_only = bool(int(input("Send to dev:\n"
#     #                                   "\t1 -> Yes\n"
#     #                                   "\t0 -> No\n"
#     #                                   "\t---> ")))
#     file = open("Logs/test.log", "a")
#     priority = 3
#     if file.closed:
#         print("closed")
#     else:
#         print("Opened")
#     file.close()
#     if file.closed:
#         print("closed")
#     else:
#         print("Opened")
#
#     print(os.path.getsize("venv.tar.xz")/float(1 << 20))
#     # testing = []
#     # testing.append((1, 3))
#     # testing.append((5, 7))
#     if priority is 4 or 3:
#         print(priority)
#     # print(testing)
#     # for first, last in enumerate(testing):
#     #     print(f" : first -> {first} : last -> {last}")
#     # print(send_to_dev_only)
#     # for value in test:
#     #     print(test.get(value))
#     # print("Hi", test.__len__())
import pyzmail
from imapclient import IMAPClient

HOST = 'imap.gmail.com'
USERNAME = 'runtov.constantin@gmail.com'
PASSWORD = '4apFMCRyB8a4pTD'

server = IMAPClient(HOST)
server.login(USERNAME, PASSWORD)
server.select_folder('INBOX')

if __name__ == '__main__':
    # print(__name__)
    # Start IDLE mode
    server.idle()
    print("Connection is now in IDLE mode, send yourself an email or quit with ^c")

    while True:
        try:
            # Wait for up to 30 seconds for an IDLE response
            # test = []
            responses = server.idle_check(timeout=30)
            # print(responses)
            tests = server.fetch(responses[0][0], 'RFC822')
            print(tests)
            parsed_message = pyzmail.PyzMessage.factory(responses[0][0][b'RFC822'])
            final_mail_inf = "You Have A New Email In The Mailbox:\n" \
                             "From: {} <{}>\n" \
                             "Subject: {}".format(parsed_message.get_address('From')[0],
                                                  parsed_message.get_address('From')[1],
                                                  parsed_message.get_subject())
            print(final_mail_inf)
            # Be sure to change the uid num
            # for item in responses:
            #     print(item)
            #     for uid, items in server.fetch(item[0], 'RFC822]'):
            #         print(uid, items, sep=' : ')
            #         parsed_message = pyzmail.PyzMessage.factory(items[b'RFC822'])  # Be sure to change the uid num
            #         final_mail_inf = "You Have A New Email In The Mailbox:\n" \
            #                          "From: {} <{}>\n" \
            #                          "Subject: {}".format(parsed_message.get_address('From')[0],
            #                                               parsed_message.get_address('From')[1],
            #                                               parsed_message.get_subject())
            #         print(final_mail_inf)
            # print(test)
            # hello = server.fetch(test, 'RFC822]')
            # print(hello)
            # for uid, items in hello.items():
            #     parsed_message = pyzmail.PyzMessage.factory(items[b'RFC822'])  # Be sure to change the uid num
            #     final_mail_inf = "You Have A New Email In The Mailbox:\n" \
            #                      "From: {} <{}>\n" \
            #                      "Subject: {}".format(parsed_message.get_address('From')[0],
            #                                           parsed_message.get_address('From')[1],
            #                                           parsed_message.get_subject())
            #     print(final_mail_inf)
            print("Server sent:", responses if responses else "nothing")
        except KeyboardInterrupt:
            break

    server.idle_done()
    print("\nIDLE mode done")
    server.logout()
