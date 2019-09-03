# 按拼音和笔画排序中文字符。

from constant import *


def init_pinyin_dict(path):
    # 建立拼音辞典
    dict_py = dict()
    with open(path, 'r', encoding='utf-8') as f:
        content_py = f.readlines()
        for i in content_py:
            i = i.strip()
            word_py, mean_py = i.split('\t')
            dict_py[word_py] = mean_py
    return dict_py


def init_bihua_dict(path):
    # 建立笔画辞典
    dict_bh = dict()
    with open(path, 'r', encoding='utf-8') as f:
        content_bh = f.readlines()

        for i in content_bh:
            i = i.strip()
            word_bh, mean_bh = i.split('\t')
            dict_bh[word_bh] = mean_bh
    return dict_bh


# 辞典查找函数
def searchdict(dic, uchar):
    if u'\u4e00' <= uchar <= u'\u9fa5':
        value = dic.get(uchar)
        if value == None:
            value = '*'
    else:
        value = uchar
    return value


# 比较单个字符
def comp_char_PY(A, B, dict_py, dict_bh):
    if A == B:
        return -1
    pyA = searchdict(dict_py, A)
    pyB = searchdict(dict_py, B)

    # 比较拼音
    if pyA > pyB:
        return 1
    elif pyA < pyB:
        return 0

    # 比较笔画
    else:
        bhA = eval(searchdict(dict_bh, A))
        bhB = eval(searchdict(dict_bh, B))
        if bhA > bhB:
            return 1
        elif bhA < bhB:
            return 0
        else:
            return "拼音相同，笔画也相同？"


# 比较字符串
def comp_char(A, B, dict_bh, dict_py):
    n = min(len(A), len(B))
    i = 0
    result = 0
    while i < n:
        dd = comp_char_PY(A[i], B[i], dict_py, dict_bh)
        # 如果第一个单词相等，就继续比较下一个单词
        if dd == -1:
            i = i + 1
            # 如果比较到头了
            if i == n:
                dd = len(A) > len(B)
        else:
            result = dd
            break
    return result


# 排序函数
def cnsort(nline):
    dict_bh = init_bihua_dict(config_constant.CHINESE_BIHUA_PATH)
    dict_py = init_pinyin_dict(config_constant.CHINESE_PINYIN_PATH)
    n = len(nline)
    lines = "\n".join(nline)

    for i in range(1, n):  # 插入法
        tmp = nline[i]
        j = i
        while j > 0 and comp_char(nline[j - 1], tmp, dict_bh, dict_py):
            nline[j] = nline[j - 1]
            j -= 1
        nline[j] = tmp
    return nline


if __name__ == "__main__":
    # 排序中文字符
    tag_sort = cnsort(["人民", "太阳", "人们", "太"])
    print('输出：', tag_sort)
