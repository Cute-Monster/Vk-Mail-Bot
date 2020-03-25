from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


def print_message(msg):
    for item in msg['payload']['headers']:
        if item['name'] == 'Subject':
            message_subject = ""
        else:
            message_subject = "No Subject Provided"
    message_body = msg['snippet']
    message_from = ""
    for item in msg['payload']['headers']:
        if item['name'] == 'From':
            message_from = item['value']
        elif item['name'] == 'Subject':
            message_subject = item['value']
    print("From: {}"
          "\nSubject: {}\n".format(message_from, message_subject))


def get_mail_from_inbox():
    SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets("Gmail/client_id.json", SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))

    # Call the Gmail API to fetch INBOX
    results = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
    messages = results.get('messages', [])
    messages_array = []
    if not messages:
        print("No messages found.")
        return messages_array
    else:
        print("Message snippets:")
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            messages_array.append(msg)
            # print_message(msg)
        return messages_array


if __name__ == '__main__':
    get_mail_from_inbox()