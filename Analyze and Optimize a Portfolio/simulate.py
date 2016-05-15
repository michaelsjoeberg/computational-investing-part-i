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

    # set time and day
    dt_timeofday = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(startdate, enddate, dt_timeofday)

    # create object
    c_dataobj = da.DataAccess('Yahoo', cachestalltime=0)

    # keys to read from datas
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

    # get data
    ldf_data = c_dataobj.get_data(ldt_timestamps, symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    # create array of close prices and normalize
    na_price = d_data['close'].values
    na_normalized_price = na_price / na_price[0, :]

    # multiply normalized price with allocation
    na_normalized_price[:,0] = na_normalized_price[:,0] * allocations[0]
    na_normalized_price[:,1] = na_normalized_price[:,1] * allocations[1]
    na_normalized_price[:,2] = na_normalized_price[:,2] * allocations[2]
    na_normalized_price[:,3] = na_normalized_price[:,3] * allocations[3]

    # copy normalized prices to new array and calculate daily return
    na_rets = na_normalized_price.copy()

    # get sum of each row (cumulative daily return)
    n = 0
    for i in na_rets:
        na_rets[n] = np.sum(na_rets[n])
        n = n + 1

    # naturalize average returns
    na_avg_ret = na_rets[:,0].copy()
    tsu.returnize0(na_avg_ret)

    # calculate daily return, standad deviation, cumulative return, and sharpe
    average_daily_ret = np.average(na_avg_ret)
    volatility = np.std(na_avg_ret)
    cumulative_ret = na_rets[-1,0]
    sharpe = np.sqrt(252) * average_daily_ret / volatility

    # print results
    print "Start Date:", startdate
    print "End Date:", enddate
    print "Symbols:", symbols
    print "Optimal Allocations:", allocations
    print "Sharpe Ratio:", sharpe
    print "Volatility (stdev of daily returns):", volatility
    print "Average Daily Return:", average_daily_ret
    print "Cumulative Return:", cumulative_ret

if __name__ == '__main__':

    # set input variables
    startdate = dt.datetime(2010, 1, 1) # first day 2011
    enddate = dt.datetime(2010, 12, 31) # last day 2011
    symbols = ['AXP','HPQ','IBM','HNZ']
    allocations = [0.0,0.0,0.0,1.0]

    # initiate function
    simulate(startdate, enddate, symbols, allocations)
