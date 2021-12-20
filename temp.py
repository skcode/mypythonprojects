import math
import numpy as np
import matplotlib.pyplot as plt

def autocompound(capital=100, apr=0.15, n_compound=12):
    equity = capital
    rew4sample = 1 / n_compound
    apr4samples = apr * rew4sample
    for i in range(0, n_compound):
        equity = equity * (1 + apr4samples)
    return equity


def primes(n=100):
    l = [1, 2, 3]
    c = 4
    while len(l) < n:
        isprime = True
        for j in l[1:]:
            if (c % j) == 0:
                isprime = False
        if isprime:
            l.append(c)
        c = c + 1
    return l


def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)

def mylist(*lst):
    l=[]
    for x in lst:
        l.append(x)
    return l

def mydic(**dct):
    d={}
    for k,v in dct.items():
        d[k]=v
    return d
###################################



class Security:
    Markets = ('NYSE', 'MLSE', 'XETRA', 'EURONEXT','OTC')
    Type=('STOCK','BOND','INDEX','FUTURE','ETF','ETC','OPTION','CERTIFICATE','CRYPTO')
    def __init__(self, name, description, mkts, tp):
        self.__name = name#double underscore to make attribute private
        self.__description = description
        if type(mkts) is tuple:
            for x in mkts:
                if x not in Security.Markets:
                    raise RuntimeError("markets not found")
            self.__mkts=mkts
        else:
            raise RuntimeError('not a tuple')
        self.__type=tp
    def get_name(self):
        return self.__name
    def get_description(self):
        return self.__description


if __name__ == '__main__':
    print(autocompound())
    print(primes(10))
    print(factorial(5))
    print(mylist('ciao','cacca','bello'))
    print(mydic(nome='ettore',cognome='mastrogiacomo',caratteristica='bello'))
    s=Security('microsoft','bill',('NYSE','XETRA'),'STOCK')
    print(s.get_name())
    f1 = lambda x: x*x
    print([f1(x) for x in np.arange(10)])

    fig,ax =plt.subplots(1,2,figsize=(12,4))
    x=np.linspace(start=0.01, stop=2*math.pi)
    for axs in ax:
        axs.spines['bottom'].set_color('black')
        axs.spines['bottom'].set_linewidth(2)
        axs.spines['bottom'].set_position(('data', 0))
        axs.spines['left'].set_color('black')
        axs.spines['left'].set_linewidth(2)
        axs.spines['left'].set_position(('data', 0))
        axs.grid(True)

    ax[0].plot(x,np.sin(x),label=r"$y = \sin(x)$")
    ax[0].plot(x, np.cos(x), label=r"$y = \cos(x)$")
    ax[0].legend(loc=3)
    ax[0].axis('tight')
    ax[1].plot(x,np.log(x),label=r"$y = \log(x)$")
    ax[1].legend(loc=4)
    ax[1].axis('tight')
    plt.show()