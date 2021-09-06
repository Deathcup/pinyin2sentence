import pandas as pd

#文件路径
fashe_filename = "fashe.csv"
chushi_filename = "chushi.csv"
zhuanyi_filename = "zhuanyi.csv"
ptoh_filename = "pinyin2hanzi.csv"
test_filename = "test.csv"

#读取csv文件到DataFrame
df_fashe = pd.read_csv(fashe_filename)
df_chushi = pd.read_csv(chushi_filename)
df_zhuanyi = pd.read_csv(zhuanyi_filename)
df_ptoh = pd.read_csv(ptoh_filename)
df_test = pd.read_csv(test_filename)

#创建字典
dict_fashe = {}
dict_chushi = {}
dict_zhuanyi = {}
dict_ptoh = {}

#把数据读入到字典中
for i in range(len(df_fashe)):
    haxi = str(df_fashe['zi'][i])+'-'+str(df_fashe['pinyin'][i])
    dict_fashe[haxi] = df_fashe['gailv'][i]

for i in range(len(df_chushi)):
    haxi = str(df_chushi['zi'][i])
    dict_chushi[haxi] = df_chushi['gailv'][i]

for i in range(len(df_zhuanyi)):
    haxi = str(df_zhuanyi['first'][i])+'-'+str(df_zhuanyi['second'][i])
    dict_zhuanyi[haxi] = df_zhuanyi['gailv'][i]

for i in range(len(df_ptoh)):
    haxi = str(df_ptoh['pinyin'][i])
    dict_ptoh[haxi] = df_ptoh['words'][i]

#viterbi算法实现输入法
def shurufa(pinyinlist):
    #状态图
    Graph = []
    for pinyin in pinyinlist:
        Graph.append(dict_ptoh[pinyin])
    #print(Graph)
    dict_start = {}
    #更新第一列状态 用初始概率乘发射概率
    for i in Graph[0]:
        #概率的缺省值
        chushigailv = -14
        fashegailv = -12
        if i in dict_chushi:
            chushigailv = dict_chushi[i]
        if i+'-'+pinyinlist[0] in dict_fashe:
            fashegailv = dict_fashe[i+'-'+pinyinlist[0]]
        #因为log(a)+log(b) = log(a*b) 用加法即可
        dict_start[str(i)] = chushigailv + fashegailv
    #print('chushi',dict_start)
    #前一列状态
    dict_before = dict_start
    #当前列状态
    dict_sentence = {}
    #遍历后面的列
    for i in range(1,len(Graph)):
        dict_sentence = {}
        #当前列的所有节点
        for word in Graph[i]:
            maxgailv = -1000000
            choice = ''
            #遍历前一列的所有路径并更新
            for key in dict_before:
                #概率的缺省值
                zhuanyigailv = -17
                fashegailv = -12
                if key[-1]+'-'+word in dict_zhuanyi:
                    zhuanyigailv = dict_zhuanyi[key[-1]+'-'+word]
                if word+'-'+pinyinlist[i] in dict_fashe:
                    fashegailv = dict_fashe[word+'-'+pinyinlist[i]]
                #计算概率
                gailv = dict_before[key]+zhuanyigailv+fashegailv
                #更新
                if gailv > maxgailv:
                    maxgailv = gailv
                    choice = key
            newkey = str(choice)+str(word)
            #print(newkey)
            dict_sentence[newkey] = maxgailv
        #将当前列状态变为前列状态
        dict_before = dict_sentence
        #print('after',dict_before)

    #寻找最后一列的最优路线
    resultgailv = -1000000
    resultsentence = ''
    for key in dict_sentence:
        if dict_sentence[key] > resultgailv:
            resultgailv = dict_sentence[key]
            resultsentence = key
    return resultsentence, resultgailv
        

#返回相同字的个数
def check(presentence,turesentence):
    cnt1 = 0
    for i in range(len(presentence)):
        if(presentence[i]==turesentence[i]):
            cnt1+=1
    return cnt1

#测试
def test():
    totcheck = 0
    tot = 0
    for i in range(len(df_test)):
        pinyinlist = df_test['pinyinlist'][i].split(' ')
        turesentence = df_test['sentence'][i]
        presentence,gailv = shurufa(pinyinlist)
        print(df_test['pinyinlist'][i])
        print('log(预测概率):',gailv)
        print('预测句子:',presentence)
        print('真实句子:',turesentence)
        print('准确率:',check(presentence,turesentence)/len(presentence))
        totcheck += check(presentence,turesentence)
        tot += len(presentence)
        print("-----------------------------------------------------------------")
    print("总体准确率为:",totcheck/tot)

test()
# test1 = 'ni jue de jin tian zen me yang'
# pinyinlist = test1.split(' ')
# sentence,gailv = shurufa(pinyinlist)

# print(test1)
# print(sentence)