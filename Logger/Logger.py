from datetime import datetime
import os
from time import sleep
import sentry_sdk

sentry_sdk.init("https://eca61270fe5e4ceeb1046ad58ad7333e@o402810.ingest.sentry.io/5264523")


class Log:
    def __init__(self, class_name):
        self.abs_path_to_log = os.path.abspath('Logs')
        # self.error_log_file = open("{}/errors.log".format(self.abs_path_to_log), "a")
        # self.access_log_file = open("{}/access.log".format(self.abs_path_to_log), "a")
        self.module = class_name

        self.priority = {
            1: "CRITICAL",
            2: "WARNING",
            3: "INFO",
            4: "DEBUG"
        }

    def log_all(self, priority, string):
        try:
            # if self.error_log_file.closed or self.access_log_file.closed:
            #     self.error_log_file = open("{}/errors.log".format(self.abs_path_to_log), "a")
            #     self.access_log_file = open("{}/access.log".format(self.abs_path_to_log), "a")
            # if self.error_log_file.writable() or self.access_log_file.writable():
            #     (self.access_log_file if priority == 3 or priority == 4 else self.error_log_file).writelines(
            #         "{} | {} | {} | {}\n".format(
            #             datetime.now(),
            #             self.module,
            #             self.priority.get(priority),
            #             string
            #         ))
            with open("{}/{}.log".format(self.abs_path_to_log,
                                         "access" if priority == 3 or 4 else "errors"),
                      "a") as file:
                file.writelines(
                    "{} | {} | {} | {}\n".format(
                        datetime.now(),
                        self.module,
                        self.priority.get(priority),
                        string
                    )
                )

            # self.error_log_file.close()
            # self.access_log_file.close()
        except BrokenPipeError as broken_pipe:
            with open("{}/errors.log".format(self.abs_path_to_log), "a") as error_log_file:
                error_log_file.writelines(
                    "{} | {} | {} | {}\n".format(
                        datetime.now(),
                        self.module,
                        self.priority.get(priority),
                        broken_pipe
                    ))
            sleep(10)
            self.log_all(priority, string)
