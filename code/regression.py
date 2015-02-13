'''regression related files
   created by Robert Kruhlak
'''
## use floating point division always (ie matlab, python 3.x)
from __future__ import division

import numpy as np
from scipy.optimize import minimize, leastsq

#Normalizer/Scaler class
from sklearn.preprocessing import StandardScaler

def linfit(y, x = None):
    '''function to fit data with an axis that is non-numeric.
       Takes an array of dependent variables (y) and creates a sequential
       x-axis based on the length of y.
       returns: x (array), theoretical y (array), model (array), r squared
       In this case the model is the coefficient to a linear polynomial
       A[0]*x + A[1] 
    '''
    if x is None:
        x = np.arange(len(y))
    
    model, resid = np.polyfit(x,y,1,full=True)[:2]

    ytheory = np.polyval(model, x)
    
    resid2 = np.sum((ytheory-y)**2)
    r2 = 1 - resid / (y.size * y.var())
    return x, ytheory, model, r2

def weighted_exponential_fit(xaxis, y, model0):
    '''weighted exponential fitting routine
       xaxis, array or series
       y, y data array or series
       model0, two element list as the initial guess [slope, y-int]
    '''
    n = len(xaxis)
    
    logy = np.log(y)
    
    result = minimize(opt_fun, model0, args = (xaxis, y, logy), 
                      method = 'BFGS' )
    #this is the log value and will need to be np.exp(ytheory) outside
    #this function.
    ytheory = np.polyval(result.x, xaxis)

    #mean squared error
    mse = np.sum((ytheory-logy)**2)/n
    
    if not result.success:
        if result.status != 2:
            print result.message
    

    return xaxis, ytheory, result.x, mse, result.success

def opt_fun(c, x, y, logy):
    '''weighted exponential fitting function.
       minimize with c being the parameters
       Input: c, list of float parameters
              x, x data array or Series
              y, y data array or Series
       logy, natural log of the y data, array or Series
       Output: float
    '''
    #use the same format as polyfit so we can use polyval to determine
    #the theoretical y
    return np.sum(y*(logy - c[1] -c[0]*x)**2)/100.

def mean_value(y):
    '''function to  create a horizontal line with the mean value of y
       This is useful to compare against a linfit with a small slope or 
       just to visualize where the mean is for noisy data.
    '''
    y_mean = y.mean()

    y_mean_array = np.array(y_mean*np.ones(len(y)))
    return y_mean_array

def correlate(df, columns = None):
    '''function to determine the correlation between columns in a dataframe
    '''
    if columns is None:
        #calculate the correlation for all numeric columns
        return df.corr()
    else:
        return df[columns].corr()
def exponential(kd, x0):
    '''Exponential distribution'''
    #Exponential and weibull don't seem to be a good fit for 
    #the distribution of users that have not started using the service
    #after x days
    return (1 - np.exp(-x0**kd[1]))  #exponential distribution
    
#Weibull distribution
#return kd[0]/kd[1]*((x0/kd[1])**(kd[0]-1))*np.exp(-(x0/kd[1])**kd[0])

def pareto(kd, x0):
    '''function that describe a pareto distribution in x0
       Used in fitting routines
       Inputs: kd, array of floats 
               x0, array independent variable
       Output: y, dependent variable
    '''
    #kd[0] represents the minimum day (can be float) after which
    #the probability is < 1.
    #kd[1] is the scale
    #Multiply by 100 because we are dealing with % not fractional probability
    return 100*(kd[0]/(x0))**kd[1] #Pareto distribution
    
def pareto_cdf(kd, x0):
    '''function that describe a pareto cumulative distribution function in x0
       Used in fitting routines
       Inputs: kd, array of floats 
               x0, array independent variable
       Output: y, dependent variable
    '''  
    #kd[0] represents the minimum day (can be float) after which
    #the probability is < 1.
    return 100*(1 - (kd[0]/x0)**kd[1]) 
    
def lomax(kd, x0):
    '''function that describe a lomax distribution (pareto type II) in x0
       Used in fitting routines
       Inputs: kd, array of floats 
               x0, array independent variable
       Output: y, dependent variable
    '''
    #Multiply by 100 because we are dealing with % not fractional probability
    return 100*(1+ (x0-kd[2])/kd[0])**(-kd[1]) #Lomax distribution
    
def power_law(kd, x0):
    '''function that describe a lomax distribution (pareto type II) in x0
       Used in fitting routines
       Inputs: kd, array of floats 
               x0, array independent variable
       Output: y, dependent variable
    '''
    #kd[0] represents the minimum day (can be float) after which
    #the probability is < 1.
    #kd[1] is the scale
    #Multiply by 100 because we are dealing with % not fractional probability
    #return 100*(kd[0]/(x0))**kd[1] #Pareto distribution  
        
    return kd[0]*(x0**kd[1]) #Power law -- like Pareto distribution
    
def power_law_m(kd, x0):
    '''function that describe a 100 -  power law in x0
       Used in fitting routines
       Inputs: kd, array of floats 
               x0, array independent variable
       Output: y, dependent variable
    '''
    #Cumulative distribution function of the Pareto distribution
    return 100*(1 - (kd[0]/x0)**kd[1])      

def residuals(kd, x0, y, func):
    return y - func(kd, x0)


