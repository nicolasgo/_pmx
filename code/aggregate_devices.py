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
import clean 

class Aggregate(object):
    '''represents the aggregation of files for device analysis'''
    def __init__(self,sessions_filename, first_chars =None):
        '''initialize'''
        fname2  = 'data/sessions23.pv.a.csv'
        temp_df = pd.read_csv(fname2, nrows=2)
        #The 23 files still have the ua column but the 55 files don't
        if '55' in sessions_filename:
            temp_df = temp_df.drop('ua', axis = 1)

        if ('23' in sessions_filename) and ('1411' in sessions_filename):
            temp_df = temp_df.drop('ua', axis = 1)

        self.columns = temp_df.columns
        
        #the sessions .csv file is split by the first character of the
        #user_id
        if first_chars is None:
            self.first_chars = get_first_chars()
        else:
            self.first_chars = first_chars
        pieces = sessions_filename.split('.')
        #insert an input location so we can increment the 
        #filename
        
        #files we need to cycle over
        self.sessions_i_fn = pieces[0]+'_{0}.'+ '.'.join(pieces[1:])
        #combined file name
        self.sessions_devices_fn = pieces[0]+'_devices.'+ '.'.join(pieces[1:])

    def run(self, nrows = None):
        '''aggregate
           Input: nrows, int number of rows to load from each file
           Output: df, resampled data
        '''
        #loop over all the pieces of the daily_sums  dataset
        pieces = {}
        df = None
        start = time.time()
        d_columns = ['time', 'duration', 'pv', 'dfamily', 'dmodel', 'dversion',
                     'activ', 'avata', 'conve', 'frien', 'help', 'home', 
                     'inbox', 'info', 'media', 'mymed', 'publi',  
                     'uploa', 'variety' ]
        for char in self.first_chars:
            #read in the pieces
            temp_df = pd.read_csv(self.sessions_i_fn.format(char), 
                             index_col = 0, names = self.columns,
                             nrows = nrows)[d_columns].fillna('Other')

            temp_df.dmodel = clean.clean_dmodel(temp_df.dmodel)
            #print temp_df.head()
            pieces[char] = temp_df
        
       
        #concatentate the pieces     
        df = pd.concat( pieces.values())

        
        #create a multiindex
        df = df.to_csv(self.sessions_devices_fn)
        

def main(  sessions_fname = None, first_chars = None, 
          nrows = None):
    '''main function of the module. Purpose is to split large .csv files
       by the first char of the user_id. This is accomplished using 
       a bash command in  a subprocess.
    
       Input: fname, str, filename of interest
              first_chars, list of first characters of the user_id. Currently,
                           0 .. f (hex)
    '''       

    if sessions_fname is None:
        sessions_fname = 'data/sessions23.pv.a.csv'

    aggregate = Aggregate( sessions_fname, first_chars)

    return aggregate.run(nrows = nrows)

if __name__ == '__main__':
    #while testing only take 100 rows from each file (None gets the entire file)
    main(nrows = None)
