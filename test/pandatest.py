import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

M=np.random.random([5,3])
print(M)
print(np.arange(6).reshape([3,2]))
df=pd.DataFrame(columns=['a','b'],data=np.arange(6).reshape([3,2]),dtype=float)
print(df)
print( df.where(df['a']>1).dropna())
df.loc[df['a']>1,'b']=0
print(df)
