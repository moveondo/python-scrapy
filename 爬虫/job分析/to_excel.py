from json import JSONDecodeError
import pandas as pd
import json

with open('boss.json', 'r', encoding='utf-8') as f:
    lines = f.readlines()
lis = []
for line in lines:
    try:
        dic = json.loads(line)
        lis.append(dic)
        print(dic)
    except JSONDecodeError:
        print(line)
df = pd.DataFrame(lis)
df.to_excel('boss.xlsx')