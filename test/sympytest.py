import sympy as sp
import  numpy
from PyQt5.QtWidgets import *
import sympy.printing as printing
x,y=sp.symbols("x y")
expr=x**2-2*x*y + y**2+3
print("-"*50)
sp.pprint(expr)
print("-"*50)
eq=sp.Eq(expr,0)
sp.pprint(eq)
sp.pprint(sp.solve(eq,'y'))
print("-"*50)
sp.pprint(sp.diff(expr,x))
print("-"*50)
sp.pprint(sp.integrate(expr,x))

eq=sp.Eq(sp.pi**(1-x),sp.exp(1)**x)
sp.pprint(sp.solve(eq,x))