# 交互式生成填空的文本。
import os

from process_config import set_blanks_rate, get_file_path, set_path, set_cloze_index_switch
from process_text import *
from process_cloze_notation import *


def divide():
    """
    用于字段间的分隔。
    :return: 无。
    """
    print("---------------------------------------------------------------------------------------------------")


def save_cloze_text(in_path, out_path):
    """
    保存批量添加填空的文本。
    :param in_path: 待添加填空的.txt文件路径。
    :param out_path:输出填空的.txt文件路径。
    :return: 无。
    """

    # 添加填空的文本。
    cloze_out_lines = []

    with open(in_path, "r", encoding="utf-8") as f:
        in_lines = f.readlines()
        in_lines = [in_line.strip("\n") for in_line in in_lines]

        for in_line in in_lines:
            while True:

                cloze_seged_words = get_cloze_seged_words(in_line)
                cloze_out_line = "".join(cloze_seged_words)

                print("经处理后的anki填空形式的分词列表：")
                print(cloze_out_line)
                divide()
                answer = input("是否需要继续修改？[y/n]\n")
                divide()
                if answer == "y":
                    ask_to_set_words()
                elif answer == "n":
                    cloze_out_lines.append(cloze_out_line)
                    break
            answer = input("是否自动将修改应用到所有文本？[y/n]\n")
            divide()
            if answer == "y":
                cloze_out_lines = []
                for in_line in in_lines:
                    cloze_seged_words = get_cloze_seged_words(in_line)
                    cloze_out_line = "".join(cloze_seged_words)
                    cloze_out_lines.append(cloze_out_line)
                break
        cloze_out_lines = ["".join([cloze_out_line, "\n"])
                           for cloze_out_line in cloze_out_lines]
        cloze_out_lines[-1] = cloze_out_lines[-1].strip("\n")

    with open(out_path, "w", encoding="utf-8") as m:
        m.writelines(cloze_out_lines)

    print("成功保存输出的文件!")
    divide()


def ask_to_set_cloze():
    """
    交互式询问建立填空。
    :return:无。
    """
    in_path = ""
    out_path = ""
    while True:
        in_path = input("请输入源文件的路径[源文件需存在且必须有.txt后缀]：\n")
        divide()
        in_path_last = os.path.splitext(in_path)[-1]
        if not os.path.exists(in_path) and in_path_last != ".txt":
            print("请输入正确的文件路径！")
            divide()
        else:
            break

    while True:
        out_path = input("请输入目标文件的路径[目标文件必须有.txt后缀]：\n")
        divide()
        out_path_last = os.path.splitext(out_path)[-1]
        if out_path_last != ".txt":
            print("请输入正确的文件路径！")
            divide()
        else:
            break

    save_cloze_text(in_path, out_path)


def ask_to_set_words():
    """
    交互式询问添加新词/关键词/停止词的操作。
    :return: 无。
    """
    answer = input("请添加新词/关键词/停止词。[new/tag/stop ...(...为添加的词，用空格分开)]\n")
    answer_list = answer.split(" ")
    operator = answer_list[0]
    words = set(answer_list[1:])
    if operator == "tag":
        set_tag_words(words)
    elif operator == "stop":
        set_stop_words(words)
    elif operator == "new":
        set_new_words(words)
    print("添加成功！")
    divide()


def ask_to_set_blanks_rate():
    """
    交互式询问设置空格率。
    :return: 无。
    """
    blanks_per_word_count = 1
    per_word_count = 10
    while True:
        try:
            blanks_per_word_count = int(input("请输入每定长字符数中的空格数：\n"))
            divide()
        except ValueError:
            print("请输入正确的整数！")
            divide()
            continue
        if blanks_per_word_count <= 0:
            print("请输入正数！\n")
            divide()
            continue
        else:
            break

    while True:
        try:
            per_word_count = int(input("请输入每定长字符数：\n"))
            divide()
        except ValueError:
            print("请输入正确的整数！")
            divide()
            continue
        if per_word_count <= 0:
            print("请输入正数！")
            divide()
            continue

        if blanks_per_word_count > per_word_count:
            print("每定长字符数中所含的空格数,不要超过每定长字符数！")
            divide()
        else:
            break

    set_blanks_rate(blanks_per_word_count, per_word_count)
    print("成功设置空格率！")
    divide()


