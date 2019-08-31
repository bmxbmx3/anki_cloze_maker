# 对配置文件的一些操作

from configparser import ConfigParser
from constant import config_constant
import os


def set_path(file_name, path):
    """
    设置路径到config.ini中。

    文件路径必须是/分隔符，而不是\\分隔符，如果输入\\做分隔，程序会自动纠正为/。
    :param file_name: 文件名。
    :return: 无。
    """
    cfg = ConfigParser()
    cfg.read(config_constant.CONFIG_PATH)

    # 规范化路径
    norm_path = os.path.normpath(path).replace("\\", "/")
    cfg["path"][file_name] = norm_path
    with open(config_constant.CONFIG_PATH, "w") as conf:
        cfg.write(conf)


def get_file_path(file_name):
    """
    由文件名，获得文件的路径。
    :param file_name: 给定文件名。
    :return: 文件路径。
    """
    cfg = ConfigParser()
    cfg.read(config_constant.CONFIG_PATH)

    # 规范化路径
    file_path = cfg["path"][file_name]
    root_path = cfg["path"]["root"]
    if root_path in file_path:
        relative_file_path = file_path.replace(root_path, "%(root)s")
        set_path(file_name, relative_file_path)
    return file_path


def set_blanks_rate(blanks_per_word_count, per_word_count):
    """
    计算空格率，存入配置文件中。
    :param blanks_per_word_count: 每定长字符数中所含的空格数。
    :param per_word_count: 每定长字符数。
    :return: 无。
    """
    # 输入数字前先做判断。
    number_ruler = per_word_count <= 0 or blanks_per_word_count <= 0 or not str(
        per_word_count).isdigit() or not str(blanks_per_word_count).isdigit()
    blanks_rate = blanks_per_word_count / per_word_count
    cfg = ConfigParser()
    cfg.read(config_constant.CONFIG_PATH)
    a = cfg.sections()
    cfg["blanks"]["blanks_per_word_count"] = str(blanks_per_word_count)
    cfg["blanks"]["per_word_count"] = str(per_word_count)
    # 保存3位小数
    cfg["blanks"]["blanks_rate"] = "%.3f" % blanks_rate
    with open(config_constant.CONFIG_PATH, "w") as conf:
        cfg.write(conf)


def get_valid_char_count(text):
    """
    获取有效的字符数。
    :param text: 输入文本。
    :return: 有效字符数。
    """
    char_count = 0
    for i in text:
        # 计算真正的汉字、字母、数字在内的有效字符个数。
        if i.isdigit() or i.isalpha():
            char_count += 1
    return char_count


def get_valid_blanks_count(text):
    """
    获取有效的空格数。
    :param text: 输入文本
    :return: 有效的空格数。
    """
    cfg = ConfigParser()
    cfg.read(config_constant.CONFIG_PATH)
    blanks_rate = float(cfg["blanks"]["blanks_rate"])
    blanks = int(blanks_rate * get_valid_char_count(text))
    # 防止没有空格。
    if blanks == 0:
        blanks += 1
    return blanks


def get_cloze_index_switch():
    """
    获取对anki填空符是否加索引的设置，如{{c::[关键词]}}还是{{c[索引]::[关键词]}}。
    :return: 确认是否加索引的布尔值，True表示加，False表不加。
    """
    cfg = ConfigParser()
    cfg.read(config_constant.CONFIG_PATH)
    cloze_index_switch = (str(cfg["mode"]["cloze_index_switch"]) == "True")
    return cloze_index_switch


def set_cloze_index_switch(switch):
    """
    设置对anki填空符是否加索引，如{{c::[关键词]}}还是{{c[索引]::[关键词]}}。
    :param switch: True表示加，False表不加。
    :return: 无
    """
    cfg = ConfigParser()
    cfg.read(config_constant.CONFIG_PATH)
    cfg["mode"]["cloze_index_switch"] = str(switch)
    with open(config_constant.CONFIG_PATH, "w") as conf:
        cfg.write(conf)


if __name__ == "__main__":
    get_cloze_index_switch()
