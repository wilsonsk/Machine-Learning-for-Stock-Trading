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
import scipy.optimize as spo


############### Global Variables #################

global arg_check
arg_check = 0
global risk_free_rate
risk_free_rate = 0

############### Optimize Portfolio #################

def symbol_to_path(symbol, base_dir="./csv_files"):
	#return CSV file path given ticker symbol
	return os.path.join(base_dir, "{}.csv".format(str(symbol)))

def port_optimizer():
	start_val = float(sys.argv[1])	
	start_date = str(sys.argv[2])	
	end_date = str(sys.argv[3])
	df1_start_date = '2000-01-01'
	df1_end_date = '2016-08-23'
	dates = pd.date_range(df1_start_date, df1_end_date)
	df1, symbols, allocs = get_data_frame(dates)
	print "SYMBOLS: ", symbols, " | ALLOCATIONS: ", allocs
	df1 = df1.ix[start_date : end_date]
	print "Adj Close Prices:\n", df1

	#Set Optimizer Conditions

        # x == the allocations that we are looking for -- optimizer will try different combinations in order to discover the best set of allocations that optimizes this function
        # initial guess == allocs for portfolio assets
        initial_guess = allocs

        #define constraints:    # Constraints essential to get correct solution: are properties of x that must be "true"
                                # we want the sum of our allocations to add up to 1
                #http://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html
                        # 'type': str -- constraint type: 'eq' for equality, 'ineq' for inequality
                                # equality constraint means that the constraint function result is to be zero whereas inequality means that it is to be non-negative
                        # 'fun': callable -- the function defining the constraint
        constraints = ({'type': 'eq', 'fun' : lambda inputs: 1 - (np.sum(np.absolute(inputs)))})

        #define range (aka boundary):
                                # Ranges enable faster optimization: limits on values for x -- tells optimizer to only look in specific ranges for x
                                # for each of the allocations its only worth looking for values between 0 and 1 (0% - 1%)
                #http://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html
                        # bounds: sequence, optional
                                # Bounds for variables (only for L-BFGS-B, TNC, and SLSQP optimize algorithms)
                                # (min, max) pairs for each element in x, defining the bounds on that parameter
                                # use None for one of min or max when there is no bound in that direction
        range = []
        for i in allocs:
                range.append((0.0, 1.0))

        #Test: Optimize Sharpe Ratio
        #optimized_res = spo.minimize(test_opt_sharpe, initial_guess, args=(df1,), method='SLSQP', bounds=range, constraints=constraints, options={'disp': True})
        #print "TEST OPT ALLOC: ", symbols, optimized_res.x

	#Actual: Optimize Sharpe Ratio
        optimized_res = spo.minimize(optimize_sharpe_ratio, initial_guess, args=(df1,), method='SLSQP', bounds=range, constraints=constraints, options={'disp': True})

	#Calc Optimized Stats
	normalized_df = normalize(df1)
	optimized_allocations = allocated(normalized_df, optimized_res.x)
	optimized_position_vals = position_vals(optimized_allocations, start_val)	
	optimized_port_vals = portfolio_vals(optimized_position_vals)

	#Print Optimized Stats
	print "Normalized Prices:\n", normalized_df
	print "Optimized Allocations:\n", optimized_allocations
	print "Optimized Pos Vals:\n", optimized_position_vals
	print "Optimized Port Vals: \n", optimized_port_vals
	opt_cum_ret = (optimized_port_vals[-1] / optimized_port_vals[0]) - 1
	print "CUMUMLATIVE RETURNS BASED ON MINIMIZED SHARPE RATIO: ", opt_cum_ret
        print "OPTIMAL ALLOCATIONS BASED ON MINIMIZED SHARPE RATIO: ", symbols, optimized_res.x
	opt_sharpe = optimize_sharpe_ratio(optimized_res.x, df1)
        print "Sharpe Ratio of Daily Returns:"
        print "Optimized Frequency: Daily (k=252): ", opt_sharpe * (math.sqrt(252)) * -1
        print "Optimized Frequency: Weekly (k=52): ", opt_sharpe * (math.sqrt(52)) * -1
        print "Optimized Frequency: Monthly (k=12): ", opt_sharpe * (math.sqrt(12)) * -1
        print "Optimized Frequency: Yearly (k=1): ", opt_sharpe * (math.sqrt(1)) * -1

	#Test: Optimized Cumulative Returns
        #optimized_res = spo.minimize(test_opt_cum, initial_guess, args=(df1,), method='SLSQP', bounds=range, constraints=constraints, options={'disp': True})
	#print "TEST CUM RETURNS ALLOCATIONS: ", optimized_res.x

	#Actual: Optimize Cumulative Ratio
        optimized_res = spo.minimize(optimize_cumulative_returns, initial_guess, args=(df1,), method='SLSQP', bounds=range, constraints=constraints, options={'disp': True})

	#Calc Optimized Stats
	opt_cum_ret = optimize_cumulative_returns(optimized_res.x, df1)
	print "OPTIMAL CUMUMLATIVE RETURNS BASED ON MINIMIZED CUMULATIVE RETURNS: ", opt_cum_ret * -1
        print "OPTIMAL ALLOCATIONS BASED ON MINIMIZED CUMULATIVE RETURNS: ", symbols, optimized_res.x

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
	allocations = []
	#get allocs and store in allocations tuple
	for alloc in sys.argv[4+arg_check:]:
		allocations.append(alloc)
	return tempdf, symbols, allocations

