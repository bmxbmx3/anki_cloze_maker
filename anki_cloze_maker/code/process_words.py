import requests
from process_words_txt import *
from constant import config_constant

def sync_local_stop_words():
    """
    更新停止词库。
    :return: 无。
    """
    stop_words_api_path=config_constant.STOP_WORDS_API_PATH
    r = requests.get(stop_words_api_path)
    stop_words_list = r.text.strip("\n").split("\n")
    stop_words_list_sorted = cnsort(stop_words_list)
    stop_words_list_sorted = ["".join([stop_word, "\n"]) for stop_word in stop_words_list_sorted]
    stop_words_list_sorted[-1] = stop_words_list_sorted[-1].strip("\n")
    with open(config_constant.STOP_WORDS_PATH, "w", encoding="utf-8") as f:
        f.writelines(stop_words_list_sorted)


def sync_tag_to_new():
    """
    同步关键词库到新词库中。
    :return:
    """
    all_tag_words = open_file(config_constant.TAG_WORDS_PATH, "r")
    open_file(config_constant.NEW_WORDS_PATH, "a", all_tag_words)


def set_stop_words(stop_words={""}):
    """
    添加停止词到停止词库中。

    同时将添加的停止词从新词库和关键词库中移除。
    :param stop_words:所添加的停止词，集合形式。
    :return:无。
    """
    # 保存自定义的停止词到停止词库中。
    open_file(config_constant.STOP_WORDS_PATH, "a", stop_words)

    # 从关键词库中去除停止词库的词。
    all_tag_words = open_file(config_constant.TAG_WORDS_PATH, "r")
    all_stop_words = open_file(config_constant.STOP_WORDS_PATH, "r")
    all_tag_words = all_tag_words - all_stop_words
    open_file(config_constant.TAG_WORDS_PATH, "w", all_tag_words)

    # 从新词库中去除停止词库的词。
    all_new_words = open_file(config_constant.NEW_WORDS_PATH, "r")
    all_stop_words = open_file(config_constant.STOP_WORDS_PATH, "r")
    all_new_words = all_new_words - all_stop_words
    open_file(config_constant.NEW_WORDS_PATH, "w", all_new_words)


def set_tag_words(tag_words={""}):
    """
    添加自定义的关键词到关键词库中。

    同时自定义的关键词加入到新词库中，从停止词库中删除。
    :param tag_words:添加的自定义的关键词，集合形式。
    :return:无。
    """
    # 保存自定义的关键词到关键词库中。
    open_file(config_constant.TAG_WORDS_PATH, "a", tag_words)

    # 同步关键词库到新词库中。
    sync_tag_to_new()

    # 从停止词库中去除关键词。
    all_stop_words = open_file(config_constant.STOP_WORDS_PATH, "r")
    all_tag_words = open_file(config_constant.TAG_WORDS_PATH, "r")
    all_stop_words = all_stop_words - all_tag_words
    open_file(config_constant.STOP_WORDS_PATH, "w", all_stop_words)


def set_new_words(new_words={""}):
    """
    添加自定义的新词到新词库中。

    同时自定义的关键词加入到新词库中，从停止词库中删除。
    :param new_words:添加的自定义的关键词，集合形式。
    :return:无。
    """
    # 保存自定义的新词到新词库中。
    open_file(config_constant.NEW_WORDS_PATH, "a", new_words)

    # 先同步关键词库到新词库中，防止关键词库不是新词库的子集。
    sync_tag_to_new()

    # 从停止词库中去除新词库的词。
    all_stop_words = open_file(config_constant.STOP_WORDS_PATH, "r")
    all_new_words = open_file(config_constant.NEW_WORDS_PATH, "r")
    all_stop_words = all_stop_words - all_new_words
    open_file(config_constant.STOP_WORDS_PATH, "w", all_stop_words)