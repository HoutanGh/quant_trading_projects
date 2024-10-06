import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf

df = yf.download('^GSPC', start='2010-01-01', end='2023-01-01')
ma1 = 50
ma2 = 200
df['ma1'] = df['Adj Close'].rolling(window=ma1, min_periods=1, center=False).mean()
df['ma2'] = df['Adj Close']. rolling(window=ma2, min_periods=1, center=False).mean()


# they're obviously gonna be the same at the start, silly me
# print(sum(df['ma1']-df['ma2']))

# if df['ma1'].equals(df['ma2']):
#     print("The 'ma1' and 'ma2' columns are identical.")
# else:
#     print("The 'ma1' and 'ma2' columns are different.")

# print(df.head())

df['positions'] = 0

df['positions'][ma1:] = np.where(df['ma1'][ma1:]>=df['ma2'][ma1:], 1, 0)

df['signals'] = df['positions'].diff()
# print(df)
# print(sum(df['positions']))

df['oscillator'] = df['ma1'] - df['ma2']

# print(df)

fig, axs = plt.subplots(2, 2, figsize=(10, 8))
axs[0, 0].plot(df['Adj Close'], label='GSPC')
axs[0, 0].plot(df.loc[df['signals']==1]. index, df['Adj Close'][df['signals']==1], label = 'LONG', lw=0, marker='^', c='g')
axs[0, 0].plot(df.loc[df['signals']==-1]. index, df['Adj Close'][df['signals']==-1], label = 'SHORT', lw=0, marker='v', c='r')

axs[0, 0].legend(loc='best')
axs[0, 0].grid(True)
axs[0, 0].set_title('Positions')


axs[0, 1].bar(df.index, df['oscillator'], label = 'Oscillator (MA1 - MA2)', color='orange')
axs[0, 1].legend(loc='best')
axs[0, 1].grid(True)
axs[0, 1].set_xticks([])
axs[0, 1].set_xlabel('')
axs[0, 1].set_title('MACD Oscillator')

axs[1, 1].plot(df['ma1'],label='ma1')
axs[1, 1].plot(df['ma2'],label='ma2', linestyle=':')
axs[1, 1].legend(loc='best')
axs[1, 1].grid(True)

plt.show()

# debugging
# print(df.isna().sum())
# print(f"ONE SIGNALS:\n{df[df['signals'] == 1]}")
# print(f"MINUS SIGNALS: {df[df['signals'] == -1]}")



