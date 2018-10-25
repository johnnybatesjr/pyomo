from __future__ import division

import logging
from math import pi

from six import StringIO

import pyutilib.th as unittest
from pyomo.common.log import LoggingIntercept
from pyomo.contrib.mcpp.pyomo_spectral import Spectral as sb, mcpp_available
from pyomo.core import (
    ConcreteModel, Expression, Var, acos, asin, atan, cos, exp, quicksum, sin,
    tan, value
)
from pyomo.core.expr.current import identify_variables


m = ConcreteModel()
m.x1 = Var(bounds=(-0.3, 0.2), initialize = 0.1)
m.x2 = Var(bounds=(-0.1, 0.6), initialize = 0.3)
m.x3 = Var(bounds=(-0.4, 0.5), initialize = 0.2)
m.e = Expression(expr = exp(m.x1 - 2 * pow(m.x2, 2) + 3 * pow(m.x3, 3)))
eqn = sb(m.e.expr)
print("Lower Interval Bound: ", eqn.lower())
print("Upper Interval Bound: ", eqn.upper())
print("Lower Spectral Bound: ", eqn.specbnd_l())
print("Upper Spectral Bound: ", eqn.specbnd_u())
    
#def lower(self):
#    return self.mcpp_lib.new_lower(self.expr)

#def upper(self):
#    return self.mcpp_lib.new_upper(self.expr)

#def specbnd_u(self):
#    return self.mcpp_lib.new_specbnd_u(self.expr)

#def specbnd_l(self):
#    return self.mcpp_lib.new_specbnd_l(self.expr)



