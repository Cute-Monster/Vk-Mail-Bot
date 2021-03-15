from datetime import datetime
import os
from time import sleep
import sentry_sdk

sentry_sdk.init(
    "https://eca61270fe5e4ceeb1046ad58ad7333e@o402810.ingest.sentry.io/5264523"
)


class Log:
    def __init__(self, class_name):
        self.abs_path_to_log = os.path.abspath("Logs")
        self.module = class_name

        self.priority = {1: "CRITICAL", 2: "WARNING", 3: "INFO", 4: "DEBUG"}

    def log_all(self, priority, string):
        try:
            with open(
                "{}/{}.log".format(
                    self.abs_path_to_log, "access" if priority == 3 or 4 else "errors"
                ),
                "a",
            ) as log_file:
                log_file.writelines(
                    "{} | {} | {} | {}\n".format(
                        datetime.now(), self.module, self.priority.get(priority), string
                    )
                )

        except BrokenPipeError as broken_pipe:
            with open(
                "{}/errors.log".format(self.abs_path_to_log), "a"
            ) as error_log_file:
                error_log_file.writelines(
                    "{} | {} | {} | {}\n".format(
                        datetime.now(),
                        self.module,
                        self.priority.get(priority),
                        broken_pipe,
                    )
                )
            sleep(10)
            self.log_all(priority, string)