############### Portfolio Calcs #################

def normalize(dframe):
	#normalize stock prices using the first row of the dataframe
	#normalize data so that all prices start at $1
	# this helps us see movement (up or down) compared to the others
	return dframe/dframe.ix[0, :]

def allocated(dframe, allocations):
	#convert list into np.array
	narr_allocations = np.array([allocations], dtype=np.float64)
	return narr_allocations * dframe

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

def optimize_cumulative_returns(allocs, df):
	start_val = float(sys.argv[1])	
	#Portfolio Calcs
	df = normalize(df)
	narr_allocations = allocated(df, allocs)
	narr_position_vals = position_vals(narr_allocations, start_val)	
	port_vals = portfolio_vals(narr_position_vals)

	cum_ret = (port_vals[-1] / port_vals[0]) - 1
	# cum_ret * -1 to get optimal value
	return cum_ret * -1

def average_daily_returns(daily_ret):
	return daily_ret.mean()

def std_deviation_daily_returns(daily_ret):
	return daily_ret.std()

def optimize_sharpe_ratio(allocs, df):
	#the greater the std deviation the smaller the sharpe ratio, the larger the risk the smaller the sharpe ratio, the larger the daily return the greater the sharpe ratio
	#this equation is passed to optimizer where it attempts to use different combos of parameters (allocations, prices) until sharpe ratio is minimalized (this value is reversed via * -1 because want 
	#largest sharpe ratio value
	start_val = float(sys.argv[1])	

	#Portfolio Calcs
	df = normalize(df)
	narr_allocations = allocated(df, allocs)
	narr_position_vals = position_vals(narr_allocations, start_val)	
	port_vals = portfolio_vals(narr_position_vals)
	
	#Portfolio Stats
	daily_ret = daily_returns(port_vals)
	std_daily_ret = std_deviation_daily_returns(daily_ret)

	#Sharpe Ratio Calc
	sharpe = daily_ret - risk_free_rate
	sharpe_numerator = sharpe.mean()
	sharpe = sharpe_numerator / std_daily_ret
	# sharpe * -1 to get optimal value

	return sharpe * -1

def test_opt_sharpe(allocs, df):
	start_val = float(sys.argv[1])	
	df = normalize(df)
	allocs = df * allocs
	postvalues = allocs * start_val
	portfolioValues = postvalues.sum(axis=1)

	dailyReturns = (portfolioValues / portfolioValues.shift(1)) - 1
	dailyReturns = dailyReturns.ix[0:]

	dailyReturnsStD = dailyReturns.std()
	dailyReturnsMean = dailyReturns.mean()
	sharpeRatio = dailyReturnsMean / dailyReturnsStD
	return sharpeRatio*-1

def test_opt_cum(allocs, df):
	start_val = float(sys.argv[1])
	df = normalize(df)
	allocs = df * allocs
	postvalues = allocs * start_val
	portfolioValues = postvalues.sum(axis=1)
	cumulativeReturns = (portfolioValues[-1] / portfolioValues[0]) - 1
	return cumulativeReturns*-1

if __name__ == "__main__":
	if len(sys.argv) >= 5:
		port_optimizer()
	else:
		print "usage: python portfolio.py <start_value> <start_date: yr-month-day> <end_date: yr-month-day> <tickerSymbol> ... <tickerSymbol_n> <fund_allocation: 0.0 - 1.0> ... <fund_allocation_n: 0.0 - 1.0>"


	
