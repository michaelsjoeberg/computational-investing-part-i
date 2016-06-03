# import pandas as pd
import csv
import sys
import numpy as np
import math
import copy
# import QSTK.qstkutil.qsdateutil as du
import time
import datetime as dt
# import QSTK.qstkutil.DataAccess as da
# import QSTK.qstkutil.tsutil as tsu
# import QSTK.qstkstudy.EventProfiler as ep

def read_file(filename):
	# create lists for symbols and dates
	list_symbols = []
	list_dates = []

	# read csv file
	reader = csv.reader(open(filename, 'rU'), delimiter=',')
	for row in reader:
		list_symbols.append(row[3])
		date_temp = dt.datetime(int(row[0]), int(row[1]), int(row[2]))
		list_dates.append(date_temp)

	# remove duplicates
	list_symbols = list(set(list_symbols))

	return list_symbols, list_dates
	# print list_symbols, list_dates

if __name__ == '__main__':
	# set arguments as variables
	starting_cash = str(sys.argv[1])
	file_orders = str(sys.argv[2])
	file_value = str(sys.argv[3])

	# read orders file
	ls_symbols, ls_dates = read_file(file_orders)

	dt_start = ls_dates[0]
	dt_end = ls_dates[-1] + dt.timedelta(days=1)

    # ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))

    # dataobj = da.DataAccess('Yahoo')
    # ls_symbols = dataobj.get_symbols_from_list('sp5002012')
    # ls_symbols.append('SPY')

    # ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    # ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    # d_data = dict(zip(ls_keys, ldf_data))


