from __future__ import division
from pyomo.core.expr.current import identify_variables
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from pyomo.environ import *
from pyomo_mcpp import McCormick as mc
from pyomo_spectral import Spectral as sbmc
import numpy as np
import math
import timeit

m = ConcreteModel()
m.x = Var(bounds = (-2, 2), initialize = 1)
m.e = Expression(expr = cos(m.x))

def underestimator(m):
    eqn = sbmc(m.e.expr)
    alpha = eqn.specbnd_l()
    m.temp = 0
    for i in m.component_data_objects(ctype=Var,
                                           active=True,
                                           descend_into=True):
        m.temp = m.temp + (i.lb - i) * (i.ub - i)
    #L(x) = f(x) + alph * summ_i((x^L_i - x_i)(x^U_i - x_i))
    beta = alpha * m.temp
    return Expression(expr = m.e + beta)

def overestimator(m):
    eqn = sbmc(m.e.expr)
    alpha = eqn.specbnd_u()
    m.temp = 0
    for i in m.component_data_objects(ctype=Var,
                                           active=True,
                                           descend_into=True):
        m.temp = m.temp + (i.lb - i) * (i.ub - i)
    #L(x) = f(x) + alph * summ_i((x^L_i - x_i)(x^U_i - x_i))
    beta = alpha * m.temp
    return Expression(expr = m.e + beta)

m.eqn1 = underestimator(m)
m.eqn2 = overestimator(m)
print(m.eqn1.expr)
print(m.eqn2.expr)