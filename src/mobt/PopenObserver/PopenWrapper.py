import subprocess

from mobt.PopenObserver.PopenListener import PopenListener

_listeners = []


def _notify_listeners(command: list, result: tuple):
    if not _listeners:
        return

    stdout, stderr = result
    for listener in _listeners:
        listener.popen_executed(command, stdout, stderr)


class PopenWrapper(subprocess.Popen):

    @staticmethod
    def add_listener(listener: PopenListener):
        _listeners.append(listener)

    @staticmethod
    def remove_listener(listener: PopenListener):
        _listeners.remove(listener)

    def communicate(self, *args, **kwargs):
        result = super().communicate(*args, **kwargs)
        _notify_listeners(self.args, result)
        return result
