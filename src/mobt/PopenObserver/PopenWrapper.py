import subprocess

from mobt.PopenObserver.PopenListener import PopenListener

_listeners: list[PopenListener] = []


def _notify_listeners(command: list[str], stdout: str, stderr: str):
    if not _listeners:
        return

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
        stdout, stderr = result
        stdout_str = stdout.decode('utf-8')
        stderr_str = stderr.decode('utf-8')
        _notify_listeners(self.args, stdout_str, stderr_str)
        return result
