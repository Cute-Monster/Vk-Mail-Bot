from time import sleep
from datetime import datetime
from VkNotifier import VkNotifier
from Logger import Log


if __name__ == '__main__':
    """ # Debug
    login_type = int(input("Login method:\n"
                           "\t1 -> Group\n"
                           "\t2 -> User\n"
                           "\t---> "))
    chat_to_send_notification = int(input("Chat to send notifications:\n"
                                          "\t1 -> Mr.Robot\n"
                                          "\t2 -> Test\n"
                                          "\t---> "))
    send_to_dev_only = bool(int(input("Send to dev:\n"
                                      "\t1 -> Yes\n"
                                      "\t0 -> No\n"
                                      "\t---> ")))
    """

    log = Log(__name__)
    vk_notifier = VkNotifier(login_method=1,
                             chat_to_send=1,
                             send_only_to_dev=False)
    log.log_all(3, "Successfully started")
    vk_notifier.send_message_to_dev(text="Successfully started")
    sleep_university_time = int(600)
    sleep_summer_time = int(86400)
    sleep_night_time = None
    sleep_months = [7, 8]
    sleep_hours = [0, 1, 2, 3, 4, 5, 6, 7]
    exception_counter = 0
    while True:
        try:
            if datetime.now().month in sleep_months:
                log.log_all(3, f"Going to sleep for {sleep_summer_time}s")
                sleep(sleep_summer_time)
            elif datetime.now().hour in sleep_hours:
                sleep_night_time = 3600-(datetime.now().minute*60)
                log.log_all(3, f"Going to sleep for {sleep_night_time}s")
                sleep(sleep_night_time-datetime.now().second)
            else:
                vk_notifier.check_for_new_messages()
                log.log_all(3, f"Going to sleep for {sleep_university_time}s")
                sleep(sleep_university_time)
                # print("after sleep")
        except Exception as exception:
            exception_counter += 1
            log.log_all(1, exception)
            vk_notifier.send_message_to_dev(f"Critical in main:\n{str(exception)}")
            # vk_notifier.mail_client.reconnect()
            if exception_counter == 5:
                vk_notifier.send_message_to_dev("Exception counter limit reached!\nExiting :-(")
                vk_notifier.mail_client.logout_from_mail()
                log.log_all(1, "Terminating bot")
                exit(0)
