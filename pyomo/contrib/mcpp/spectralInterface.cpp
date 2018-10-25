#include "interval.hpp"
#include "specbnd.hpp"
typedef mc::Interval I;
typedef mc::Specbnd<I> SB;


//Build pyomo expression in MC++
void *createVar(double lb, double pt, double ub, int count, int index)
{
    SB var1( I( lb, ub ), index, count);

    void *ans = new SB(var1);

    return ans;
}

void *createConstant(double cons)
{
    void *ans = new SB(cons);

    return ans;
}

SB *mult(SB *var1, SB *var2)
{
    SB F = *var1 * *var2;

    SB *ans = new SB(F);
    return ans;
}

SB *add(SB *var1, SB *var2)
{
    SB F = *var1 + *var2;

    SB *ans = new SB(F);
    return ans;
}

SB *power(SB *var1, SB *var2)
{
    SB var = *var2;
    double doub = var.I().l();
    int exponent = (int)doub;

    SB F = pow(*var1, exponent);

    SB *ans = new SB(F);
    return ans;
}


SB *monomial(SB *var1, SB *var2)
{
    SB F = *var1 * *var2;

    SB *ans = new SB(F);
    return ans;
}

SB *reciprocal(SB *var1, SB *var2)
{
    SB F = inv(*var2);

    SB *ans = new SB(F);
    return ans;
}

SB *negation(SB *var1)
{
    SB F = 0 - *var1;

    SB *ans = new SB(F);
    return ans;
}
/*
fabs not supported

SB *abs(SB *var1)
{
    SB F = fabs(*var1);

    SB *ans = new SB(F);
    return ans;
}
*/

SB *trigSin(SB *var1)
{
    SB F = sin(*var1);

    SB *ans = new SB(F);
    return ans;
}

SB *trigCos(SB *var1)
{
    SB F = cos(*var1);

    SB *ans = new SB(F);
    return ans;
}

SB *trigTan(SB *var1)
{
    SB F = tan(*var1);

    SB *ans = new SB(F);
    return ans;
}

SB *atrigSin(SB *var1)
{
    SB F = asin(*var1);

    SB *ans = new SB(F);
    return ans;
}

SB *atrigCos(SB *var1)
{
    SB F = acos(*var1);

    SB *ans = new SB(F);
    return ans;
}

SB *atrigTan(SB *var1)
{
    SB F = atan(*var1);

    SB *ans = new SB(F);
    return ans;
}

SB *NPV(SB *var1)
{
    SB F = *var1;

    SB *ans = new SB(F);
    return ans;
}

void *displayOutput(void *ptr)
{
    SB *var  = (SB*) ptr;
    SB F = *var;
    std::cout << "F: " << F << std::endl;
}

SB *exponential(SB *var1)
{
    SB F = exp(*var1);

    SB *ans = new SB(F);
    return ans;
}

















//Get usable information from SB++
double lower(SB *expr)
{
    SB F = *expr;
    double Flb = F.I().l();
    return Flb;
}

double upper(SB *expr)
{
    SB F = *expr;
    double Fub = F.I().u();
    return Fub;
}

double specbnd_u(SB *expr)
{
    SB F = *expr;
    double Fsb_u = F.SI().u();
    return Fsb_u;
}

double specbnd_l(SB *expr)
{
    SB F = *expr;
    double Fsb_l = F.SI().l();
    return Fsb_l;
}

/*
double subcc(SB *expr, int index)
{
    SB F = *expr;
    double Fccsub = F.ccsub(index);
    return Fccsub;
}

double subcv(SB *expr, int index)
{
    SB F = *expr;
    double Fcvsub = F.cvsub(index);
    return Fcvsub;
}
*/













extern "C"
{
    void *new_createVar(double lb, double pt, double ub, int count, int index)
    {
        void *ans = createVar(lb, pt, ub, count, index);
        return ans;
    }


    void *new_createConstant(double cons)
    {
        void *ans = createConstant(cons);
        return ans;
    }

    SB *new_mult(SB *var1, SB *var2)
    {
        SB *ans = mult(var1, var2);
        return ans;
    }

    SB *new_add(SB *var1, SB *var2)
    {
        SB *ans = add(var1, var2);
        return ans;
    }

    SB *new_power(SB *var1, SB *var2)
    {
        SB *ans = power(var1, var2);
        return ans;
    }

    SB *new_monomial(SB *var1, SB *var2)
    {
        SB *ans = monomial(var1, var2);
        return ans;
    }

    SB *new_reciprocal(SB *var1, SB *var2)
    {
        SB *ans = reciprocal(var1, var2);
        return ans;
    }

    SB *new_negation(SB *var1)
    {
        SB *ans = negation(var1);
        return ans;
    }
/*
    fabs not supported
    SB *new_abs(SB *var1)
    {
        SB *ans = abs(var1);
        return ans;
    }
*/

    SB *new_trigSin(SB *var1)
    {
        SB *ans = trigSin(var1);
        return ans;
    }

    SB *new_trigCos(SB *var1)
    {
        SB *ans = trigCos(var1);
        return ans;
    }

    SB *new_trigTan(SB *var1)
    {
        SB *ans = trigTan(var1);
        return ans;
    }

    SB *new_atrigSin(SB *var1)
    {
        SB *ans = atrigSin(var1);
        return ans;
    }

    SB *new_atrigCos(SB *var1)
    {
        SB *ans = atrigCos(var1);
        return ans;
    }

    SB *new_atrigTan(SB *var1)
    {
        SB *ans = atrigTan(var1);
        return ans;
    }

    SB *new_NPV(SB *var1)
    {
        SB *ans = NPV(var1);
        return ans;
    }

    void *new_displayOutput(void *ptr)
    {
        displayOutput(ptr);
    }

    SB *new_exponential(SB *ptr1)
    {
        SB *ans = exponential(ptr1);
        return ans;
    }

    double new_lower(SB *expr)
    {
        double ans = lower(expr);
        return ans;
    }

    double new_upper(SB *expr)
    {
        double ans = upper(expr);
        return ans;
    }

    double new_specbnd_u(SB *expr)
    {
        double ans = specbnd_u(expr);
        return ans;
    }

    double new_specbnd_l(SB *expr)
    {
        double ans = specbnd_l(expr);
        return ans;
    }
/*
    double new_subcc(SB *expr, int index)
    {
        double ans = subcc(expr, index);
        return ans;
    }

        double new_subcv(SB *expr, int index)
    {
        double ans = subcv(expr, index);
        return ans;
    }
*/
}

//g++ -I ~/MC++/mcpp/src/3rdparty/fadbad++ -I ~/MC++/mcpp/src/mc -I /usr/include/python2.7/ -I ~/MC++/mcpp/src/3rdparty/cpplapack-2015.05.11-1/include/ -fPIC -O2 -c spectralInterface.cpp

//g++ -shared spectralInterface.o -o spectralInterface.so
