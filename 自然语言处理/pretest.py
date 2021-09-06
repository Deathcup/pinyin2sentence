import pandas as pd

test_filename = "测试集.txt"
save_filename = 'test.csv'

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

lineslist=ReadTxtName(test_filename)

df = pd.DataFrame(columns=['pinyinlist','sentence'])
cnt = 0
def insert(pinyinlist,sentence):
    global cnt
    new_line = [pinyinlist,sentence]
    df.loc[cnt] = new_line
    cnt+=1

for i in range(0,len(lineslist),2):
    linepinyin = lineslist[i]
    linesentence = lineslist[i+1] 
    insert(linepinyin,linesentence)

df.to_csv(save_filename)
print(df)
