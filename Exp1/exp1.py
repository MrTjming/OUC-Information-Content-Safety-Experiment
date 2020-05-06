import re

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
    for one in sorted(map.items(), key=lambda item: item[1]):
        print(one[0],":",one[1])
    return {"map": map, "max_len": max_len}


# 打印结果
def my_print(res):
    for word in res:
        if word == "" or word == " ":
            continue
        if word == '\r\n' or word == '\r' or word == '\n':
            print(word, end="")
        else:
            print(word + "/", end="")


def fmm(helper, string):
    map = helper["map"]
    max_len = helper["max_len"]
    res = []
    str_len = len(string)

    l = 0
    r = max_len
    while l < str_len:
        if (r > str_len):
            r = str_len
        if l + 1 == r:
            res.append(string[l:r])
            l = r
            r = l + max_len
        elif map.get(string[l:r]) != None:
            res.append(string[l:r])
            l = r
            r = l + max_len
        else:
            r = r - 1

    my_print(res)
    return res


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


def main():
    helper = calc_word_frequency()
    str = '''祝愿祖国明天更加繁荣昌盛 香港大学生在京度佳节 
新华社北京１月１日电 
昨晚，第一次来到首都北京的５０多名香港大学生，和北京航空航天大学的同学们在《歌唱祖国 》的歌声中一起迎接１９９８年的到来。
此次到京的香港大学生来自香港科技大学和浸会大学，他们于１２月３０日抵京后  参观了北大、清华和抗日战争纪念馆。在中国青年政治学院，两地大学生就学习、生活等共同关心的话题展开了交流。
'''
    print("原文:")
    print(str)

    print("fmm:")
    fmm(helper, str)

    print("\nbmm:")
    bmm(helper, str)


if __name__ == '__main__':
    main()
