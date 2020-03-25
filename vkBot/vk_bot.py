import requests
from time import sleep
import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from Gmail.readEmail import get_mail_from_inbox


def message_info(msg):
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
    short_message_info = "You Have A New Email In The Mailbox:\n " \
                         "From: {}\n" \
                         "Subject: {}\n".format(message_from, message_subject)
    print(short_message_info)
    return short_message_info


def main():
    session = requests.Session()

    # Авторизация пользователя:
    """
    login, password = 'python@vk.com', 'mypassword'
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    """

    # Авторизация группы (для групп рекомендуется использовать VkBotLongPoll):
    # при передаче token вызывать vk_session.auth не нужно
    """
    vk_session = vk_api.VkApi(token='токен с доступом к сообщениям и фото')
    """
    token = '1e415cfb00820bd2be0c44ce3085998e5d73b441fa68cc0edbe152ae5b3babc75f043ca93e441ea7bc52d'
    vk_session = vk_api.VkApi(token=token)
    vk = vk_session.get_api()

    upload = VkUpload(vk_session)  # Для загрузки изображений
    longpoll = VkLongPoll(vk_session)
    new_gmail_inbox_messages = []
    recent_gmail_inbox_messages = []
    while True:

        fetched_gmail_inbox_messages = get_mail_from_inbox()
        for item in fetched_gmail_inbox_messages:
            if item not in recent_gmail_inbox_messages:
                new_gmail_inbox_messages.append(item)
        fetched_gmail_inbox_messages.clear()
        for item in new_gmail_inbox_messages:
            vk.messages.send(
                user_id='198253590',
                random_id=get_random_id(),
                message=message_info(item)
            )
            recent_gmail_inbox_messages.append(item)
        new_gmail_inbox_messages.clear()
        sleep(10)
        print("after sleep")
        # for event in longpoll.listen():
        #     if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        #         print('id{}: "{}"'.format(event.user_id, event.text), end=' ')
        #
        #         response = session.get(
        #             'http://api.duckduckgo.com/',
        #             params={
        #                 'q': event.text,
        #                 'format': 'json'
        #             }
        #         ).json()
        #
        #         text = response.get('AbstractText')
        #         image_url = response.get('Image')
        #
        #         if not text:
        #             vk.messages.send(
        #                 user_id=event.user_id,
        #                 random_id=get_random_id(),
        #                 message='No results'
        #             )
        #             print('no results')
        #             continue
        #
        #         attachments = []
        #
        #         if image_url:
        #             image = session.get(image_url, stream=True)
        #             photo = upload.photo_messages(photos=image.raw)[0]
        #
        #             attachments.append(
        #                 'photo{}_{}'.format(photo['owner_id'], photo['id'])
        #             )
        #
        #         vk.messages.send(
        #             user_id=event.user_id,
        #             attachment=','.join(attachments),
        #             random_id=get_random_id(),
        #             message=text
        #         )
        #         print('ok')


if __name__ == '__main__':
    main()
