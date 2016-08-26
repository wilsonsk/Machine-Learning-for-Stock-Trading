#Portfolio Optimizer:
	# Purpose:	
		# Given a set of assets, and a time period, find an allocation of funds to assets that maximizes performance
			# performance -- could chose from a number of metrics: cumulative return, risk aka volatility, or risk adjusted return (aka Sharpe Ratio) 
		# easiest to write an optimizer for cumulative return: because you only need to find the single stock that maximized return over that time period
		# if you are going to optimize for minimum volatility or Sharpe ratio you have to evaluate various combinations of those stocks whereas cumulative return is 100% allocation to highest returnstock
	# How to use: 
		# 1. Framing the portfolio optimization problem as a minimalization problem
			# in order to use an optimizer that minimalizes, 3 things required:
				# 1. Provide a function to minimize -- f(x) 
					# x == the allocations that we are looking for -- optimizer will try different combinations in order to discover the best set of allocations that optimizes this function
					# x == can have multiple dimensions -- where each dimension of x is an allocation to each of the stocks
						# so if trying to solve for a portfolio of 4 stocks, x will have 4 dimensions and the value for each of those dimensions is the % of funds to allocate to each of
						# those stocks
					# f() == NOT Sharpe ratio equation -- in this case the optimizer will try finding allocations that minimize the Sharpe ratio (i.e., find the smallest Sharpe ratio)
					# f() == we want LARGEST Sharpe ratio 
					# f() == Sharpe ration * -1 -- optimize for negative Sharpe ratio which will find the best allocation set that optimizes the Sharpe ratio function
				# 2. Provide an initial guess for x 
					# initial guess == allocs for portfolio assets
				# 3. Call the optimizer
		# Ranges and Constraints:
			# Ranges enable faster optimization: limits on values for x -- tells optimizer to only look in specific ranges for x 
				# for each of the allocations its only worth looking for values between 0 and 1 (0% - 1%)
			# Constraints essential to get correct solution: are properties of x that must be "true"
				# we want the sum of our allocations to add up to 1
	# How it works:
                # checks function value with initial guess input
                # tests an input value slightly above initial guess and tests an input value slightly below initial guess
                # finds slope of the equation of the newly varied guess
                # performs a gradient desent (goes downhill due to minimizing action)
                # tests another input value down along that slope
                # test an input value slightly below the above input, tests an input value slightly above the previous input
                # repeat
	
import pandas as pd
import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import math

############### Global Variables #################

arg_check = 0
risk_free_rate = 0

############### Portfolio Manager Functions -- interface #################

def symbol_to_path(symbol, base_dir="./csv_files"):
	#return CSV file path given ticker symbol
	return os.path.join(base_dir, "{}.csv".format(str(symbol)))

def port_manager():
	start_val = float(sys.argv[1])	
	start_date = str(sys.argv[2])	
	end_date = str(sys.argv[3])
	df1_start_date = '2000-01-01'
	df1_end_date = '2016-08-23'
	dates = pd.date_range(df1_start_date, df1_end_date)
	df1,symbols = get_data_frame(dates)
	#print "SYMBOLS: ", symbols

	#Portfolio Calcs
	#slice df1
	df1 = df1.ix[start_date : end_date]
	print "Adj Close Prices:\n", df1
	df1 = normalize(df1)	
	print "Normalized Prices:\n", df1
	narr_allocations, allocs = allocated(df1)
	print "Allocated Prices: (allocated funds: ", allocs, "):\n", narr_allocations
	narr_position_vals = position_vals(narr_allocations, start_val)	
	print "Position Prices:\n", narr_position_vals
	port_vals = portfolio_vals(narr_position_vals)
	print "Portfolio Prices:\n", port_vals	

	#Portfolio Stats
	daily_ret = daily_returns(port_vals)
	print "Daily Returns:\n", daily_ret
	cum_ret = optimize_cumulative_returns(port_vals)
	print "Cumulative Returns:\n", cum_ret
	ave_daily_ret = average_daily_returns(daily_ret)
	print "Average Daily Returns:\n", ave_daily_ret
	std_daily_ret = std_deviation_daily_returns(daily_ret)
	print "Standard Deviation Daily Returns:\n", std_daily_ret
	sharpe = optimize_sharpe_ratio(daily_ret, std_daily_ret)
	print "Sharpe Ratio of Daily Returns:"
	print "Sample Frequency: Daily (k=252): ", sharpe * (math.sqrt(252))
	print "Sample Frequency: Weekly (k=52): ", sharpe * (math.sqrt(52))
	print "Sample Frequency: Monthly (k=12): ", sharpe * (math.sqrt(12))
	print "Sample Frequency: Yearly (k=1): ", sharpe * (math.sqrt(1))
	
	axis = port_vals.plot(title="Daily Portfolio Value", label="Portfolio")
	axis.set_xlabel("Date")
	axis.set_ylabel("Price")
	plt.legend(loc='upper left')
	plt.show()

	optimize_portfolio(allocs, symbols, start_val)
		

