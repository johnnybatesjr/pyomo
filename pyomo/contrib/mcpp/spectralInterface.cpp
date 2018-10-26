#include "interval.hpp"
#include "specbnd.hpp"
typedef mc::Interval I;
typedef mc::Specbnd<I> SB;
#include "mccormick.hpp"
typedef mc::McCormick<I> MC;
typedef mc::Specbnd<MC> SBMC;

//Build pyomo expression in MC++
void *createVarSB(double lb, double pt, double ub, int count, int index)
{
    SB var1( I( lb, ub ), index, count);

    void *ans = new SB(var1);

    return ans;
}

void *createVarSBMC(double lb, double pt, double ub, int count, int index)
{
    SBMC var1( MC(I( lb, ub ), pt).sub(count, index), index, count);

    void *ans = new SBMC(var1);

    return ans;
}

void *createConstant(double cons)
{
    void *ans = new SBMC(cons);

    return ans;
}

SBMC *mult(SBMC *var1, SBMC *var2)
{
    SBMC F = *var1 * *var2;

    SBMC *ans = new SBMC(F);
    return ans;
}

SBMC *add(SBMC *var1, SBMC *var2)
{
    SBMC F = *var1 + *var2;

    SBMC *ans = new SBMC(F);
    return ans;
}

SBMC *power(SBMC *var1, SBMC *var2)
{
    SBMC var = *var2;
    double doub = var.I().l();
    int exponent = (int)doub;

    SBMC F = pow(*var1, exponent);

    SBMC *ans = new SBMC(F);
    return ans;
}


SBMC *monomial(SBMC *var1, SBMC *var2)
{
    SBMC F = *var1 * *var2;

    SBMC *ans = new SBMC(F);
    return ans;
}

SBMC *reciprocal(SBMC *var1, SBMC *var2)
{
    SBMC F = inv(*var2);

    SBMC *ans = new SBMC(F);
    return ans;
}

SBMC *negation(SBMC *var1)
{
    SBMC F = 0 - *var1;

    SBMC *ans = new SBMC(F);
    return ans;
}
/*
fabs not supported

SBMC *abs(SBMC *var1)
{
    SBMC F = fabs(*var1);

    SBMC *ans = new SBMC(F);
    return ans;
}
*/

SBMC *trigSin(SBMC *var1)
{
    SBMC F = sin(*var1);

    SBMC *ans = new SBMC(F);
    return ans;
}

SBMC *trigCos(SBMC *var1)
{
    SBMC F = cos(*var1);

    SBMC *ans = new SBMC(F);
    return ans;
}

SBMC *trigTan(SBMC *var1)
{
    SBMC F = tan(*var1);

    SBMC *ans = new SBMC(F);
    return ans;
}

SBMC *atrigSin(SBMC *var1)
{
    SBMC F = asin(*var1);

    SBMC *ans = new SBMC(F);
    return ans;
}

SBMC *atrigCos(SBMC *var1)
{
    SBMC F = acos(*var1);

    SBMC *ans = new SBMC(F);
    return ans;
}

SBMC *atrigTan(SBMC *var1)
{
    SBMC F = atan(*var1);

    SBMC *ans = new SBMC(F);
    return ans;
}

SBMC *NPV(SBMC *var1)
{
    SBMC F = *var1;

    SBMC *ans = new SBMC(F);
    return ans;
}

void *displayOutput(void *ptr)
{
    SBMC *var  = (SBMC*) ptr;
    SBMC F = *var;
    std::cout << "F: " << F << std::endl;
}

SBMC *exponential(SBMC *var1)
{
    SBMC F = exp(*var1);

    SBMC *ans = new SBMC(F);
    return ans;
}

















//Get usable information from SBMC++
double lower(SBMC *expr)
{
    SBMC F = *expr;
    double Flb = F.I().l();
    return Flb;
}

double upper(SBMC *expr)
{
    SBMC F = *expr;
    double Fub = F.I().u();
    return Fub;
}

double specbnd_u(SBMC *expr)
{
    SBMC F = *expr;
    double Fsb_u = F.SI().u();
    return Fsb_u;
}

double specbnd_l(SBMC *expr)
{
    SBMC F = *expr;
    double Fsb_l = F.SI().l();
    return Fsb_l;
}

double concave(SBMC *expr)
{
    SBMC F = *expr;
    double Fcc = F.SI().cc();
    return Fcc;
}

