# Note: the self.mcpp.* functions are all C-style functions implemented
# in the compiled MC++ wrapper library

from __future__ import division

import ctypes
import logging
import os

from pyomo.core import value
from pyomo.core.expr.current import identify_variables
from pyomo.core.expr.expr_pyomo5 import (
    AbsExpression, LinearExpression, NegationExpression, NPV_AbsExpression,
    NPV_ExternalFunctionExpression, NPV_NegationExpression, NPV_PowExpression,
    NPV_ProductExpression, NPV_ReciprocalExpression, NPV_SumExpression,
    NPV_UnaryFunctionExpression, PowExpression, ProductExpression,
    ReciprocalExpression, StreamBasedExpressionVisitor, SumExpression,
    UnaryFunctionExpression, nonpyomo_leaf_types
)
from pyomo.core.kernel.component_map import ComponentMap

logger = logging.getLogger('pyomo.contrib.mcpp')

path = os.path.dirname(__file__)


def mcpp_available():
    """True if the MC++ shared object file exists. False otherwise."""
    return os.path.isfile(path + '/spectralInterface.so')


NPV_expressions = set(
    (NPV_AbsExpression, NPV_ExternalFunctionExpression,
     NPV_NegationExpression, NPV_PowExpression,
     NPV_ProductExpression, NPV_ReciprocalExpression, NPV_SumExpression,
     NPV_UnaryFunctionExpression))


