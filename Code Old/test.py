import numpy
import pylab
from scipy.optimize import fmin

def multi(x):
        return (x[0]*x[0]+x[1]*x[1]+50*x[0]+100*x[1]+5)
#multi=lambda x: (x[0]*x[0]+x[1]*x[1]+50*x[0]+100*x[1]+5)
print list(fmin(multi,[-5,-5]))