def ask_to_sync_stop_words():
    """
    交互式询问更新本地停止词库。
    :return:无。
    """
    answer = input("你是否要更新本地的停止词库？[y/n]\n")
    divide()
    if answer == "y":
        sync_local_stop_words()
        print("成功更新本地本地的停止词库！")
        divide()

def ask_to_set_root_path():
    """
    交互式询问设置 anki_cloze_maker 所在的根目录。
    :return: 无。
    """
    while True:
        root_path = input(
            "请设置 anki_cloze_maker 所在的根目录[.../anki_cloze_maker 该路径必须存在]:\n")
        divide()
        root_path_last = os.path.split(root_path)[-1]
        if not os.path.isdir(
                root_path) or root_path_last != "anki_cloze_maker":
            print("请输入正确的路径！")
            divide()
        else:
            set_path("root", root_path)
            print("成功设置根目录！")
            divide()
            break


def ask_to_set_cloze_index():
    """
    交互式询问是否对 anki 填空符添加索引。
    :return:
    """
    while True:
        answer = input("请启用/关闭 anki 填空符的索引[True/False]:\n")
        divide()
        if answer == "True":
            set_cloze_index_switch(True)
            print("成功启用 anki 填空符的索引！")
            divide()
            break
        elif answer == "False":
            set_cloze_index_switch(False)
            print("成功关闭 anki 填空符的索引！")
            divide()
            break
        else:
            print("请输入 True/False ！")
            divide()


def ask_to_operate_cloze():
    """
    交互式询问对填空符的操作。
    :return:无。
    """
    while True:
        operate_cloze_description = "\n".join(
            ["请选择对填空符相应的操作[按序号]：", "1.对填空符添加索引", "2.对填空符去除索引", "3.去除填空符", "4.由填空符导入关键词"])
        choose_index = input(operate_cloze_description + "\n")
        divide()
        choose = {
            "1": add_cloze_index,
            "2": remove_cloze_index,
            "3": remove_cloze,
            "4": get_tag_from_cloze}
        if choose_index not in ["1", "2", "3", "4"]:
            print("请输入正确的序号！")
            divide()
        else:
            # 输入文件的路径
            in_path = ""
            # 输出文件的路径
            out_path = ""

            while True:
                in_path = input("请输入源文件的路径[源文件的路径存在且必须有.txt后缀]:\n")
                divide()
                in_path_last = os.path.splitext(in_path)[-1]
                if os.path.exists(in_path) and in_path_last == ".txt":
                    break
                else:
                    print("请输入正确的文件路径！")
                    divide()

            if choose_index in ["1", "2", "3"]:
                while True:
                    out_path = input("请输入目标文件的路径[源文件的路径必须有.txt后缀]:\n")
                    divide()
                    out_path_last = os.path.splitext(out_path)[-1]
                    if out_path_last == ".txt":
                        break
                    else:
                        print("请输入正确的文件路径！")
                        divide()
            choose[choose_index](in_path, out_path)
            print("处理成功！")
            divide()
            break

# 运行主程序入口


def main():
    while True:
        # 程序运行前，必须执行这一步，初始化所用的常量到内存中。
        config_constant.init_all_constant()
        choose = {
            "1": ask_to_set_cloze,
            "2": ask_to_set_blanks_rate,
            "3": ask_to_set_words,
            "4": ask_to_set_cloze_index,
            "5": ask_to_sync_stop_words,
            "6": ask_to_set_root_path,
            "7": ask_to_operate_cloze,
            "8":""}
        start_description = "\n".join(["请选择以下操作[按序号]：",
                                       "1.建立填空",
                                       "2.自定义空格率",
                                       "3.自定义新词/关键词/停止词",
                                       "4.设置 anki 填空符索引",
                                       "5.更新本地停止词库",
                                       "6.自定义 anki_cloze_maker 文件根目录",
                                       "7.对填空符的操作",
                                       "8.结束程序运行"])
        choose_index = input(start_description + "\n")
        divide()
        if choose_index not in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            print("请输入正确的序号！")
            divide()
        else:
            if choose_index == "8":
                print("成功退出程序！")
                divide()
                break
            else:
                # 执行对应序号操作
                choose[choose_index]()


if __name__ == "__main__":
    main()