import pandas as pd 
import matplotlib.pyplot as plt

#code to make the 6 main graphs
# df = pd.read_csv("data3.csv") 
# df2 = pd.read_csv("data4.csv")
# print(df.loc[0])
# stepList = list()
# rewardList = list()
# rewardList2 = list()
# for i in range(len(df.loc[0])-1):
#     stepList.append(df.loc[0][i+1])
#     rewardList.append(df.loc[1][i+1])
#     rewardList2.append(df2.loc[1][i+1])
# plt.title("Secret Room (Dense Rewards)")
# plt.xlabel("# of env. steps")
# plt.ylabel("Evaluation Rewards")
# plt.plot(stepList, rewardList, label="CMAE")
# plt.plot(stepList, rewardList2, label="Epsilon")

#code to make the pressure plate graph
with open('./greedyData.txt') as f:
    lines = f.read().splitlines()
convertList = list()
for i in lines:
    convertList.append(int(i))
plt.title("Pressure Plate")
plt.xlabel("Episode")
plt.ylabel("# of steps to complete")
plt.plot(convertList, label="Greedy")
f.close()

plt.legend()
plt.show()