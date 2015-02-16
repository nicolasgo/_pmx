# Config file for ipython_config.py
import datetime
import pandas as pd
import numpy as np
import seaborn as sns
from pandas import DataFrame, read_csv

print '*** ++in config'

# Global variables
_rootdir='/Users/Nicolas/dev/'

sns.set_palette("deep", desat=.6)
sns.set_context(rc={"figure.figsize": (8, 4)})


# Make graphs prettier
pd.set_option('display.width', 400)
pd.set_option('display.line_width', 4)
pd.set_option('display.max_columns', 15)
pd.set_option('display.mpl_style', 'default')

# Make the fonts bigger
matplotlib.rc('figure', figsize=(8, 5))
matplotlib.rc('font', family='normal', weight='bold', size=18)

print 'configured as per my config'
print '*** ++out config'