############### Create Dataframe #################

def get_data_frame(dates):
	tempdf = pd.DataFrame(index=dates)
	symbols = []
	for symbol in sys.argv[4:]:
		#check contents of symbol for any number values -- this indicates an allocation and not a symbol
		num_check = False
		for i in range(0, len(symbol)):
			if symbol[i] == '0' or symbol[i] == '1' or symbol[i] == '2' or symbol[i] == '3' or symbol[i] == '4' or symbol[i] == '5' or symbol[i] == '6' or symbol[i] == '7' or symbol[i] == '8' or symbol[i] == '9':
				num_check =True
				break
		if num_check == False:
			symbols.append(symbol)
			global arg_check
			arg_check = arg_check + 1
			#join .csv with new dataframe of dates
			csv_df = pd.read_csv(symbol_to_path(symbol), index_col='Date', parse_dates=True, usecols=['Date', 'Adj Close'], na_values=['nan'])
			#prevent clashing column names by renaming column names with each symbol
			csv_df = csv_df.rename(columns={'Adj Close': symbol}) 
			#inner join
			tempdf = tempdf.join(csv_df, how='inner')
		else:
			break				
	return tempdf, symbols

############### Portfolio Calcs #################

def normalize(dframe):
	#normalize stock prices using the first row of the dataframe
	#normalize data so that all prices start at $1
	# this helps us see movement (up or down) compared to the others
	return dframe/dframe.ix[0, :]

def allocated(dframe):
	global arg_check
	allocations = []
	#get allocs and store in allocations tuple
	for alloc in sys.argv[4+arg_check:]:
		allocations.append(alloc)
	#convert list into np.array
	narr_allocations = np.array([allocations], dtype=np.float64)
	return narr_allocations * dframe, allocations

def position_vals(narr_allocations, start_val):
	pos_val = narr_allocations * start_val
	return pos_val

def portfolio_vals(pos_val):
	port_vals = pos_val.sum(axis=1)
	return port_vals

############### Portfolio Stats #################

def daily_returns(port_vals):
	daily_ret = port_vals.copy()
	daily_ret = (port_vals / port_vals.shift(1)) - 1
	daily_ret.ix[0] = 0
	return daily_ret

def optimize_cumulative_returns(port_vals):
	cum_ret = (port_vals[-1] / port_vals[0]) - 1
	# cum_ret * -1 to get optimal value
	return cum_ret * -1

def average_daily_returns(daily_ret):
	return daily_ret.mean()

def std_deviation_daily_returns(daily_ret):
	return daily_ret.std()

def optimize_sharpe_ratio(daily_ret, std_daily_ret):
	sharpe = daily_ret - risk_free_rate
	sharpe = sharpe.mean()
	sharpe = sharpe / std_daily_ret
	# sharpe * -1 to get optimal value
	return sharpe * -1


############### Optimize Portfolio #################
def optimize_portfolio(allocs, symbols, start_val):
	# x == the allocations that we are looking for -- optimizer will try different combinations in order to discover the best set of allocations that optimizes this function
	# initial guess == allocs for portfolio assets
	print "ALLOCS: ", allocs, ". SYMOBLS: ", symbols, ". START_VAL: ", start_val





if __name__ == "__main__":
	if len(sys.argv) >= 5:
		port_manager()
	else:
		print "usage: python portfolio.py <start_value> <start_date: yr-month-day> <end_date: yr-month-day> <tickerSymbol> ... <tickerSymbol_n> <fund_allocation: 0.0 - 1.0> ... <fund_allocation_n: 0.0 - 1.0>"


	
