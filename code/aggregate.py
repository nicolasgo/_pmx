#!/usr/bin/env python
'''module for cohort related code.
   Created by Robert Kruhlak
   Note: cohorts are defined by a datetime.date object. This appears to be
         working well but all of the code has not been tested.
         They can be changed to a TimeStamp object (includes hours, mins, secs
         etc) with a couple changes. 
         1) in the set_to_start_of_month function
            uncomment: return mydatetime.replace( day = 1, minute = 0, hour = 0, 
                              second = 0, microsecond = 0) and comment the
                    current return statement.
         2) in dates.py uncomment:  comment the current the list comprehension
'''
## use floating point division always (ie matlab, python 3.x)
from __future__ import division
import pandas as pd
import time

from split_csv import get_first_chars

class Aggregate(object):
    '''Represents the resample class'''
    def __init__(self, sessions_filename, first_chars = None):
        '''initialize the class instance'''
        
        self.columns = pd.read_csv(sessions_filename, nrows=2).columns
      
        #the sessions .csv file is split by the first character of the
        #user_id
        if first_chars is None:
            self.first_chars = get_first_chars()
        else:
            self.first_chars = first_chars
        pieces = sessions_filename.split('.')
        #insert an input location so we can increment the 
        #filename
        self.sessions_agg_fn = pieces[0]+'_daily_sums.'+ '.'.join(pieces[1:])
        self.sessions_i_out_fn = pieces[0]+'_{0}_daily_sums.'+ '.'.join(pieces[1:])

    def daily(self, nrows = None):
        '''create daily dataframe'''
                
        self.run(nrows = nrows)

    def run(self, nrows = None):
        '''resample
           Input: time_span, str, in ('D', 'W', 'M')
                  how, str or dict, {'column_name':'how_to_resample',...}
           Output: df, resampled data
        '''
        #loop over all the pieces of the daily_sums  dataset
        pieces = {}
        df = None
        start = time.time()
        for char in self.first_chars:
            #read in the pieces
            pieces[char] = pd.read_csv(self.sessions_i_out_fn.format(char), 
                                       index_col = 0, nrows = nrows)
        
        #concatentate the pieces     
        df = pd.concat( pieces.values(), ignore_index = True)
        #rename the index column to time
        df= df.rename(columns = {'index' : 'time', 'count' : 'sessions'})
        #create a multiindex
        df = df.set_index(['user_id','time'])
        
        df.to_csv(self.sessions_agg_fn.format(char))
        print 'time to create: {0:.2} minutes'.format((time.time()-start)/60)    


def main( users_fname = None, sessions_fname = None, first_chars = None, 
          nrows = None):
    '''main function of the module. Purpose is to split large .csv files
       by the first char of the user_id. This is accomplished using 
       a bash command in  a subprocess.
    
       Input: fname, str, filename of interest
              first_chars, list of first characters of the user_id. Currently,
                           0 .. f (hex)
    '''       
    if users_fname is None:
        #filenames for the two .csv files version 2 located in the data folder

        users_fname = 'data/users23.a.csv'

    if sessions_fname is None:
        sessions_fname = 'data/sessions23.pv.a.csv'

    aggregate = Aggregate( sessions_fname, first_chars)

    return aggregate.daily(nrows = nrows)

if __name__ == '__main__':
    #while testing only take 100 rows from each file (None gets the entire file)
    main(nrows = None)
