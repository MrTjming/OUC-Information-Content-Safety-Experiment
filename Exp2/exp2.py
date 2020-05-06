import re
import math

lines=[]
# 分割每行内容,去掉词性标记等无关内容
def spilt_word(string):
    p = re.compile(r'[ ]{2}(.*?)[//]', re.S)
    return re.findall(p, string)


# 获取词频
def calc_word_frequency():
    max_len = 0
    map = {}
    with open("语料库.txt", "r", encoding='utf') as f:
        for line in f.readlines():
            words = spilt_word(line)
            for word in words:
                max_len = len(word) if len(word) > max_len else max_len
                if map.get(word) is None:
                    map[word] = 1
                else:
                    map[word] = map.get(word) + 1

    # 按照词频从小到大排序输出
    # for one in sorted(map.items(), key=lambda item: item[1]):
    #     print(one[0],":",one[1])
    return {"map": map, "max_len": max_len}


# 获取每一行的词频tf
def calc_word_frequency_of_per_line():
    line_num = 0
    TFs = []
    IDFs = {}

    with open("语料库.txt", "r", encoding='utf') as f:
        for line in f.readlines():
            lines.append(line)
            line_num += 1
            tf = {}
            words = spilt_word(line)
            word_num = 0
            for word in words:
                word_num += 1

                def increase(di, key):
                    if di.get(key) is None:
                        di[key] = 1
                    else:
                        di[key] = di.get(key) + 1

                increase(IDFs, word)
                increase(tf, word)

            for key in tf:
                tf[key] = tf[key] / word_num

            TFs.append(tf)

    for key in IDFs:
        IDFs[key] = math.log1p(line_num / IDFs[key])

    # 按照词频从小到大排序输出
    # for one in sorted(map.items(), key=lambda item: item[1]):
    #     print(one[0],":",one[1])
    return TFs, IDFs


# 计算TF-IDF
def calc_ft_idf_of_per_line(words, TFs, IDFs):
    res = []
    # 将TF-IDF的值求和
    for index,tf in enumerate(TFs):
        if_idf = 0
        for word in words:
            if word in tf:
                if_idf += tf[word] * IDFs[word]

        res.append([if_idf, lines[index]])

    # 将TF-IDF的值排序
    sortRes=sorted(res, key=lambda if_idf: if_idf[0], reverse=True)
    # 打印TF-IDF最大的10个结果
    for one in sortRes[:10]:
        print(one)
    return res


# 打印结果
def my_print(res):
    for word in res:
        if word == "" or word == " ":
            continue
        if word == '\r\n' or word == '\r' or word == '\n':
            print(word, end="")
        else:
            print(word + "/", end="")
    print()


def bmm(helper, string):
    map = helper["map"]
    max_len = helper["max_len"]
    res = []
    str_len = len(string)

    l = str_len - max_len
    r = str_len
    while r > 0:
        if (l < 0):
            l = 0
        if l + 1 == r:
            res.append(string[l:r])
            r = l
            l = r - max_len
        elif map.get(string[l:r]) != None:
            res.append(string[l:r])
            r = l
            l = r - max_len
        else:
            l = l + 1

    res.reverse()
    my_print(res)
    return res


if __name__ == '__main__':
    helper = calc_word_frequency()
    str = """中国世界杯夺冠"""
    print("原文:")
    print(str)

    print("\nbmm分词结果:")
    words = bmm(helper, str)
    TFs, IDFs = calc_word_frequency_of_per_line()
    calc_ft_idf_of_per_line(words, TFs, IDFs)
