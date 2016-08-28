#daily portfolio value:
	# start_val = 1000000
	# start_date = 2009-01-01
	# end_date = 2011-12-31
	# symbols = ['SPY', 'XOM', 'GOOG', 'GLD']
	# allocs (fund allocation) = [0.4, 0.4, 0.1, 0.1, ]

#process -- prices df 			-> normed df 			-> allocated df 		-> position_vals 		-> portfolio_vals
#	['SPY', 'XOM', 'GOOG', 'GLD']	['SPY', 'XOM', 'GOOG', 'GLD']	['SPY', 'XOM', 'GOOG', 'GLD']	['SPY', 'XOM', 'GOOG', 'GLD']	[Portfolio]
#	  45	 34	23 	100	  1.0	 1.0	1.0 	1.0  	  0.4	 0.4	0.1 	0.1  	 400000  400000	100000 	100000 	 1000000
#	  40	 39	30 	95  	  0.8	 1.1	1.3 	0.9  	  0.32	 0.44	0.13 	0.09  	 320000	 440000	130000 	90000  	 980000
#	  ...				  ...				  ...				 ...				 ...


#first step is to normalize these prices -- gives a starting point of 1 for all prices
	# price values divided by the first row -- normed = prices / prices[0]
	# this gives the first row all values of 0
	# yields essentially cumulative returns from the start date 
#next step is to multiply these normed values by the allocations to each of the equities
	# allocd = normed * allocs 
	# this gives the first row the values of the allocs
#next step is to multiply the allocated df by the start_val
	# position_val = allocateddf * start_val
	# this gives the first row the amount of cash allocated to each asset
	# the values below the first row show the value of that asset over time
#final step is to calculate the total value for the portfolio each day by summing across each day/row
	# portfolio_val = position_val.sum(axis=1)
	# this gives the total value for the portfolio for each day(aka row) 
	# this yields 1 column