class MCPP_visitor(StreamBasedExpressionVisitor):
    """Creates an MC++ expression from the corresponding Pyomo expression.

    This class walks a pyomo expression tree and builds up the corresponding
    expression of type McCormick.

    """

    def __init__(self, mcpp_lib, expression):
        super(MCPP_visitor, self).__init__()
        self.expr = expression
        self.mcpp = mcpp_lib
        self.declare_mcpp_library_calls()
        vars = list(identify_variables(expression, include_fixed=False))
        self.num_vars = len(vars)
        # Map expression variables to MC variables
        self.known_vars = ComponentMap()
        # Map expression variables to their index
        self.var_to_idx = ComponentMap()
        # Pre-register all variables
        for i, var in enumerate(vars):
            self.var_to_idx[var] = i
            self.known_vars[var] = self.register_var(var)

    def declare_mcpp_library_calls(self):
        # Create MC type variable
        self.mcpp.new_createVar.argtypes = [ctypes.c_double,
                                            ctypes.c_double,
                                            ctypes.c_double,
                                            ctypes.c_int,
                                            ctypes.c_int]
        self.mcpp.new_createVar.restype = ctypes.c_void_p

        # Create MC type constant
        self.mcpp.new_createConstant.argtypes = [ctypes.c_double]
        self.mcpp.new_createConstant.restype = ctypes.c_void_p

        # Multiply MC objects
        self.mcpp.new_mult.argtypes = [ctypes.c_void_p,
                                       ctypes.c_void_p]
        self.mcpp.new_mult.restype = ctypes.c_void_p

        # Add MC objects
        self.mcpp.new_add.argtypes = [ctypes.c_void_p,
                                      ctypes.c_void_p]
        self.mcpp.new_add.restype = ctypes.c_void_p

        # pow(x, y) function, where y is an int
        self.mcpp.new_power.argtypes = [ctypes.c_void_p,
                                        ctypes.c_void_p]
        self.mcpp.new_power.restype = ctypes.c_void_p

        # MC constant * MC Variable
        self.mcpp.new_monomial.argtypes = [ctypes.c_void_p,
                                           ctypes.c_void_p]
        self.mcpp.new_monomial.restype = ctypes.c_void_p

        # 1 / MC Variable
        self.mcpp.new_reciprocal.argtypes = [ctypes.c_void_p,
                                             ctypes.c_void_p]
        self.mcpp.new_reciprocal.restype = ctypes.c_void_p

        # - MC Variable
        self.mcpp.new_negation.argtypes = [ctypes.c_void_p]
        self.mcpp.new_negation.restype = ctypes.c_void_p

        # fabs(MC Variable)
        # Not Supported
        #self.mcpp.new_abs.argtypes = [ctypes.c_void_p]
        #self.mcpp.new_abs.restype = ctypes.c_void_p

        # sin(MC Variable)
        self.mcpp.new_trigSin.argtypes = [ctypes.c_void_p]
        self.mcpp.new_trigSin.restype = ctypes.c_void_p

        # cos(MC Variable)
        self.mcpp.new_trigCos.argtypes = [ctypes.c_void_p]
        self.mcpp.new_trigCos.restype = ctypes.c_void_p

        # tan(MC Variable)
        self.mcpp.new_trigTan.argtypes = [ctypes.c_void_p]
        self.mcpp.new_trigTan.restype = ctypes.c_void_p

        # asin(MC Variable)
        self.mcpp.new_atrigSin.argtypes = [ctypes.c_void_p]
        self.mcpp.new_atrigSin.restype = ctypes.c_void_p

        # acos(MC Variable)
        self.mcpp.new_atrigCos.argtypes = [ctypes.c_void_p]
        self.mcpp.new_atrigCos.restype = ctypes.c_void_p

        # atan(MC Variable)
        self.mcpp.new_atrigTan.argtypes = [ctypes.c_void_p]
        self.mcpp.new_atrigTan.restype = ctypes.c_void_p

        # exp(MC Variable)
        self.mcpp.new_exponential.argtypes = [ctypes.c_void_p]
        self.mcpp.new_exponential.restype = ctypes.c_void_p

        self.mcpp.new_NPV.argtypes = [ctypes.c_void_p]
        self.mcpp.new_NPV.restype = ctypes.c_void_p

    def exitNode(self, node, data):
        if isinstance(node, ProductExpression):
            ans = self.mcpp.new_mult(data[0], data[1])
        elif isinstance(node, SumExpression):
            ans = data[0]
            for arg in data[1:]:
                ans = self.mcpp.new_add(ans, arg)
        elif isinstance(node, PowExpression):
            assert (type(data[0]) == int),\
                "Argument to pow() must be an integer. Received %s" % (data[0],)
            ans = self.mcpp.new_power(data[0], data[1])
        elif isinstance(node, ReciprocalExpression):
            ans = self.mcpp.new_reciprocal(
                self.mcpp.new_createConstant(1), data[0])
        elif isinstance(node, NegationExpression):
            ans = self.mcpp.new_negation(data[0])
        #elif isinstance(node, AbsExpression):
        #    ans = self.mcpp.new_abs(data[0])
        elif isinstance(node, LinearExpression):
            raise NotImplementedError(
                'Quicksum has bugs that prevent proper usage of MC++.')
            # ans = self.mcpp.new_createConstant(node.constant)
            # for coef, var in zip(node.linear_coefs, node.linear_vars):
            #     ans = self.mcpp.new_add(
            #         ans,
            #         self.mcpp.new_mult(
            #             self.mcpp.new_createConstant(coef),
            #             self.register_num(var)))
        elif isinstance(node, UnaryFunctionExpression):
            if (node.name == "exp"):
                ans = self.mcpp.new_exponential(data[0])
            if (node.name == "sin"):
                ans = self.mcpp.new_trigSin(data[0])
            if (node.name == "cos"):
                ans = self.mcpp.new_trigCos(data[0])
            if (node.name == "tan"):
                ans = self.mcpp.new_trigTan(data[0])
            if (node.name == "asin"):
                ans = self.mcpp.new_atrigSin(data[0])
            if (node.name == "acos"):
                ans = self.mcpp.new_atrigCos(data[0])
            if (node.name == "atan"):
                ans = self.mcpp.new_atrigTan(data[0])
        elif any(isinstance(node, npv) for npv in NPV_expressions):
            ans = self.mcpp.new_NPV(value(data[0]))
        elif type(node) in nonpyomo_leaf_types:
            ans = self.mcpp.new_createConstant(node)
        elif not node.is_expression_type():
            ans = self.register_num(node)
        else:
            raise RuntimeError("Unhandled expression type: %s" % (type(node)))

        return ans

    def beforeChild(self, node, child):
        if type(child) in nonpyomo_leaf_types:
            # This means the child is POD
            # i.e., int, float, string
            return False, self.mcpp.new_createConstant(child)
        elif not child.is_expression_type():
            # node is either a Param, Var, or NumericConstant
            return False, self.register_num(child)
        else:
            # this is an expression node
            return True, None

    def register_num(self, num):
        """Registers a new number: Param, Var, or NumericConstant."""
        if num.is_fixed():
            return self.mcpp.new_createConstant(value(num))
        else:
            return self.known_vars[num]

    def register_var(self, var):
        """Registers a new variable."""
        var_idx = self.var_to_idx[var]
        lb = var.lb
        ub = var.ub
        var_val = value(var, exception=False)
        if lb is None:
            lb = -500000
            logger.warning(
                'Var %s missing lower bound. Assuming LB of %s'
                % (var.name, lb))
        if ub is None:
            ub = 500000
            logger.warning(
                'Var %s missing upper bound. Assuming UB of %s'
                % (var.name, ub))
        if var_val is None:
            var_val = (lb + ub) / 2
            logger.warning(
                'Var %s missing value. Assuming midpoint value of %s'
                % (var.name, var_val))
        return self.mcpp.new_createVar(
            lb, var_val, ub, self.num_vars, var_idx)

    def finalizeResult(self, node_result):
        return node_result


