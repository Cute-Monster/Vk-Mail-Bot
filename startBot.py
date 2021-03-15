#!/usr/bin/env python3
import argparse
import sys
from time import sleep
from typing import Dict, Union, List
from datetime import datetime

from VkNotifier.VkNotifier import VkNotifier
from Logger.Logger import Log
import sentry_sdk

sentry_sdk.init(
    "https://eca61270fe5e4ceeb1046ad58ad7333e@o402810.ingest.sentry.io/5264523"
)

# Creating Argument parser
_parser: argparse.ArgumentParser = argparse.ArgumentParser(
    prog="VkMailNotifier",
    description="Bot which checks mailServer for new mails and sends their content to user via VK",
    add_help=True,
)
_parser.add_argument(
    "--login-method",
    "-l",
    help="1 for Group method, 2 for user method",
    default=1,
    type=int,
    choices=[1, 2],
)
_parser.add_argument(
    "--reporting-chat",
    "-r",
    help="Chat number for sending reports",
    default=1,
    type=int,
    choices=[1, 2],
)
_parser.add_argument(
    "--dev-only",
    "-d",
    help="Send reports only to dev",
    default=True,
    type=bool,
    choices=[True, False]
)
_parser.add_argument(
    "--dev-id", "-i", help="Developer id to use", default="198253590", type=str
)
_args = _parser.parse_known_args()


vk_notifier: VkNotifier = VkNotifier(
    login_method=_args[0].login_method,
    chat_to_send=_args[0].reporting_chat,
    send_only_to_dev=_args[0].dev_only,
)
_log: Log = Log(__name__)
_sleep: Dict[str, Union[int, List[int], None]] = {
    "duration": int(600),
    "hours": [0, 1, 2, 3, 4, 5, 6, 7],
    "night_time": None,
}
_exception_counter: int = 0


def main(exception_counter=_exception_counter):
    while True:
        try:
            if datetime.now().hour in _sleep["hours"]:
                _sleep["night_time"] = 3600 - (datetime.now().minute * 60)
                _log.log_all(3, f"Going to sleep for {_sleep['night_time']}s")
                sleep(_sleep["night_time"] - datetime.now().second)
            else:
                vk_notifier.check_for_new_messages()
                _log.log_all(3, f"Going to sleep for {_sleep['duration']}s")
                sleep(_sleep["duration"])
        except KeyboardInterrupt as exc:
            vk_notifier.send_message_to_dev(exc.__str__())
            vk_notifier.db.close_connection()
            sys.exit()

        except Exception as exception:
            exception_counter += 1
            _log.log_all(1, exception)
            vk_notifier.send_message_to_dev(
                "Critical in main!\n" "Exception:\n" f"{str(exception)}"
            )
            if exception_counter == 5:
                vk_notifier.send_message_to_dev(
                    "Exception counter limit reached!\nExiting :-("
                )
                vk_notifier.db.close_connection()
                _log.log_all(1, "Terminating bot")
                sys.exit()


if __name__ == '__main__':
    main()
