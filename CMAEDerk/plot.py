import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("log/CMAE/CMAE_lbf_9/data.csv")
df1 = pd.read_csv("log/CMAE/CMAE_lbf_8/data.csv")

r = list(df.iloc[1][1:])
r1 = list(df1.iloc[1][1:])
x = list(df.iloc[0][1:])
print(r[:3])

plt.plot(x[:len(r1)],r1)
plt.plot(x[:len(r1)],r[:len(r1)])
plt.legend(["CMAE", "Q Learning"], loc ="upper left")
plt.title("Push Box")
plt.show()