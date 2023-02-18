import subprocess


def register_popen_wrapper():
    from mobt.PopenObserver.PopenWrapper import PopenWrapper
    if subprocess.Popen != PopenWrapper:
        subprocess.Popen = PopenWrapper
