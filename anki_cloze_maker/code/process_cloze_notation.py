# 用于对填空符的操作。

import re
import os
from main import *
from cn_sort import *
from constant import *
from process_words import *


def get_tag_from_cloze(in_path, out_path=""):
    """
    从填空符获取关键词，并存储到tag_words.txt中。
    :param in_path: 输入的文件路径。
    :param out_path: 输出的文件路径（暂时不用）。
    :return: 无。
    """
    pattern = re.compile(r"{{c\d+::((?P<value>[^:]*).*?)}}")
    tag_words = set()
    with open(in_path, "r", encoding="utf-8") as f:
        while True:
            line = f.readline()
            if line:
                result = pattern.finditer(line)
                for i in result:
                    tag_words.add(i.group("value"))
            else:
                break
    set_tag_words(tag_words)


def remove_cloze_index(in_path, out_path):
    """
    去除填空的索引，使多个填空一次性出现。
    :param in_path: 输入文件的路径。
    :param out_path: 输出文件的路径。
    :return: 无。
    """
    pattern = re.compile(r"{{c\d+::((?P<value>[^:]*).*?)}}")
    with open(in_path, "r", encoding="utf-8") as f_in:
        result = []
        while True:
            line = f_in.readline()
            if line:
                line = pattern.sub(lambda i: "".join(
                    ["{{c1::", i.group("value"), "}}"]), line)
                result.append(line)
            else:
                break
        with open(out_path, "w", encoding="utf-8") as f_out:
            f_out.writelines(result)


def change_index(i, tmp):
    """
    寻找并生成index。
    :param i:匹配到的填空字符。
    :param tmp:每一行里从前往后已找到的填空字符集。
    :return:添加index的填空字符。
    """
    value = i.group("value")
    if value not in tmp:
        tmp.append(value)
    index = tmp.index(value) + 1
    concat_str = "".join(["{{c", str(index), "::", value, "}}"])
    return concat_str


def add_cloze_index(in_path, out_path):
    """
    添加填空的索引，使多个填空一次一个出现。
    :param in_path:输入文件的路径。
    :param out_path:输出文件的路径。
    :return:无。
    """
    pattern = re.compile(r"{{c\d+::((?P<value>[^:]*).*?)}}")
    with open(in_path, "r", encoding="utf-8") as f_in:
        result = []
        tmp = []
        while True:
            tmp.clear()
            line = f_in.readline()
            if line:
                line = pattern.sub(lambda i: change_index(i, tmp), line)
                result.append(line)
            else:
                break
        with open(out_path, "w", encoding="utf-8") as f_out:
            f_out.writelines(result)


def remove_cloze(in_path, out_path):
    """
    去除填空符。
    :param in_path: 输入文件的路径。
    :param out_path: 输出文件的路径。
    :return:无。
    """
    pattern = re.compile(r"{{c\d+::((?P<value>[^:]*).*?)}}")
    with open(in_path, "r", encoding="utf-8") as f_in:
        result = []
        while True:
            line = f_in.readline()
            if line:
                line = pattern.sub(lambda i: i.group("value"), line)
                result.append(line)
            else:
                break
        with open(out_path, "w", encoding="utf-8") as f_out:
            f_out.writelines(result)