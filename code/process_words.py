from  process_words_txt import *
from process_config import *
import constant
import requests

def sync_local_stop_words(api_path):
    """
    更新停止词库。
    :param api_path:调用的请求api。
    :return: 无。
    """
    r = requests.get(api_path)
    text=r.text.strip("\n")
    with open(config_constant.STOP_WORDS_PATH, "w", encoding="utf-8") as f:
        f.write(text)

def sync_tag_to_new():
    """
    同步关键词库到新词库中。
    :return:
    """
    tag_words=open_file(config_constant.TAG_WORDS_PATH, "r")
    open_file(config_constant.NEW_WORDS_PATH, "a", tag_words)

def set_stop_words(stop_words):
    """
    添加停止词到停止词库中。

    同时将添加的停止词从新词库和关键词库中移除。
    :param stop_words:所添加的停止词，集合形式。
    :return:无。
    """
    open_file(config_constant.STOP_WORDS_PATH, "a", stop_words)
    tag_words=open_file(config_constant.TAG_WORDS_PATH, "r")
    tag_words=tag_words-stop_words
    new_words=open_file(config_constant.NEW_WORDS_PATH, "r")
    new_words=new_words-stop_words
    open_file(config_constant.TAG_WORDS_PATH, "w", tag_words)
    open_file(config_constant.NEW_WORDS_PATH, "w", new_words)

def set_tag_words(tag_words):
    """
    添加自定义的关键词到关键词库中。

    同时自定义的关键词加入到新词库中，从停止词库中删除。
    :param tag_words:添加的自定义的关键词，集合形式。
    :return:无。
    """
    open_file(config_constant.TAG_WORDS_PATH, "a", tag_words)
    stop_words=open_file(config_constant.STOP_WORDS_PATH, "r")
    stop_words=stop_words-tag_words
    open_file(config_constant.STOP_WORDS_PATH, "w", stop_words)
    open_file(config_constant.NEW_WORDS_PATH, "a", tag_words)

if __name__=="__main__":
    pass