import pandas as pd
import matplotlib.pyplot as plt
import math
import sys

# Percentage of shared resource allowed
alpha = 0.0

# if len(sys.argv) > 1:
#     alpha = float(sys.argv[1])

df = pd.read_csv('report.csv', usecols=[0,1,2], names=['timestamp','desired', 'actual'])
df.sort_values(by=['timestamp'])
df['timestamp'] = pd.to_datetime(df['timestamp'],format='mixed')
df = df.groupby(pd.Grouper(key='timestamp', freq='1min')).mean()

fig,ax = plt.subplots(figsize=(8,5))

desired = pd.Series(df['desired'])
actual = pd.Series(df['actual'])

cpu_used_arr = []
cpu_idle_arr = []
cpu_degr_arr = []
cpu_shared_arr = []

cpu_guaranteed_sum = 0
cpu_shared_sum = 0
cpu_degradation_sum = 0

for i in range(len(desired)):
  cpu_used_arr.append(min(desired[i], actual[i]))
  cpu_idle_arr.append(actual[i] if actual[i] > desired[i] else 0.0)
  cpu_degr_arr.append(desired[i] if desired[i] > actual[i]*(1.0+alpha) else 0.0)
  cpu_shared_arr.append(min(desired[i], actual[i]*(1.0+alpha)) if desired[i] > actual[i] else 0.0)

  cpu_guaranteed_sum += actual[i]
  cpu_shared_sum += min(desired[i]-actual[i], actual[i]*alpha) if desired[i] > actual[i] else 0
  cpu_degradation_sum += max(desired[i]-actual[i]*(1.0+alpha), 0)

cpu_used = pd.Series(cpu_used_arr)
cpu_idle = pd.Series(cpu_idle_arr)
cpu_shared = pd.Series(cpu_shared_arr)
cpu_degr = pd.Series(cpu_degr_arr)

cpu_idle.plot(drawstyle="steps",ax=ax, visible=False)
ax.fill_between(cpu_idle.index, cpu_idle, facecolor='blue', alpha=1,step='pre', label="idle")

cpu_degr.plot(drawstyle="steps",ax=ax, visible=False)
ax.fill_between(cpu_degr.index, cpu_degr, facecolor='red', alpha=1,step='pre', label="degradasi")

cpu_shared.plot(drawstyle="steps",ax=ax, visible=False)
ax.fill_between(cpu_shared.index, cpu_shared, facecolor='yellow', alpha=1,step='pre', label="shared")

cpu_used.plot(drawstyle="steps",ax=ax, visible=False)
ax.fill_between(cpu_used.index, cpu_used, facecolor='green', alpha=1,step='pre', label="terpakai")

print("CPU Guaranteed", cpu_guaranteed_sum)
print("CPU Shared", cpu_shared_sum)
print("CPU Degradation", cpu_degradation_sum)