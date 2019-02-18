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


#m = ConcreteModel()
#m.x = Var(bounds = (math.pi/6, math.pi/3), initialize = math.pi/6)
#m.e = Expression(expr = cos(pow(m.x, 2))*sin(pow(m.x,-3)))
m = ConcreteModel()
m.x = Var(bounds = (-2, 1), initialize = -1)
m.y = Var(bounds = (-1, 2), initialize = 0)
m.e = Expression(expr = m.x*pow(exp(m.x)-m.y,2))

eqn = sbmc(m.e.expr)
#print(eqn.specbnd_u())
print(eqn.specbnd_l())
alpha = eqn.specbnd_l()

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


'''def f(x, y):
    m.eqn = underestimator(m)
    x1 = m.x.value
    y1 = m.y.value
    m.x.set_value(x)
    m.y.set_value(y)
    ans = value(m.eqn)
    m.x.set_value(x1)
    m.y.set_value(y1)
    return ans'''
m.eqn1 = underestimator(m)
m.eqn2 = overestimator(m)
print(m.eqn1.expr)
print(m.eqn2.expr)

def f(x, y):
    return (x*(np.exp(x) - y)**2) - 105.662108841*((-2 - x)*(1 - x) + (-1 - y)*(2 - y))

def f2(x, y):
    return (x*(np.exp(x) - y)**2) + 78.7466282119*((-2 - x)*(1 - x) + (-1 - y)*(2 - y))

def make3dPlotSBMC(expr, space, affineptx = None, affinepty = None):
    ccSurf = []
    cvSurf = []
    fvals = []
    xaxis2 = []
    yaxis2 = []
    ccAffine = []
    
    eqn = sbmc(expr)
    x = list(identify_variables(expr))[0]
    y = list(identify_variables(expr))[1]
    xaxis = np.linspace(x.lb, x.ub, space)
    yaxis = np.linspace(y.lb, y.ub, space)
    
    if (affineptx != None):
        eqn.changePoint(x, affineptx)
        x.set_value(affineptx)
    if (affinepty != None):
        eqn.changePoint(y, affinepty)
        y.set_value(affinepty)

    #Making the affine tangent planes
    ccSlope = eqn.subcc()
    cvSlope = eqn.subcv()
    ccTanPlane = ccSlope[x]*(xaxis - value(x)) + ccSlope[y]*(yaxis - value(y)) + eqn.concave()
    cvTanPlane = cvSlope[x]*(xaxis - value(x)) + cvSlope[y]*(yaxis - value(y)) + eqn.convex()
    
    #To Visualize Concave Affine Plane for different points
    for i in xaxis:
        for j in yaxis:
            ccAffine += [ccSlope[x]*(i - value(x)) + ccSlope[y]*(j - value(y)) + eqn.concave()]
    
    #Making the fxn surface (fvals) and cc and cv surfaces
    for i in xaxis:
        eqn.changePoint(x, i)
        for j in yaxis:
            xaxis2 += [i]
            yaxis2 += [j]
            eqn.changePoint(y, j)
            ccSurf += [eqn.concave()]
            cvSurf += [eqn.convex()]
            fvals += [value(expr)]
            
    #Plotting Solutions in 3D
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1, projection='3d')
    xaxis, yaxis = np.meshgrid(xaxis, yaxis)
    ax.scatter(xaxis2, yaxis2, cvSurf, color = 'b')
    ax.scatter(xaxis2, yaxis2, fvals, color = 'r')
    ax.scatter(xaxis2, yaxis2, ccSurf, color = 'b')
    #ax.plot_surface(xaxis, yaxis, ccTanPlane, color = 'k')
    ax.plot_surface(xaxis, yaxis, cvTanPlane, color = 'k')
    
    #To Visualize Concave Affine Plane for different points
    ax.scatter(xaxis2, yaxis2, ccAffine, color = 'k')
    
    #Plot Closed-Form Soln
    ax.plot_surface(xaxis, yaxis, f(xaxis, yaxis), color = 'g')
    ax.plot_surface(xaxis, yaxis, f2(xaxis, yaxis), color = 'g')

    #Create a better view
    ax.view_init(0,270)
    plt.show()

#print(f(1, 1))
make3dPlotSBMC(m.e.expr, 30, affineptx = -1, affinepty = 0)






