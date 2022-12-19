import pandas as pd
import os

# os.chdir("/mnt/c/Users/conog/Desktop")

# df1 = pd.read_csv("Dataframe_1.csv")
# df2 = pd.read_csv("Dataframe_2.csv")
# df3 = pd.read_csv("Dataframe_3.csv")

# value1 = "PRJNA515382"
# value2 = "SRS1505138"
# value3 = "PRJNA723064"

# if value1 in df1.values :
#     print(f"\n{value1} exists in Dataframe1")
# elif value2 in df1.values :
#     print(f"\n{value2} exists in Dataframe1")
# elif value3 in df1.values :
#     print(f"\n{value3} exists in Dataframe1")
# else:
#     print("no values found for df1")

# if value1 in df2.values :
#     print(f"\n{value1} exists in Dataframe2")
# elif value2 in df2.values :
#     print(f"\n{value2} exists in Dataframe2")
# elif value3 in df2.values :
#     print(f"\n{value3} exists in Dataframe2")
# else:
#     print("no values found for df2")

# if value1 in df3.values :
#     print(f"\n{value1} exists in Dataframe3")
# elif value2 in df3.values :
#     print(f"\n{value2} exists in Dataframe3")
# elif value3 in df3.values :
#     print(f"\n{value3} exists in Dataframe3")
# else:
#     print("no values found for df3")
 



import re

str_list = 'ERS4202782-ERS4202789'
# chr: il primo match di qualsiasi gruppo di lettere in str_list
chr = (re.search(r'[a-zA-Z]+', str_list)).group(0)
# ranges: una lista di due elementi, il primo numero e il secondo numero del range str_list. [4202782, 4202789]
# è solo un findall di tutti i numeri dentro str, con int applicato su entrambi
ranges = list(map(int, re.findall(r'\d+', str_list)))  
# # per la nuova lista assembla chr e i per ogni i nel range che parte 
# # dal primo numero fino al secondo + 1 per comprenderlo
new_list = ([f'{chr}{i}' for i in range(ranges[0], ranges[1]+1)])

print(new_list)