class Spectral(object):

    """
    This class takes the constructed expression from MCPP_Visitor and
    allows for MC methods to be performed on pyomo expressions.

    displayOutput(self): displays an MC expression in the form:
    F: [lower interval : upper interval ] [convex underestimator :
    concave overestimator ] [ (convex subgradient) : (concave subgradient]

    lower(self): returns a float of the lower interval bound that is valid
    across the entire domain

    upper(self): returns a float of the upper interval bound that is valid
    across the entire domain

    concave(self): returns a float of the concave overestimator at the
    current value() of each variable.

    convex(self): returns a float of the convex underestimator at the
    current value() of each variable.

    ##Note: In order to describe the concave and convex relaxations over
    the entire domain, it is necessary to use changePoint() to repeat the
    calculation at different points.

    subcc(self): returns a ComponentMap() that maps the pyomo variables
    to the subgradients of the McCormick concave overestimators at the
    current value() of each variable.

    subcv(self): returns a ComponentMap() that maps the pyomo variables
    to the subgradients of the McCormick convex underestimators at the
    current value() of each variable.

    def changePoint(self, var, point): updates the current value() on the
    pyomo side and the current point on the MC++ side.
                                                                    """

    def __init__(self, expression):
        self.mcpp_lib = ctypes.CDLL(path + '/spectralInterface.so')
        self.oExpr = expression
        self.visitor = MCPP_visitor(self.mcpp_lib, expression)
        self.mcppExpression = self.visitor.walk_expression(expression)
        self.expr = self.mcppExpression

        self.mcpp_lib.new_displayOutput.argtypes = [ctypes.c_void_p]

        self.mcpp_lib.new_lower.argtypes = [ctypes.c_void_p]
        self.mcpp_lib.new_lower.restype = ctypes.c_double

        self.mcpp_lib.new_upper.argtypes = [ctypes.c_void_p]
        self.mcpp_lib.new_upper.restype = ctypes.c_double

        self.mcpp_lib.new_specbnd_u.argtypes = [ctypes.c_void_p]
        self.mcpp_lib.new_specbnd_u.restype = ctypes.c_double

        self.mcpp_lib.new_specbnd_l.argtypes = [ctypes.c_void_p]
        self.mcpp_lib.new_specbnd_l.restype = ctypes.c_double

        #self.mcpp_lib.new_subcc.argtypes = [ctypes.c_void_p, ctypes.c_int]
        #self.mcpp_lib.new_subcc.restype = ctypes.c_double
        #
        #self.mcpp_lib.new_subcv.argtypes = [ctypes.c_void_p, ctypes.c_int]
        #self.mcpp_lib.new_subcv.restype = ctypes.c_double

    def displayOutput(self):
        return self.mcpp_lib.new_displayOutput(self.expr)

    def lower(self):
        return self.mcpp_lib.new_lower(self.expr)

    def upper(self):
        return self.mcpp_lib.new_upper(self.expr)

    def specbnd_u(self):
        return self.mcpp_lib.new_specbnd_u(self.expr)

    def specbnd_l(self):
        return self.mcpp_lib.new_specbnd_l(self.expr)

    #def subcc(self):
    #    ans = ComponentMap()
    #    for key in self.visitor.var_to_idx:
    #        i = self.visitor.var_to_idx[key]
    #        ans[key] = self.mcpp_lib.new_subcc(self.expr, i)
    #    return ans
    #
    #def subcv(self):
    #    ans = ComponentMap()
    #    for key in self.visitor.var_to_idx:
    #        i = self.visitor.var_to_idx[key]
    #        ans[key] = self.mcpp_lib.new_subcv(self.expr, i)
    #    return ans

    #def changePoint(self, var, point):
    #    var.set_value(point)
    #    # WARNING: TODO: this has side effects
    #    self.visitor = MCPP_visitor(self.mcpp_lib, self.oExpr)
    #    self.mcppExpression = self.visitor.walk_expression(self.oExpr)
    #    self.expr = self.mcppExpression





