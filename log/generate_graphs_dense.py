import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

dfq = pd.read_csv("CMAE/CMAE_ROOM_3_3/dataDenseQ.csv")
dfq = dfq.transpose()
dfcmae = pd.read_csv("CMAE/CMAE_ROOM_2_2/dataDenseCMAE.csv")
dfcmae = dfcmae.transpose()
# print(df)
stepq = []
eval_rewq = []
stepcmae = []
eval_rewcmae = []
for i in range(len(dfq)-1):
    stepq.append(dfq[0][i+1])
    eval_rewq.append(dfq[1][i+1])

for i in range(len(dfcmae)-1):
    stepcmae.append(dfcmae[0][i+1])
    eval_rewcmae.append(dfcmae[1][i+1])
# print('Step',step)
# print('RewardS', eval_rew)
plt.plot(stepq,eval_rewq, label = "Q Learning")
plt.plot(stepcmae,eval_rewcmae, label = "CMAE")
plt.legend()
# plt.xlim(100, 3700000)
# plt.ylim(0,1)
plt.title("Room / Pass")
plt.xlabel('Steps')
plt.ylabel('Reward')
sns.despine(top=True, right=True, left=False, bottom=False)
plt.show()