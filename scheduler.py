from __future__ import annotations

import time

from app.bot import DealPlatform


class Scheduler:

    def __init__(self, interval: int = 300):
        self.interval = interval

    def start(self):

        while True:

            try:

                DealPlatform().run()

            except Exception as e:

                print(e)

            time.sleep(self.interval)


if __name__ == "__main__":
    Scheduler().start()
