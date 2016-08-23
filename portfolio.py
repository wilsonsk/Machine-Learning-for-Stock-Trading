#daily portfolio value:
	# start_val = 1000000
	# start_date = 2009-01-01
	# end_date = 2011-12-31
	# symbols = ['SPY', 'XOM', 'GOOG', 'GLD']
	# allocs (fund allocation) = [0.4, 0.4, 0.1, 0.1, ]

#process -- prices df 			-> normed df 			-> allocated df 		-> position_vals 		-> portfolio_vals
	['SPY', 'XOM', 'GOOG', 'GLD']	['SPY', 'XOM', 'GOOG', 'GLD']	['SPY', 'XOM', 'GOOG', 'GLD']	['SPY', 'XOM', 'GOOG', 'GLD']	[Portfolio]
	  45	 34	23 	100	  1.0	 1.0	1.0 	1.0  	  0.4	 0.4	0.1 	0.1  	 400000  400000	100000 	100000 	 1000000
	  40	 39	30 	95  	  0.8	 1.1	1.3 	0.9  	  0.32	 0.44	0.13 	0.09  	 320000	 440000	130000 	90000  	 980000
	  ...				  ...				  ...				 ...				 ...


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
		# cumulative returns 
			# cum_ret = (portfolio_vals[-1] / portfolio_vals[0]) - 1 -- note portfolio_vals[-1] == last value in portfolio_vals
		# average daily returns
			# daily_ret.mean()
		# standard deviation daily returns
			# daily_ret.std()
		# sharpe ratio -- is a measure for calculating risk-adjusted return(i.e., consider our return in context of risk -- risk usually defined as std or volatility 
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
			



























