#交互式生成填空的文本。

from process_words import *
import jieba.analyse

def get_all_tag_words(text):
    """
    获取关键词(tag_word.txt+jieba的tf-idf算法)。
    :param text：输入tf-idf算法待提取关键词的文本。
    :return: 返回关键词的集合all_tag_words,以及相应文本的预期空格数blanks_count。
    """
    #获取自定义的空格数。
    blanks_count=get_valid_blanks_count(text)

    #jieba的tf-idf算法分析的关键词，这里最先导入停止词库。
    jieba.analyse.set_stop_words(STOP_WORDS_PATH)
    tf_idf_tag_words = jieba.analyse.extract_tags(text, topK=blanks_count, withWeight=False, allowPOS=())
    tf_idf_tag_words=set(tf_idf_tag_words)

    #tag_words.txt自定义的关键词。
    custom_tag_words= open_file(TAG_WORDS_PATH,"r")

    #生成所有的关键词。
    all_tag_words=tf_idf_tag_words| custom_tag_words

    return all_tag_words,blanks_count

def get_seged_words(text):
    """
    获取用jieba按新词库分词后的分词列表。
    :param text: 输入待分词的文本。
    :return: 分词后的分词列表。
    """
    # jieba导入新词库。
    jieba.load_userdict(NEW_WORDS_PATH)
    # 将文本分词。
    seged_words = list(jieba.cut(text, cut_all=False))
    return seged_words

def get_cloze_seged_words(text):
    """
    对给定的文本，获得添加填空后的分词列表。
    :param text: 输入待加填空的文本。
    :return: 添加填空的分词列表cloze_seged_words。
    """
    seged_words=get_seged_words(text)
    all_tag_words,blanks_count=get_all_tag_words(text)
    #对文本所找到关键词的缓存。
    tmp_tag_words=[]
    cloze_seged_words=[]
    count=0
    for seged_word in seged_words:
        if seged_word in all_tag_words:
            if seged_word in tmp_tag_words:
                word_index=tmp_tag_words.index(seged_word)+1
                seged_word = "".join(["{{c", str(word_index), "::", seged_word, "}}"])
            else:
                count+=1
                tmp_tag_words.append(seged_word)
                seged_word = "".join(["{{c", str(count), "::", seged_word, "}}"])
        cloze_seged_words.append(seged_word)

    text_tag_count=len(tmp_tag_words)
    if blanks_count >text_tag_count:
        print('你所期望的空格数为 %d 个，但超过系统找到的关键词数 %d 个。' % (blanks_count, text_tag_count))
    return cloze_seged_words

def ask_to_set_words():
    """
    交互式询问添加新词/关键词/停止词的操作。
    :return: 无。
    """
    answer = input("请添加新词/关键词/停止词。[new/tag/stop ...(添加的词用空格分开)]\n")
    answer_list = answer.split(" ")
    operator = answer_list[0]
    words = set(answer_list[1:])
    if operator == "tag":
        set_tag_words(words)
    elif operator == "stop":
        set_stop_words(words)
    elif operator =="new":
        open_file(NEW_WORDS_PATH,"a",words)
    print("添加成功！\n")

def save_cloze_text(in_path,out_path):
    """
    保存批量添加填空的文本。
    :param in_path: 待添加填空的.txt文件路径。
    :param out_path:输出填空的.txt文件路径。
    :return: 无。
    """
    with open(in_path,"r",encoding="utf-8") as f:
        in_lines=f.readlines()
        in_lines=[in_line.strip("\n") for in_line in in_lines]
        cloze_out_lines=[]
        for in_line in in_lines:
            while True:
                cloze_out_line = "".join(get_cloze_seged_words(in_line))
                print("经处理后的anki填空形式的分词列表：")
                print(cloze_out_line)
                answer=input("是否需要继续修改？[y/n]\n")
                if answer=="y":
                    ask_to_set_words()
                elif answer=="n":
                    cloze_out_lines.append(cloze_out_line)
                    break
            print("-----------------------------------------------------------")
            answer=input("是否自动将修改应用到所有文本？[y/n]\n")
            if answer=="y":
                cloze_out_lines=[]
                for in_line in in_lines:
                    cloze_out_line = "".join(get_cloze_seged_words(in_line))
                    cloze_out_lines.append(cloze_out_line)
                break
            print("-----------------------------------------------------------")
        cloze_out_lines=["".join([cloze_out_line,"\n"]) for cloze_out_line in cloze_out_lines]
        cloze_out_lines[-1]=cloze_out_lines[-1].strip("\n")
        with open(out_path,"w",encoding="utf-8") as m:
            m.writelines(cloze_out_lines)
            print("成功保存输出的文件名为 "+out_path+" !")

if __name__ == "__main__":
    set_blanks_percent(2,40)
    save_cloze_text("a.txt","b.txt")