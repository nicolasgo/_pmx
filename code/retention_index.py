'''module for the definition of rentention index and  related code.
   Created by Robert Kruhlak
'''   
## use floating point division always (ie matlab, python 3.x)
from __future__ import division

import numpy as np
from .plot import histogram_subplots, histogram_plot, sub_range

class RetentionIndex(object):
    '''represents Engagement of the cohorts on the social network
    '''
    def __init__(self, cohorts_df, cohort_arr):
        '''initialize class instance
           Input: cohorts, Cohorts class instance
                  cohort_arr, np.array of datetime.date objects representing
                              the cohorts of interest.
                  
        '''
        self.cohorts_df = cohorts_df
        #make sure it is a np.array
        self.cohort_arr = np.asarray(cohort_arr)
        self.num_cohorts = len(cohort_arr)
       
    def plot(self, cohort, log = False, xlabel = None, ylabel = None, 
             min_x = 0, sharey = True):
        '''****Bug in IPython that does not allow this at the time being
           see interact doesn't work with instance methods #6278 
           high-priority so hopefully it will be fixed soon.
           ****
           method to call when we want to plot engagement rate as a function
           of time using IPython.html.widgets in an IPython notebook.
           All input parameters are passed from widgets interact and are 
           typically the index of the parameters name. It is done this way
           because the parameters name is used as the label on the interactive
           widget.
           Input: cohort, int, better description is center_index (ie the cohort
                               that will be plotted in the middle
                  log, Boolean, use a log scale or not for the y axis
        '''
        #rename cohort to the more appropriate center_index
        center_index = cohort
        
        if self.num_cohorts >= 3: #need a minimum of three otherwise subplots 
                                  #does not work!!!!
            
            #cohort range shortened because there is a function called 
            #cohort_range
            crange = sub_range( center_index, self.cohort_arr, 
                                self.num_cohorts ) 
            
            df = self.cohorts_df.ix[crange]
            
            ax = histogram_subplots( crange, df, log = log, xlabel = xlabel,
                                     ylabel = ylabel, min_x = min_x, 
                                     sharey =  sharey) 
      
        else:
            
            #select the chosen cohort from the cohort_arr 
            #(not cohort is an index)
            mycohort = self.cohort_arr[cohort]
            df = self.cohorts_df.ix[mycohort]
            ax = histogram_plot(mycohort, df, log = log, xlabel = xlabel,
                                ylabel = ylabel )

        return ax


def retention_index(df):
    '''function to calculate the retention index from a dataframe with 
       columns 'joined' and 'last_seen'. This is typically the dataframe
       associated with the User class instance but could be any dataframe.
       Input: df, DataFrame
       Output: retention_index, Series
    '''
    #Original definition
    #return (df.last_seen - df.joined)/(pd.to_datetime('now') - df.joined)
    #The original does not work when we  have irregular updates to the 
    #datasets. The most recent cohorts get penalized too heavily
    # because they have fewer days to work with.
    most_recent_date = df.last_seen.max()
    age = (most_recent_date - df.joined)
    
    retention_index = (df.last_seen - df.joined)/age
    #There is a possiblily tha the most_recent_date = joined which 
    #could create an infinity. Replace with 1
    
    return retention_index.replace([np.inf, -np.inf], 1)

