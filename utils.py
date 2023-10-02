import datetime
import sys
from loguru import logger


logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")
now = datetime.datetime.now()
date_time = str(now.strftime("%d-%m-%Y %H-%M-%S"))
logger.add(f"logs/{date_time}.log")

def remove_line_break(s):
    return s.replace("\n", "")

def remove_line_breaks(lst):
    return list(map(lambda s: s.replace("\n", ""), lst))

def write_to_file(file_path, content, mode="a", separator="\n"):
    with open(file_path, mode, encoding="utf-8") as f:
        f.write(f"{content}{separator}")

def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def read_file_as_list(file_path, separator="\n"):
    with open(file_path, "r", encoding="utf-8") as f:
        if separator == "\n":
            return remove_line_breaks(f.readlines())
        else:
            return f.read().split(separator)