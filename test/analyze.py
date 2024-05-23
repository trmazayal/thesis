import pandas as pd
import matplotlib.pyplot as plt
import math

df = pd.read_csv('report.csv', usecols=[0,1,2], names=['timestamp','desired', 'actual'])
df.sort_values(by=['timestamp'])
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.groupby(pd.Grouper(key='timestamp', freq='1min')).mean()

fig,ax = plt.subplots(figsize=(8,5))

desired = pd.Series(df['desired'])
actual = pd.Series(df['actual'])

cpu_used_arr = []
cpu_idle_arr = []
cpu_degr_arr = []

cpu_used_sum = 0
cpu_idle_sum = 0
cpu_degr_sum = 0


for i in range(len(desired)):
  cpu_used_arr.append(min(desired[i], actual[i]))
  cpu_used_sum += min(desired[i], actual[i])

  cpu_idle_arr.append(actual[i] if actual[i] > desired[i] else cpu_used_arr[i])
  cpu_idle_sum += max(actual[i]-desired[i], 0)

  cpu_degr_arr.append(desired[i] if desired[i] > actual[i] else cpu_used_arr[i])
  cpu_degr_sum += max(desired[i]-actual[i], 0)


cpu_used = pd.Series(cpu_used_arr)
cpu_idle = pd.Series(cpu_idle_arr)
cpu_degr = pd.Series(cpu_degr_arr)

cpu_idle.plot(drawstyle="steps",ax=ax, visible=False)
ax.fill_between(cpu_idle.index, cpu_idle, facecolor='blue', alpha=1,step='pre', label="degradasi")

cpu_degr.plot(drawstyle="steps",ax=ax, visible=False)
ax.fill_between(cpu_degr.index, cpu_degr, facecolor='red', alpha=1,step='pre', label="degradasi")

cpu_used.plot(drawstyle="steps",ax=ax, visible=False)
ax.fill_between(cpu_used.index, cpu_used, facecolor='green', alpha=1,step='pre', label="degradasi")

