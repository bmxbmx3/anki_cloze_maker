# 读写res文件下new_words.txt、stop_words.txt、tag_words.txt。
from cn_sort.process_cn_word import *

def open_file(path, operator, new_set={""}):
    """
    读写.txt文件,支持“r/w/a”。
    :param path:读写的文件路径。
    :param operator:读/写操作。
    :param new_set:写入时所需的词的集合。
    :return:如果读，以集合形式返回读出的文本；如果写，什么也不返回。
    """
    with open(path, operator, encoding="utf-8") as f:
        if operator == "r":
            new_words = f.readlines()
            tmp_set = set()
            for new_word in new_words:
                new_word = new_word.strip("\n").strip(" ")
                if new_word != "":
                    tmp_set.add(new_word)
            # 防止文件出现空行。
            open_file(path, "w", tmp_set)
            return tmp_set
        elif operator == "w":
            # 对元素排序。
            lines = list(sort_text_list(list(new_set)))
            # 防止读取空文件，否则lines[-1].strip("\n")会出错。
            if not lines:
                lines.append("")
            lines = ["".join([line, "\n"]) for line in lines]
            lines[-1] = lines[-1].strip("\n")
            f.writelines(lines)
        elif operator == "a":
            old_set = open_file(path, "r")
            # 防止文件出现空行。
            open_file(path, "w", old_set)
            add_set = new_set - old_set
            if len(add_set) != 0:
                # 对元素排序。
                lines = list(sort_text_list(list(add_set)))
                lines = ["".join([line, "\n"]) for line in lines]
                lines[-1] = lines[-1].strip("\n")
                # 如果读入的原文件为空，就不要另起一行，否则另起下一行插入。
                if old_set:
                    lines.insert(0, "\n")
                f.writelines(lines)
