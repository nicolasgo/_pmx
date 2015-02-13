'''module for engagement related code.
   Created by Robert Kruhlak
   Note: cohorts are defined by a datetime.date object. This appears to be
         working well.
         They can be changed to a TimeStamp object (includes hours, mins, secs
         etc) with a couple changes. 
         1) in the set_to_start_of_month function in cohorts
            uncomment: return mydatetime.replace( day = 1, minute = 0, hour = 0, 
                              second = 0, microsecond = 0) and comment the
                    current return statement.
         2) in dates.py uncomment:  comment the current the list comprehension
'''
## use floating point division always (ie matlab, python 3.x)
from __future__ import division

import numpy as np

from .cohort import sub_range
from .plot import engagement_subplots, engagement_plot

class Engagement(object):
    '''represents Engagement of the cohorts on the social network
    '''
    def __init__(self, cohorts, cohort_arr):
        '''initialize class instance
           Input: cohorts, Cohorts class instance
                  cohort_arr, np.array of datetime.date objects representing
                              the cohorts of interest.
                  
        '''
        self.cohorts = cohorts
        #make sure it is a np.array
        self.cohort_arr = np.asarray(cohort_arr)
        self.num_cohorts = len(cohort_arr)
        self.time_units =  ['days', 'hours', 'minutes']

    def plot(self, cohort,  time_span, units, normalized, window, visible,
             drop_first = True, drop_last = True, min_retention_index = 0,
             max_retention_index = 1):
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
                  units, int, better description is the time_units_index
                  normalized, Boolean, True/False
                  window, int, number of days for the rolling mean/std
                  visible, Boolean, make axes visible or not.
                  drop_first, Boolean, drop the first index in the dataframe:
                                       use this until we have a method 
                                       for determining if we have a full
                                       day, week, month as the first index
                  drop_last, Boolean, drop the last index in the dataframe
                                      use this until we have a method 
                                       for determining if we have a full
                                       day, week, month as the last index      
        '''
        #rename cohort to the more appropriate center_index
        center_index = cohort
        time_span_index = time_span
        time_span_list = ['D', 'W', 'M']
        time_span = time_span_list[time_span_index]
        
        if self.num_cohorts >= 3: #need a minimum of three otherwise subplots 
                                  #does not work!!!!
            
            #cohort range shortened because there is a function called 
            #cohort_range
            crange = sub_range( center_index, self.cohort_arr, 
                                self.num_cohorts ) 
            
            df = self.cohorts.get_engagement_rates( time_span = time_span, 
                                                    cohort_range = crange, 
                                                    units = 
                                                    self.time_units[units], 
                                                    normalized = normalized,
                                                    min_retention_index = 
                                                    min_retention_index,
                                                    max_retention_index =
                                                    max_retention_index)
            
            ax = engagement_subplots( crange, df, 
                                      units = self.time_units[units],  
                                      normalized = normalized, window = window,
                                      time_span = time_span,
                                      drop_first = drop_first,
                                      drop_last = drop_last ) 

            for ax_name in ax:
                ax_name.set_visible(visible)
      
           
        else:
            time_units = self.time_units[units]
            #select the chosen cohort from the cohort_arr 
            #(note cohort is an index)
            mycohort = self.cohort_arr[cohort]
            df = self.cohorts.get_engagement_rates( time_span = time_span, 
                                                    cohort_range = [mycohort], 
                                                    units = time_units, 
                                                    normalized = normalized,
                                                    min_retention_index = 
                                                    min_retention_index)

            ax = engagement_plot(mycohort, df, time_units = time_units,  
                                 normalized = normalized, window = window,
                                 time_span = time_span, drop_first = drop_first,
                                 drop_last = drop_last )

        return ax
        
                       
