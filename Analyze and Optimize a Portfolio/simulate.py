# QSTK Imports
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

# Third Party Imports
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import itertools

# function for simulating allocations
def simulate(startdate, enddate, symbols):
    ''' 
    Function for sharpe ratio, volatility, average daily
    return, and cumulative daily return of allocation.
    '''

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

    # initiate optimization variables
    allocations = [0.0, 0.0, 0.0, 0.0]
    best_portfolio = [];
    best_sharpe = 0;

    # variations of legal iterations
    iteration = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0]

    for i in range(0, len(allocations) + 1):
        for subset in itertools.product(iteration, repeat=4):
            
            allocations = [item for item in subset]

            if np.sum(allocations) == 1.0:

                print allocations

                allocated_price = na_normalized_price.copy()

                # multiply normalized price with allocation
                allocated_price[:,0] = allocated_price[:,0] * allocations[0]
                allocated_price[:,1] = allocated_price[:,1] * allocations[1]
                allocated_price[:,2] = allocated_price[:,2] * allocations[2]
                allocated_price[:,3] = allocated_price[:,3] * allocations[3]

                # copy normalized prices to new array and calculate daily return
                na_rets = allocated_price.copy()

                # get sum of each row (cumulative daily return)
                n = 0
                for i in na_rets:
                    na_rets[n] = np.sum(na_rets[n])
                    n = n + 1

                # naturalize average returns
                na_avg_ret = na_rets[:,0].copy()
                tsu.returnize0(na_avg_ret)

                # calculate daily return, standad deviation,
                # cumulative return, and sharpe
                average_daily_ret = np.average(na_avg_ret)
                volatility = np.std(na_avg_ret)
                cumulative_ret = na_rets[-1,0]
                sharpe = np.sqrt(252) * average_daily_ret / volatility

                # set sharpe ratio
                if (best_sharpe == 0) or (best_sharpe < sharpe):
                    best_sharpe = sharpe.copy()
                    best_portfolio = allocations

    print "Optimal Allocation:", best_portfolio
    print "Highest Sharpe Ratio:", best_sharpe

    return

if __name__ == '__main__':

    # set input variables
    startdate = dt.datetime(2010, 1, 1)
    enddate = dt.datetime(2010, 12, 31)
    symbols = ['AXP', 'HPQ', 'IBM', 'HNZ']

    # initiate function
    simulate(startdate, enddate, symbols)
