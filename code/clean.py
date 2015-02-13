'''data cleaning related code
   created by Robert Kruhlak
'''

## use floating point division always (ie matlab, python 3.x)
from __future__ import division

def clean_device(device):
    '''function to clean the device column of the sessions dataframe
       Input: Series
       Output: Series
    '''
    device = device.str.replace('(','')
    device = device.str.replace(';', '')
    device = device.str.replace('/', ' ')
    
    return device

def clean_dmodel(dmodel):
    '''function take the 0th element of the dmodel  
       Input: Series
       Output: Series

    '''
    return dmodel.str.replace('(','').str.replace(')','').str.replace(',','').str.replace('-mx; ', '')

