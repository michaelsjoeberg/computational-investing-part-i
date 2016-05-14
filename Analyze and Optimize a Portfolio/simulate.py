# QSTK Imports
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

# Third Party Imports
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# function
def simulate(startdate, enddate, symbols, allocations):
    ''' Function '''
    
    # assign arguments
    ls_symbols = symbols
    dt_start = startdate
    dt_end = enddate

    # set time and day
    dt_timeofday = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)

    # create object
    c_dataobj = da.DataAccess('Yahoo')

    # keys to read from datas
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

    # get data
    ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

if __name__ == '__main__':
    simulate()

