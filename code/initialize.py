'''module for initialising .
   Created by Robert Kruhlak
'''
## use floating point division always (ie matlab, python 3.x)
from __future__ import division

import pandas as pd

from code import dates, validate

from code.resample import random_sample

def initialize(udf, sdf, validate_dfs = True, 
               date_str_to_period = False,
               fraction_of_population = 0.1,
               trial = True): 
    '''function used in most if not all classes related to users and 
       cohorts.
    
            Inputs: udf, dataframe with user data
                    sdf, dataframe with sessions data
                    validate_dfs, Boolean, to validate or not
                    date_str_to_period, Boolean, to convert datetime like
                                                 str to period objects
                    fraction_of_population, float, the fraction of the 
                                                   population that you
                                                   want to analyse.
                    trial, Boolean, to keep trial users or not
                    
        Note: both validate_df and date_str_to_period
              Booleans should not be True, True 
              in the current use case. For example, data that is not
              validated will have its datetime like string converted
              during the validation process. Validated data will not
              need to be revalidated but may need its datatime like strings 
              (if loaded from .csv file) converted to period objects.
              
    '''
    #create empty dataframes for the dfs the could get created in validate
    null_last_seen_df = pd.DataFrame()
    trial_df = pd.DataFrame()
    after_last_seen_df = pd.DataFrame()
    
    if fraction_of_population != 1:
        #select a fraction of the user_ids to speed up computations
        udf = random_sample(udf, fraction_of_population)

    if validate_dfs or fraction_of_population != 1: 
        #validate the input dataframes
         (udf, sdf, null_last_seen_df, 
          trial_df, after_last_seen_df 
         ) = validate.validate(udf, sdf, trial = trial)         
        
    if (date_str_to_period and (not validate_dfs) and 
        fraction_of_population == 1):
        #convert date like strs to period objects
        udf = dates.to_date(udf)
        sdf = dates.to_date(sdf)       
        
    return (udf, sdf, null_last_seen_df, trial_df, after_last_seen_df )
        
        

