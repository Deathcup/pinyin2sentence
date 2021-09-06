import pandas as pd
import math

train_filename = "toutiao_cat_data.txt"
save_filename = 'chushi.csv'

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

lineslist=ReadTxtName(train_filename)

#判断是否是中文
def is_chinese(uchar):
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False

#处理字符串只保留中文
def format_str(content):
    content_str = ''
    for i in content:
        if is_chinese(i):
            content_str = content_str+i
    return content_str

#统计转移概率
dict_count = {}
#t = 0
for line in lineslist:
    #t = t+1
    #print("处理行:",t)
    wordslist = line.split('_')
    wordslist = wordslist[7:]
    for words in wordslist:
        if(words == '!' ):
            continue
        words = format_str(words)
        if(words == ''):
            continue
        #print('words',words)
        haxi = words[0]
        if haxi in dict_count:
            dict_count[haxi] += 1
        else:
            dict_count[haxi] = 1

#保存为DataFrame形式
df = pd.DataFrame(columns=['zi','gailv'])
cnt = 0
def insert(start,gailv):
    global cnt
    new_line = [start,gailv]
    df.loc[cnt] = new_line
    cnt+=1

tot = 0
for key in dict_count:
    tot+=dict_count[key]

#概率计算
t = 0
for key in dict_count:
    t = t+1
    print('计算概率',t)
    start = key
    #防止概率过小对概率进行对数运算
    gailv = math.log(dict_count[key]/tot)
    #插入到表中
    insert(start,gailv)

#保存为csv
df.to_csv(save_filename, encoding='utf_8_sig')
print("运行结束")
