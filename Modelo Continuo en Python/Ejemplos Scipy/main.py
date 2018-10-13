__author__ = 'Pancho'

from scipy.optimize import minimize, rosen, rosen_der

def fun(x):
    suma = 0
    for i in x:
        suma+=1000*x[i]+5000/x[i]
    return suma


#cons = ({'type': 'ineq', 'fun': lambda x:  x[0] - 2 * x[1] + 2},
#        {'type': 'ineq', 'fun': lambda x: -x[0] - 2 * x[1] + 6},
#        {'type': 'ineq', 'fun': lambda x: -x[0] + 2 * x[1] + 2})

bnds = ((0.00001, None), (0.00001, None), (0.00001, None), (0.00001, None))

res = minimize(fun, (1.0, 1.0, 1.0, 1.0), method='L-BFGS-B')

print res.x
print res