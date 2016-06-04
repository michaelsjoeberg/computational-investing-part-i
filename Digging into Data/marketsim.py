import pandas as pd
import csv
import sys
import numpy as np
import math
import copy
import QSTK.qstkutil.qsdateutil as du
import time
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkstudy.EventProfiler as ep

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
	list_dates = list(set(list_dates))

	return list_symbols, list_dates
	# print list_symbols, list_dates

if __name__ == '__main__':
	# set arguments as variables
	# starting_cash = str(sys.argv[1])
	# file_orders = str(sys.argv[2])
	# file_value = str(sys.argv[3])

	starting_cash = "1000000"
	file_orders = "orders.csv"
	file_value = "values.csv"

	# read orders file
	ls_symbols, ls_dates = read_file(file_orders)

	ls_dates.sort()

	# set start and end date for trades
	dt_start = ls_dates[0]
	dt_end = ls_dates[-1] + dt.timedelta(days=1)

	# get data
	ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))
	dataobj = da.DataAccess('Yahoo')
	ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
	ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
	d_data = dict(zip(ls_keys, ldf_data))

	# create array of adjusted close prices and normalize
	na_price = d_data['close']
	#na_normalized_price = na_price / na_price[0, :]

	# trade matrix
	trade_matrix = {ls_symbols[0] : np.zeros(len(ls_dates)),
					ls_symbols[1] : np.zeros(len(ls_dates)),
					ls_symbols[2] : np.zeros(len(ls_dates)),
					ls_symbols[3] : np.zeros(len(ls_dates)),
					}

	trade_matrix = pd.DataFrame(trade_matrix, index=ls_dates)
	#print trade_matrix

	# allocations of stocks
	allocations = {ls_symbols[0] : 0.0,
					ls_symbols[1] : 0.0,
					ls_symbols[2] : 0.0,
					ls_symbols[3] : 0.0,
					}

	allocations = pd.DataFrame(allocations, index=ls_dates)

	# read csv file again
	reader = csv.reader(open(file_orders, 'rU'), delimiter=',')
	for row in reader:

		# set date for trade
		order_date = dt.datetime(int(row[0]), int(row[1]), int(row[2]))
		order_timestamp = du.getNYSEdays(order_date, order_date + dt.timedelta(days=1), dt.timedelta(hours=16))
		timestamp = order_timestamp[0]

		# set price for traded stock
		temp_data = dataobj.get_data(order_timestamp, [row[3]], ['close'])
		price_data = dict(zip(['close'], temp_data))
		price = price_data['close'].values
		price = int(price[0])

		if (row[4] == "Buy"):
			#allocations[row[3]] = allocations[row[3]] + int(row[5])
			trade_matrix.set_value(order_date, row[3], trade_matrix.get_value(order_date, row[3]) + int(row[5]))
			#total_cash = total_cash - (int(row[5]) * price)

		elif (row[4] == "Sell"):
			#allocations[row[3]] = allocations[row[3]] - int(row[5])
			trade_matrix.set_value(order_date, row[3], trade_matrix.get_value(order_date, row[3]) - int(row[5]))
			#total_cash = total_cash + (int(row[5]) * price)

	# total cash
	total_cash = int(starting_cash)

	# cash per day
	cash_matrix = pd.DataFrame(np.zeros(len(ldt_timestamps)), index=ldt_timestamps)
	#print cash_matrix

	cash_matrix.set_value(dt_start, 0, total_cash)

	trade_matrix.sort_index(inplace=True)
	cash_matrix.sort_index(inplace=True)

	for date in ldt_timestamps:
		date_timestamp = du.getNYSEdays(date, date + dt.timedelta(days=1), dt.timedelta(hours=16))
		timestamp = str(date_timestamp[0])

	#print allocations
	print trade_matrix
	#print cash_matrix