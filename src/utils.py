import os
import random
import string
from time import time


def tmp_file(type, ext):
    os.makedirs("tts", exist_ok=True)
    return f"tts/{type}-{suid()}.{ext}"


def suid():
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=10))


def log(msg, tick):
    print(f"{msg} {tick()}")


def timer():
    last_tick = time()

    def tick():
        nonlocal last_tick
        new_tick = time()
        duration = new_tick - last_tick
        last_tick = new_tick
        return f"+{duration:.2f}s"

    return tick


def write_stream(stream, path):
    with open(path, "wb") as fd:
        fd.write(stream.read())