double convex(SBMC *expr)
{
    SBMC F = *expr;
    double Fcv = F.SI().cv();
    return Fcv;
}

double subcc(SBMC *expr, int index)
{
    SBMC F = *expr;
    double Fccsub = F.SI().ccsub(index);
    return Fccsub;
}

double subcv(SBMC *expr, int index)
{
    SBMC F = *expr;
    double Fcvsub = F.SI().cvsub(index);
    return Fcvsub;
}














extern "C"
{
    void *new_createVarSB(double lb, double pt, double ub, int count, int index)
    {
        void *ans = createVarSB(lb, pt, ub, count, index);
        return ans;
    }

    void *new_createVarSBMC(double lb, double pt, double ub, int count, int index)
    {
        void *ans = createVarSBMC(lb, pt, ub, count, index);
        return ans;
    }


    void *new_createConstant(double cons)
    {
        void *ans = createConstant(cons);
        return ans;
    }

    SBMC *new_mult(SBMC *var1, SBMC *var2)
    {
        SBMC *ans = mult(var1, var2);
        return ans;
    }

    SBMC *new_add(SBMC *var1, SBMC *var2)
    {
        SBMC *ans = add(var1, var2);
        return ans;
    }

    SBMC *new_power(SBMC *var1, SBMC *var2)
    {
        SBMC *ans = power(var1, var2);
        return ans;
    }

    SBMC *new_monomial(SBMC *var1, SBMC *var2)
    {
        SBMC *ans = monomial(var1, var2);
        return ans;
    }

    SBMC *new_reciprocal(SBMC *var1, SBMC *var2)
    {
        SBMC *ans = reciprocal(var1, var2);
        return ans;
    }

    SBMC *new_negation(SBMC *var1)
    {
        SBMC *ans = negation(var1);
        return ans;
    }
/*
    fabs not supported
    SBMC *new_abs(SBMC *var1)
    {
        SBMC *ans = abs(var1);
        return ans;
    }
*/

    SBMC *new_trigSin(SBMC *var1)
    {
        SBMC *ans = trigSin(var1);
        return ans;
    }

    SBMC *new_trigCos(SBMC *var1)
    {
        SBMC *ans = trigCos(var1);
        return ans;
    }

    SBMC *new_trigTan(SBMC *var1)
    {
        SBMC *ans = trigTan(var1);
        return ans;
    }

    SBMC *new_atrigSin(SBMC *var1)
    {
        SBMC *ans = atrigSin(var1);
        return ans;
    }

    SBMC *new_atrigCos(SBMC *var1)
    {
        SBMC *ans = atrigCos(var1);
        return ans;
    }

    SBMC *new_atrigTan(SBMC *var1)
    {
        SBMC *ans = atrigTan(var1);
        return ans;
    }

    SBMC *new_NPV(SBMC *var1)
    {
        SBMC *ans = NPV(var1);
        return ans;
    }

    void *new_displayOutput(void *ptr)
    {
        displayOutput(ptr);
    }

    SBMC *new_exponential(SBMC *ptr1)
    {
        SBMC *ans = exponential(ptr1);
        return ans;
    }

    double new_lower(SBMC *expr)
    {
        double ans = lower(expr);
        return ans;
    }

    double new_upper(SBMC *expr)
    {
        double ans = upper(expr);
        return ans;
    }

    double new_specbnd_u(SBMC *expr)
    {
        double ans = specbnd_u(expr);
        return ans;
    }

    double new_specbnd_l(SBMC *expr)
    {
        double ans = specbnd_l(expr);
        return ans;
    }

    double new_concave(SBMC *expr)
    {
        double ans = concave(expr);
        return ans;
    }

    double new_convex(SBMC *expr)
    {
        double ans = convex(expr);
        return ans;
    }

    double new_subcc(SBMC *expr, int index)
    {
        double ans = subcc(expr, index);
        return ans;
    }

        double new_subcv(SBMC *expr, int index)
    {
        double ans = subcv(expr, index);
        return ans;
    }

}

//g++ -I ~/MC++/mcpp/src/3rdparty/fadbad++ -I ~/MC++/mcpp/src/mc -I /usr/include/python2.7/ -I ~/MC++/mcpp/src/3rdparty/cpplapack-2015.05.11-1/include/ -fPIC -O2 -c spectralInterface.cpp

//g++ -shared spectralInterface.o -o spectralInterface.so
