import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as ts
import QSTK.qstkutil.DataAccess as da

import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd

ls_symbols = ["AAPL","GLD","GOOG","$SPX","XOM"]
ls_keys = ['open','high','low','close','volume','actual_close']
# print ls_symbols

# set up date and times
dt_start = dt.datetime(2010,1,1)
dt_end = dt.datetime(2010,1,15)
dt_timeofday = dt.timedelta(hours=16)

ldt_timestamps = du.getNYSEdays(dt_start,dt_end,dt_timeofday)
# print ldt_timestamps

# create data object
c_dataobj = da.DataAccess('Yahoo')

# read data
ldf_data = c_dataobj.get_data(ldt_timestamps,ls_symbols,ls_keys)
# print ldf_data

# assign key to value in dictionary
d_data = dict(zip(ls_keys,ldf_data))
# print d_data['close']

# plot values
na_price = d_data['close'].values
# print na_price

plt.clf() # clear plot
plt.plot(ldt_timestamps,na_price) # plot
plt.legend(ls_symbols) # add legend
plt.ylabel('Adjusted Close') # add y-label
plt.xlabel('Date') # add x-label
plt.savefig('adjustedclose.pdf', format='pdf') # save as pdf


