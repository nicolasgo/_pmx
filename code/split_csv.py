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
import subprocess
import string
import string

def main(fname, first_chars = None):
    '''main function of the module. Purpose is to split large .csv files
       by the first char of the user_id. This is accomplished using 
       a bash command in  a subprocess.
    
       Input: fname, str, filename of interest
              first_chars, list of first characters of the user_id. Currently,
                           0 .. f (hex)
    '''       
    if first_chars is None:
        
        first_chars = get_first_chars()

    #split the fname in pieces delimited by '.'   
    pieces = fname.split('.')
    #insert an input location so we can increment the 
    #output file names.
    fname_out = pieces[0]+'_{0}.'+ '.'.join(pieces[1:])

    cmd = "cat {0} | grep '^{1}' > {2}"
    
    for char in first_chars:
        # no block, it start a sub process.
        #specific output file for this loop
        print char
        my_out = fname_out.format(char)
        #create command
        cmd_bash = cmd.format(fname, char, my_out )
        #create subprocess. Must have shell = True as it is bash cmd
        p = subprocess.Popen(cmd_bash, shell = True,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE
                            )

        # and you can block util the cmd execute finish
        #p.wait()

def get_first_chars(method = 'hex'):
    '''function to get the first characters of randomized ids
       Input: method, str in ('hex', 'dec')
       Output: list of characters
    '''
    #decimal first chars
    first_chars = range(10)

    if method == 'hex':
        #list of a,b,c ... f
        abcs = [ val for val in string.lowercase[:6]]
        #extend the list with hex digits
        first_chars.extend(abcs)

    return first_chars
#if __name__ == __main__:
#    fname = 'sessions23.pv.a.csv'
#    main(fname)
