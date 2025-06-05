# save this as connect.py
from ib_insync import *

ib = IB()
ib.connect('172.21.224.1', 4002, clientId=777)
print("Connected:", ib.isConnected())
ib.disconnect()
