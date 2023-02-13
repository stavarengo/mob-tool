import platform
import subprocess
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
            print("")
            self.make_laptop_speak("Mob Rotate!")
        finally:
            sys.stdout.write(show_cursor)

    def make_laptop_speak(self, text: str):
        if platform.system() == 'Darwin':
            subprocess.call(['say', text])
        elif platform.system() == 'Linux':
            subprocess.call(['espeak', text])
        else:
            print("\a")
