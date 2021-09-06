import pandas as pd

train_filename = "pinyin2hanzi.txt"
save_filename = "pinyin2hanzi.csv"

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

df = pd.DataFrame(columns=['pinyin','words'])

cnt = 0
def insert(pinyin,words):
    global cnt
    new_line = [pinyin,words]
    df.loc[cnt] = new_line
    cnt+=1

for line in lineslist:
    pinyin,words = line.split(" ")
    insert(pinyin,words)

df.to_csv(save_filename)
print("Done")