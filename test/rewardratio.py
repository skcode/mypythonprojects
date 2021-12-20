import numpy as np
n=10
finaleq=1.59
r=0.07
print("annual reward=",np.exp(np.log(finaleq)/n)-1, "with ",n," years and finaleq ",finaleq)
print("annualities=",np.log(finaleq)/np.log(1+r), "with ",r," yearly returns and finaleq ",finaleq)
print("final eq=",np.float_power((1 + r), n), "with ",n," years and yearly return ",r)
