from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import os.path as path


def print_message(msg):
    message_subject = None
    for subj_item in msg['payload']['headers']:
        if subj_item['name'] == 'Subject':
            message_subject = ""
        else:
            message_subject = "No Subject Provided"
    # message_body = msg['snippet']
    message_from = ""
    for msg_item in msg['payload']['headers']:
        if msg_item['name'] == 'From':
            message_from = msg_item['value']
        elif msg_item['name'] == 'Subject':
            message_subject = msg_item['value']
    print("From: {}"
          "\nSubject: {}\n".format(message_from, message_subject))


def check_fetched_mail(fetched_mail, recent_inbox_emails):
    new_inbox_emails = []
    found = False
    if not recent_inbox_emails:
        for fetched_item in fetched_mail:
            new_inbox_emails.append(fetched_item['id'])
    else:
        print(new_inbox_emails)
        for fetched_item in fetched_mail:
            for idx, recent_item in enumerate(recent_inbox_emails):
                if fetched_item['id'] == recent_item:
                    found = True
                    # print(fetched_item['id'] + " is " + recent_item + ": ",
                    #       (fetched_item['id'] == recent_item), " found: ", found)
            if not found:
                # print(fetched_item['id'] + " ->  found: ", found)
                new_inbox_emails.append(fetched_item['id'])
    return new_inbox_emails


def get_mail_from_inbox():
    global new_inbox_email
    scopes = 'https://www.googleapis.com/auth/gmail.readonly'
    store = file.Storage('token.json')
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets("{}/client_id.json".format(path.abspath('.')),
                                              scopes)
        credentials = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=credentials.authorize(Http()))

    # Call the Gmail API to fetch INBOX
    results = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
    messages = results.get('messages', [])
    messages_array = []
    if not messages:
        print("No messages found.")
        return messages_array
    else:
        # print("Message snippets:")
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            messages_array.append(msg)

        return messages_array


def return_mail_to_vkbot(checked_inbox_email):

    get_messages_array = get_mail_from_inbox()

    new_inbox_emails = check_fetched_mail(get_messages_array, checked_inbox_email)

    for new_in_item in new_inbox_emails:
        checked_inbox_email.append(new_in_item)

    return new_inbox_emails, get_messages_array, checked_inbox_email


if __name__ == '__main__':
    recent_inbox_email = []
    new_inbox_email = []
    for i in range(0, 50):
        get_items = return_mail_to_vkbot(checked_inbox_email=recent_inbox_email)
        new_inbox_email = get_items[0]
        ft_messages_array = get_items[1]
        recent_inbox_email = get_items[2]
        print("fetched_messages\n", *ft_messages_array, sep='\n')
        print("recent messages\n", *recent_inbox_email, sep='\n')
        print("\nnew messages", *new_inbox_email, sep='\n')
        if not new_inbox_email:
            print("No New Messages")
        else:
            for new_item in new_inbox_email:
                for item in ft_messages_array:
                    if new_item == item['id']:
                        print_message(item)
        if input("continue? ") != 'y':
            exit(0)
