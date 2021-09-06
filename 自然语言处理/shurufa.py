import pandas as pd

fashe_filename = "fashe.csv"
chushi_filename = "chushi.csv"
zhuanyi_filename = "zhuanyi.csv"
ptoh_filename = "pinyin2hanzi.csv"

df_fashe = pd.read_csv(fashe_filename)
df_chushi = pd.read_csv(chushi_filename)
df_zhuanyi = pd.read_csv(zhuanyi_filename)
df_ptoh = pd.read_csv(ptoh_filename)

# for i in df_fashe[(df_fashe.pinyin == 'ti') & (df_fashe.zi == 'T')].get('gailv'):
#      print(i)
# print(len(df_fashe[(df_fashe.pinyin == 'ti2') & (df_fashe.zi == 'T')])==0)


def shurufa(pinyinlist):
    sentence = ''
    #寻找最大概率的第一个字
    firstpinyin = pinyinlist[0]
    df_firstwords = df_ptoh[df_ptoh.pinyin == firstpinyin].get('words')
    firstwords = ''
    for i in df_firstwords:
        firstwords = i
    maxgailv = -100000
    maxfirstword = ''
    for firstword in firstwords:
        fashegailv = -100
        chushigailv = -100
        df_fashegailv = df_fashe[(df_fashe.zi == firstword) & (df_fashe.pinyin == firstpinyin)].get('gailv')
        for i in df_fashegailv:
            fashegailv = i
        df_chushigailv = df_chushi[(df_chushi.zi == firstword)].get('gailv')
        for i in df_chushigailv:
            chushigailv = i
        #log(a)+log(b) = log(a*b)
        totgailv = fashegailv+chushigailv
        if totgailv-maxgailv > 0 :
            maxgailv = totgailv
            maxfirstword = firstword
    sentence += maxfirstword
    #print('first:',sentence)
    beforeword = maxfirstword
    for pinyin in pinyinlist[1:]:
        df_words = df_ptoh[df_ptoh.pinyin == pinyin].get('words')
        words = ''
        for i in df_words:
            words = i
        maxgailv = -100000
        maxword = ''
        for word in words:
            fashegailv = -100
            zhuanyigailv = -100
            df_fashegailv = df_fashe[(df_fashe.zi == word) & (df_fashe.pinyin == pinyin)].get('gailv')
            for i in df_fashegailv:
                fashegailv = i
            df_zhuanyigailv = df_zhuanyi[(df_zhuanyi.first == beforeword) & (df_zhuanyi.second == word)].get('gailv')
            for i in df_zhuanyigailv:
                zhuanyigailv = i
            #log(a)+log(b) = log(a*b)
            totgailv = fashegailv + zhuanyigailv
            if totgailv - maxgailv > 0:
                maxgailv = totgailv
                maxword = word
        sentence += maxword
        #print('after:', sentence)
        beforeword = word
    return sentence

pinyinlist = ['ni','hao','a']
print(pinyinlist)
print(shurufa(pinyinlist))
pinyinlist = ['jin','tian','wan','shang','you','hao','kan','de','dian','ying']
print(pinyinlist)
print(shurufa(pinyinlist))
pinyinlist = ['ni', 'de', 'shi', 'jie', 'hui', 'bian', 'de', 'geng', 'jing', 'cai']
print(pinyinlist)
print(shurufa(pinyinlist))



