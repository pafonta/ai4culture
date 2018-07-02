import pandas as pd
import numpy as np


events= pd.read_csv("filtered.csv")
# print(df)

keys= pd.read_csv("keywords.csv")
keys= list(keys["Keywords"])
keys = [k.lower() for k in keys]

def match(tag_string):
    for i in range(len(keys)):
        tag_words = tag_string.split(" ")
        for word in tag_words:
            if word.lower() in keys:
                return True


LIST= []
for i in range(len(events)):
    m= match(events["tags"][i])
    if m:
        LIST.append(i)

print(LIST)
print(len(LIST))
print((float(len(LIST))/len(events))*100.0)

#

for i in LIST:
    print(i)
    print(events["title"][i])
    print(events["address"][i])
    print("======================")
    x= input()
