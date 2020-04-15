import requests
import os.path as path
from time import sleep
from datetime import datetime
import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
from Gmail.readEmail import return_mail_to_vkbot


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
    # print(short_message_info)
    return short_message_info


def two_fact_auth():

    key = input("Input Validation Key --> ")

    remember_device = True
    return key, remember_device


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
    vk_session = vk_api.VkApi(token=token, scope='messages')
    vk = vk_session.get_api()

    # upload = VkUpload(vk_session)  # Для загрузки изображений
    # longpoll = VkBotLongPoll(vk_session, group_id='193350828')
    """
    for event in longpoll.listen():
        
        if event.type == VkBotEventType.MESSAGE_NEW:
            print("New message for me:\n",
                  "For me from: ", event.obj.from_id,
                  "\nMessage: ", event.obj.text)
            vk.messages.send(
                peer_id='2000000003',
                raandom_id=get_random_id(),
                message="Hi^_^"
                )
    """
    def send_message_to_dev(text):
        vk.messages.send(
            user_id='198253590',  # 122029097 <- Даня, Я -> 198253590, Mr.Robot -> c84
            random_id=get_random_id(),
            message=text
        )

    def send_message_to_chat(text):
        vk.messages.send(
            peer_id='200000000{}'.format(3),  # 122029097 <- Даня, Mr.Robot -> 1, Test -> 3
            random_id=get_random_id(),
            message=text
        )

    recent_inbox_email = []
    sleep_time = int(15)  # 7200 <- 2h, 21600 -> 6h
    while True:
        log_file = open("{}/log.txt".format(path.abspath('logs')), "a")  # /home/pi/vkBot/vkBot/logs/log.txt
        get_items = return_mail_to_vkbot(checked_inbox_email=recent_inbox_email)
        new_inbox_email = get_items[0]
        ft_messages_array = get_items[1]
        recent_inbox_email = get_items[2]
        # print("fetched_messages\n", *ft_messages_array, sep='\n')
        # print("recent messages\n", *recent_inbox_email, sep='\n')
        # print("\n new messages", *new_inbox_email, sep='\n')
        if not new_inbox_email:
            send_message_to_dev('No new messages\n:-(')
            log_file.writelines("{}: {}\n".format(datetime.now(), 'No new messages'))
        else:
            for idx, new_item in enumerate(new_inbox_email):
                for ft_item in ft_messages_array:
                    if new_item == ft_item['id']:
                        # send_message_to_chat(message_info(ft_item))
                        send_message_to_dev(message_info(ft_item))
                if idx == len(new_inbox_email)-1:
                    # send_message_to_chat('Please, filter the INBOX ;-)')
                    send_message_to_dev('Please, filter the INBOX ;-)')

        if len(recent_inbox_email) > 5:
            recent_inbox_email.clear()
            send_message_to_dev('recent_inbox_email list cleared\n;-)')
            log_file.writelines("{}: {}\n".format(datetime.now(), 'recent_inbox_email list cleared'))
        log_file.writelines("{}: {}\n".format(datetime.now(), 'going to sleep {}s'.format(sleep_time)))
        log_file.close()
        sleep(sleep_time)  # 7200 <- 2h, 21600 -> 6h

        # for event in longpoll.listen():
        #     print(event)
        #     VkEventType.
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
