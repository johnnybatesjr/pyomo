
from __future__ import division
from pyomo.core.expr.current import identify_variables
import matplotlib.pyplot as plt
from pyomo.environ import *
from pyomo_mcpp import McCormick as mc
from pyomo_spectral import Spectral as sbmc
import numpy as np
import math

m = ConcreteModel()
m.x = Var(bounds = (math.pi/6, math.pi/3), initialize = math.pi/6)
m.e = Expression(expr = cos(pow(m.x, 2))*sin(pow(m.x,-3)))


def make2dMCPlot(expr, tickSpace, affinept = None):
    mc_ccVals = []
    mc_cvVals = []
    aff_cc = []
    aff_cv = []
    fvals = []
    eqn = mc(expr)
    x = list(identify_variables(expr))[0]
    xaxis = np.arange(x.lb, x.ub, tickSpace)
    if (affinept != None):
        eqn.changePoint(x, affinept)
        x.set_value(affinept)
    cc = eqn.subcc()
    cv = eqn.subcv()
    for i in xaxis:
        aff_cc += [cc[x]*(i - value(x)) + eqn.concave()]
        aff_cv += [cv[x]*(i - value(x)) + eqn.convex()]
    for i in xaxis:
        eqn.changePoint(x, i)
        mc_ccVals += [eqn.concave()]
        mc_cvVals += [eqn.convex()]
        fvals += [value(expr)]
    plt.plot(xaxis, fvals, 'r', xaxis, mc_ccVals, 'b--', xaxis, mc_cvVals, 'b--', xaxis, aff_cc, 'k|', xaxis, aff_cv, 'k|')
    plt.show()

def make2dSBMCPlot(expr, tickSpace, affinept = None):
    mc_ccVals = []
    mc_cvVals = []
    aff_cc = []
    aff_cv = []
    fvals = []
    eqn = sbmc(expr)
    x = list(identify_variables(expr))[0]
    xaxis = np.arange(x.lb, x.ub, tickSpace)
    if (affinept != None):
        eqn.changePoint(x, affinept)
        x.set_value(affinept)
    cc = eqn.subcc()
    cv = eqn.subcv()
    for i in xaxis:
        aff_cc += [cc[x]*(i - value(x)) + eqn.concave()]
        aff_cv += [cv[x]*(i - value(x)) + eqn.convex()]
    for i in xaxis:
        eqn.changePoint(x, i)
        mc_ccVals += [eqn.concave()]
        mc_cvVals += [eqn.convex()]
        fvals += [value(expr)]
    #plt.plot(xaxis, fvals, 'r', xaxis, mc_ccVals, 'b--', xaxis, mc_cvVals, 'b--', xaxis, aff_cc, 'k|', xaxis, aff_cv, 'k|')
    plt.plot(xaxis, fvals, 'r')
    plt.show()
make2dMCPlot(m.e.expr, 0.01, 0.78)
make2dSBMCPlot(m.e.expr, 0.01, 0.78)





