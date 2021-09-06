#coding=utf-8
import pandas as pd
import math

train_filename = 'lexicon.txt'
save_filename = 'fashe.csv'
cnt = 0

#保存格式（字，拼音，概率）
df = pd.DataFrame(columns=['zi','pinyin','gailv'])

def insert(zi,pinyin,gailv):
    global cnt
    new_line = [zi,pinyin,gailv]
    df.loc[cnt] = new_line
    cnt+=1

#按行读取
def ReadTxtName(rootdir):
    lines = []
    with open(rootdir, 'r',encoding='UTF-8') as file_to_read:
        while True:
            line = file_to_read.readline()
            if not line:
                break
            line = line.strip('\n')
            lines.append(line)
    return lines

#数据读取
lineslist=ReadTxtName(train_filename)
dict_count = {}

for line in lineslist:
    words,pinyins = line.split('	')
    pinyins = pinyins.split(' ')
    for i in range(len(words)):
        word = words[i]
        pinyin = pinyins[i][:-1]
        haxi = word+"-"+pinyin
        if haxi in dict_count:
            dict_count[haxi] += 1
        else:
            dict_count[haxi] = 1


tot = 0
for key in dict_count:
    tot+=dict_count[key]
print("tot:",tot)

#统计概率
for key in dict_count:
    word,pinyin = key.split('-')
    #防止概率过小对概率进行对数运算
    gailv = math.log(dict_count[key]/tot)
    #插入到表中
    insert(word,pinyin,gailv)

#保存
df.to_csv(save_filename, encoding='utf_8_sig')







