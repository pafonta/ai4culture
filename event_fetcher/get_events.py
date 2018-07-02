import pandas as pd
import numpy as np


df= pd.read_csv("filtered.csv")
# print(df)

for i in range(len(df)):
    print(i)
    print(df["title"][i])
    print(df["tags"][i])
    print(df["category_id"][i])
    print(df["category_name"][i])
    print("======================")
    x= input()
