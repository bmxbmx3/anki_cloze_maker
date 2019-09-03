# 存放常量的地方

import process_config as pg


class config_constant:
    CONFIG_PATH = "./config.ini"
    API_PATH = ""
    NEW_WORDS_PATH = ""
    STOP_WORDS_PATH = ""
    TAG_WORDS_PATH = ""
    CHINESE_PINYIN_PATH = ""
    CHINESE_BIHUA_PATH = ""
    CLOZE_INDEX_SWITCH = True

    def __init__(self):
        pass

    @staticmethod
    def init_all_constant():
        config_constant.API_PATH = pg.get_file_path("api")
        config_constant.NEW_WORDS_PATH = pg.get_file_path("new_words")
        config_constant.STOP_WORDS_PATH = pg.get_file_path("stop_words")
        config_constant.TAG_WORDS_PATH = pg.get_file_path("tag_words")
        config_constant.CHINESE_PINYIN_PATH = pg.get_file_path("chinese_pinyin")
        config_constant.CHINESE_BIHUA_PATH = pg.get_file_path("chinese_bihua")
        config_constant.CLOZE_INDEX_SWITCH = pg.get_cloze_index_switch()