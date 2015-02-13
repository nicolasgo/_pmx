'''categorize related files
   created by Robert Kruhlak
'''
## use floating point division always (ie matlab, python 3.x)
from __future__ import division

def split_users(udf, sdf = None, how = 'day', split_val = None):    
    '''function to split users based on the input day
       Input: udf, slice of users dataframe
              sdf, slice of sessions dataframe
              split_var, int/str, variable used to split the data set
              how, str, method to use to split the data set ('day', 'friend')
           Output: df
    '''
    if how == 'day':
            
        true_users, false_users = user_day_since_joining(udf, sdf, 
                                                         day = split_val)
            
    else:
            
        true_users, false_users = user_attribute(udf, attribute = how, 
                                                 split_val = split_val)  
            
    return  true_users, false_users
        
def user_day_since_joining(udf, sdf, day ): 
    '''function to split the dataset into started/not started categories
       udf, slice of users dataframe
       sdf, slice of sessions dataframe
       day, int, split_var, int/str, variable used to split the data set
    '''       
    #create a filter to split users into started/ not started categories
    mask = ((sdf.time > sdf.joined) & (sdf.time <= (sdf.joined + day)) )        
                 
    #users that have had at least one session  after their
    #join date and on or before their joined date + day                                                   
    started_users = set(sdf[ mask].index)  
    #this should be much faster than accessing the session df again.        
    not_started_users = udf.drop(started_users).index 
        
    return started_users, not_started_users
    
def user_day_range(udf, sdf, start_date, end_date): 
    '''function to split the dataset into active/inactive categories
       udf, slice of users dataframe
       sdf, slice of sessions dataframe
       day, int, split_var, int/str, variable used to split the data set
       start_date, Series of period objects the same dimensions as sdf
       end_date, Series of period objects the same dimensions as sdf
    '''       
    #create a filter to split users into started/ not started categories
    mask = ((sdf.time > start_date) & (sdf.time <= end_date) )        
                 
    #users that have had at least one session  after their
    #join date and on or before their joined date + day                                                   
    active_users = set(sdf[ mask].index)  
    #this should be much faster than accessing the session df again.        
    not_active_users = udf.drop(active_users).index 
        
    return active_users, not_active_users    
        
def user_attribute(udf, attribute = 'friends', split_val = None):
    '''function to split the dataset into friend/no friend categories
       udf, slice or whole user dataframe
       attribute, attribute (column) of the user dataframe to categorize
       split_val, int/str, value used as the category boundary.
    '''      
    if split_val is None:
        split_val = 0
        
    true_mask = udf[attribute] > split_val
    
    return udf[true_mask].index, udf[~true_mask].index

