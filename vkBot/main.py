from time import sleep
from datetime import datetime
from Logger import Log
from VkNotifier import VkNotifier


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

    log = Log("main")
    vk_notifier = VkNotifier(login_method=1,
                             chat_to_send=1,
                             send_only_to_dev=False)
    log.log_all(3, "Successfully started")
    sleep_university_time = int(600)
    sleep_summer_time = int(86400)
    sleep_night_time = None
    sleep_months = [7, 8]
    sleep_hours = [0, 1, 2, 3, 4, 5, 6, 7]
    while True:
        try:
            if datetime.now().month in sleep_months:
                log.log_all(3, f"Going to sleep for {sleep_summer_time}s")
                sleep(sleep_summer_time)
            elif datetime.now().hour in sleep_hours:
                sleep_night_time = 3600-(datetime.now().minute*60)
                log.log_all(3, f"Going to sleep for {sleep_night_time}s")
                sleep(sleep_night_time-5)
            else:
                vk_notifier.check_for_new_messages()
                log.log_all(3, f"Going to sleep for {sleep_university_time}s")
                sleep(sleep_university_time)
        except Exception as exception:
            log.log_all(1, exception)
            vk_notifier.send_message_to_dev("Critical in main:\n" + exception)
            exit(0)
