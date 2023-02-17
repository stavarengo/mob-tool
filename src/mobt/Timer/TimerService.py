import sys
import time
from dataclasses import dataclass

import colorama
from injector import inject


@inject
@dataclass
class TimerService:
    def start(self, minutes: int):
        self._print_timer(minutes * 60)

    def _print_timer(self, duration_in_seconds: int):
        sys.stdout.flush()

        border = "-" * 20
        hide_cursor = "\033[?25l"
        show_cursor = "\033[?25h"
        print("")
        sys.stdout.write(hide_cursor)
        sys.stdout.write(f"+{border}+\n")
        try:
            for i in range(duration_in_seconds, -1, -1):
                minutes, seconds = divmod(i, 60)
                lines = [
                    "\r",
                    "|",
                    f"{minutes:02d}:{seconds:02d}".center(len(border), " "),
                    "|",
                    "\n",
                    f"+{border}+",
                ]
                sys.stdout.writelines(lines)
                sys.stdout.write(colorama.Cursor.UP(lines.count("\n")))
                sys.stdout.flush()
                time.sleep(1)

            sys.stdout.write(colorama.Cursor.DOWN(3))
            print("")
            print("")
        finally:
            sys.stdout.write(show_cursor)