#now that we have the portfolio values we can run important stats on he portfolio and thus assess the portfolio and the portfolio manager's investment style
	# an important first stat calculation is Daily Returns -- first value is always 0 because on first day there is no change -- must exclude this value from any calculations made across all daily returns
		# daily_ret = daily_ret[1:] -- starts at second row excludes first row
	# Calculating Daily Returns always 4 other key stats to be calculated
		# cumulative returns -- measure of how much the value of the portfolio has gone up from the beginning to the end
			# cum_ret = (portfolio_vals[-1] / portfolio_vals[0]) - 1 -- note portfolio_vals[-1] == last value in portfolio_vals
		# average daily returns
			# daily_ret.mean()
		# standard deviation daily returns
			# daily_ret.std()
		# sharpe ratio -- risk adjusted return 
			# -- is a measure for calculating risk-adjusted return(i.e., consider our return in context of risk -- risk usually defined as std or volatility 
			# -- a measure that essentially adjusts our return for that risk 
			# -- it is the average return earned in excess of the risk-free rate per unit of volatility or total risk
			# -- subtracting the risk-free rate from the mean return, the performance associated with risk taking activities can be isolated
			# -- if stock1 and stock2 have equal volatility, stock1 has higher return -- stock1 is better
			# -- if stock1 has higher volatility, stock1 and stock2 have equal return -- stock2 is better
			# -- if stock1 has higher volatility, stock1 has higher return		-- not enough info, need to use sharpe ratio
			# all else being equal -- lower risk aka volatility is better -- higher return is better
			# sharpe ratio also considers risk-free rate of return: the interest rate you would get on your money if you put it in a risk free asset like a bank account or short term treasury
				# used to see if money would be better spent in risk free asset 
				#recently risk-free rate of return == 0; the reason why lately people have been putting money in stock market as opposed to risk free investments
		 	# -- sharpe ratio = (mean portfolio return - risk-free rate) / std of portfolio return
			# -- sharpe ratio = (portfolio return - risk free rate of return) / volatility 
				# as volatility increases, sharpe ratio decreases
				# as portfolio return increases, sharpe ratio increases
				# as risk-free rate of return increases, sharpe ratio decreases -- need to have larger portfolio return than risk-free rate to get a positive sharpe ratio 

			# computing forward looking measure of what Sharpe Ratio should be 
				# s = E[Rp - Rf] / std[Rp - Rf] 
					# E -- expected value -- ex ante
			# computing Sharpe Ratio using historical data
				# s = mean[daily_ret - daily_risk_free_rate] / std[daily_ret - daily_risk_free_rate]
					
			# what is the risk free return rate?
				# LIBOR -- London Inter Bank Offer Rate -- changes each day
				# interest rate on the 3 month Treasury Bill -- changes each day
				# 0%	
				# traditional shortcut -- convert annual amount into daily amount 
					# assume risk free rate is 0.1% per year -- meaning if we start the year at 1.0 at the end of the year we get 1.1 due to 0.1% interest
					# what is the interest rate per day to get to 0.1% -- note 252 stock trading days 
					# daily_risk_free_rate = 252  root 1.0 + 0.1 - 1 -- note 252 root 1.0 + 0.1 - 1

				# note if daily_risk_free_rate is a constant then drop it from denominator
				# s = mean(daily_ret - daily_risk_free_rate) / std(daily_ret)

			# NOTE --
			# Sharpe ratio can vary widely depending on how frequently you sample it 
			# ex. if you sample yearly vs. monthly vs. daily 
			# original vision for Sharpe ratio was that it was an annual measure
			# if sampling at frequencies other than annually -- need to include an adjustment factor, k
			# SRannualize = k * SR
			# k is square root of # of samples per year 
				# if sampling daily, k = square root of 252
				# if sampling weekly, k = square root of 52
				# if samplying monthly, k = square root of 12
				# number being square rooted == rate of sampling -- if we sampled 82 days we still use k = square root of 252 because we are sampling daily, it is the frequency at which we sample
			

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
	df1 = get_data_frame(dates)
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
	daily_ret = daily_returns(port_vals)
	print "Daily Returns:\n", daily_ret
	cum_ret = cumulative_returns(port_vals)
	print "Cumulative Returns:\n", cum_ret
	ave_daily_ret = average_daily_returns(daily_ret)
	print "Average Daily Returns:\n", ave_daily_ret
	std_daily_ret = std_deviation_daily_returns(daily_ret)
	print "Standard Deviation Daily Returns:\n", std_daily_ret
	sharpe = sharpe_ratio(daily_ret, std_daily_ret)
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
	
############### Create Dataframe #################

def get_data_frame(dates):
	tempdf = pd.DataFrame(index=dates)
	for symbol in sys.argv[4:]:
		#check contents of symbol for any number values -- this indicates an allocation and not a symbol
		num_check = False
		for i in range(0, len(symbol)):
			if symbol[i] == '0' or symbol[i] == '1' or symbol[i] == '2' or symbol[i] == '3' or symbol[i] == '4' or symbol[i] == '5' or symbol[i] == '6' or symbol[i] == '7' or symbol[i] == '8' or symbol[i] == '9':
				num_check =True
				break
		if num_check == False:
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
	return tempdf

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

def cumulative_returns(port_vals):
	cum_ret = (port_vals[-1] / port_vals[0]) - 1
	return cum_ret

def average_daily_returns(daily_ret):
	return daily_ret.mean()

def std_deviation_daily_returns(daily_ret):
	return daily_ret.std()

def sharpe_ratio(daily_ret, std_daily_ret):
	sharpe = daily_ret - risk_free_rate
	sharpe = sharpe.mean()
	sharpe = sharpe / std_daily_ret

	return sharpe	




if __name__ == "__main__":
	if len(sys.argv) >= 5:
		port_manager()
	else:
		print "usage: python portfolio.py <start_value> <start_date: yr-month-day> <end_date: yr-month-day> <tickerSymbol> ... <tickerSymbol_n> <fund_allocation: 0.0 - 1.0> ... <fund_allocation_n: 0.0 - 1.0>"























