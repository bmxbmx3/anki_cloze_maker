import jieba.analyse

from main import *
from process_config import get_valid_blanks_count
from process_words import *
from random import sample

def get_all_tag_words(text):
    """
    获取关键词(tag_word.txt+jieba的tf-idf算法)。
    :param text：输入tf-idf算法待提取关键词的文本。
    :return: 返回所有关键词all_tag_words，有效空格数blanks_count。
    """

    # jieba的tf-idf算法分析的关键词，这里最先导入停止词库。
    jieba.analyse.set_stop_words(config_constant.STOP_WORDS_PATH)
    tf_idf_tag_words = jieba.analyse.extract_tags(
        text, topK=None, withWeight=False, allowPOS=())
    tf_idf_tag_words = set(tf_idf_tag_words)

    # tag_words.txt自定义的关键词。
    custom_tag_words = open_file(config_constant.TAG_WORDS_PATH, "r")
    #计算有效空格数。
    blanks_count=get_valid_blanks_count(text)
    tf_idf_tag_length=len(tf_idf_tag_words)
    custom_tag_length=len(custom_tag_words)
    tag_count=tf_idf_tag_length+custom_tag_length
    #如果找到的关键词总数超过期望的空格数，按百分比随机选取tf-idf算法所找的关键词和自定义的关键词。
    if tag_count>blanks_count:
        rate=blanks_count/tag_count
        tf_idf_tag_count=int(rate*tf_idf_tag_length)
        custom_tag_count=int(rate*custom_tag_length)
        tf_idf_tag_words=set(sample(list(tf_idf_tag_words),tf_idf_tag_count))
        custom_tag_words=set(sample(list(custom_tag_words),custom_tag_count))
    all_tag_words=tf_idf_tag_words|custom_tag_words

    return all_tag_words,blanks_count


def get_seged_words(text):
    """
    获取用jieba按新词库分词后的分词列表。
    :param text: 输入待分词的文本。
    :return: 分词后的分词列表。
    """
    # 抑制jieba的日志消息。
    jieba.setLogLevel(20)
    # jieba导入新词库。
    jieba.load_userdict(config_constant.NEW_WORDS_PATH)
    # 将文本分词。
    seged_words = list(jieba.cut(text, cut_all=False))
    return seged_words


def get_cloze_seged_words(text):
    """
    对给定的文本，获得添加填空后的分词列表。
    :param text: 输入待加填空的文本。
    :return: 添加填空的分词列表cloze_seged_words。
    """
    seged_words = get_seged_words(text)
    all_tag_words,blanks_count = get_all_tag_words(text)

    # 对文本所找到关键词的缓存,只用于给 anki 填空符添加索引用。
    tmp_tag_words = []
    cloze_seged_words = []
    # 索引
    count = 0

    # 给文本添加填空。
    if config_constant.CLOZE_INDEX_SWITCH:
        for seged_word in seged_words:
            if seged_word in all_tag_words:
                if seged_word in tmp_tag_words:
                    word_index = tmp_tag_words.index(seged_word) + 1
                    # 给 anki 填空符添加索引。
                    seged_word = "".join(
                        ["{{c", str(word_index), "::", seged_word, "}}"])
                else:
                    count += 1
                    tmp_tag_words.append(seged_word)
                    seged_word = "".join(
                        ["{{c", str(count), "::", seged_word, "}}"])
            cloze_seged_words.append(seged_word)
    elif config_constant.CLOZE_INDEX_SWITCH == False:
        for seged_word in seged_words:
            if seged_word in all_tag_words:
                tmp_tag_words.append(seged_word)
                seged_word = "".join(["{{c1", "::", seged_word, "}}"])
            cloze_seged_words.append(seged_word)

    text_tag_count = len(all_tag_words)
    if blanks_count > text_tag_count:
        print(
            '你所期望的空格数为 %d 个，但超过系统找到的关键词数 %d 个。' %
            (blanks_count, text_tag_count))
        divide()
    return cloze_seged_words
