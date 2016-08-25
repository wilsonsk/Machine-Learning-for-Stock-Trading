import pandas as pd
import sys
import os
import matplotlib.pyplot as plt
import numpy as np

#note -- slicing -- last value is 1 past the value you actually want to include: [1:3] -> 1 to 2 
#colon by itself indicates all of either a row or column: [:, 3] -> all rows in 3rd column (note rule above does not apply here) -- [3:] all beyond 3
#last row indicated by -1, 2nd to last row is -2: [-1, 1:3] -> last row with columns 1 to 2 

def symbol_to_path(symbol, base_dir="./csv_files"):
	#return CSV file path given ticker symbol
	return os.path.join(base_dir, "{}.csv".format(str(symbol)))

def join_and_slice():
	start_date = str(sys.argv[1])
	end_date = str(sys.argv[2])
	df1_start_date = '2000-01-01'
	df1_end_date = '2016-08-22'
	dates = pd.date_range(df1_start_date, df1_end_date)
	#file = "./" + sys.argv[1]
	#create empty dataframe with dates within the above range
	df1 = pd.DataFrame(index=dates)

	#slice argv from index 3 to as many args exist
	for symbol in sys.argv[3:]:
		#index_col used because df1 uses date index, whereas dfCsvFile uses standard integer index; need to index dfCsvFile by date to match df1 
		#convert dates present in dfCsvFile to datetime objects via parse_dates=True 
		#usecols used for specifying desired columns, Date and Adj Close 
		#Weekend dates use Nan values because stocks where not traded during weekend, but csv NaN is a string, must be interpretted as a number via na_values=['nan']

		dfCsvFile = pd.read_csv(symbol_to_path(symbol), index_col='Date', parse_dates=True, usecols=['Date', 'Adj Close'], na_values=['nan'])

		#prevent clashing column names by renaming column names with each symbol
		dfCsvFile = dfCsvFile.rename(columns={'Adj Close': symbol})	

		#left join by default: all df1 rows, joined with only dfCsvFile rows that match with df1
		#df1 = df1.join(dfCsvFile)

		#drop NaN values
		#df1 = df1.dropna()
	
		#the 2 previous steps can be accomplished in 1 step via the 'how' argument in join function set to inner
		#i.e., instead of using a left join which takes all values of 1 and only values of b that match a and then dropping values of a that have no b matches
		#use inner join because this is what we are trying to accomplish with the above modified left join and drop functions
		
		df1 = df1.join(dfCsvFile, how='inner')

	#print df1

	#testing row slicing -- must be in chronological order -- you can remove ix function but .ix is more pythonic and robust
	df2 = df1.ix[start_date : end_date]
	print df2
		
	#testing column slicing
	# -- a single label selects a single column
	# -- a list of labels selects multiple columns
	#print df1[str(sys.argv[1])]


	#testing slicing through both dimensions
	#print df1.ix['2016-08-01' : '2016-08-22', [str(sys.argv[1]), str(sys.argv[2])]]
		
	plot(normalize(df2))
	global_stats(df2)
	

def normalize(dframe):
	#normalize stock prices using the first row of the dataframe
	#normalize data so that all prices start at $1
	# this helps us see movement (up or down) compared to the others
	return dframe/dframe.ix[0, :]


def plot(dframe):
	#name plot via title parameter
	ptitle = "Sample Plot"
	#output of dframe.plot is a handler/object; assign this returned object to a variable called axis
	axis = dframe.plot(title=ptitle, fontsize=2)
	#x and y axis titles via handler which the dataframe generates
	axis.set_xlabel("Date")
	axis.set_ylabel("Adj Close Price")
	plt.show()

def global_stats(dframe):
	#at least 33 global stats
		
	print "Mean Adj Close Price:\n", dframe.mean()
	print "Median Adj Close Price:\n", dframe.median()
	print "Std. Deviation Adj Close Price(measure of deviation from central value; high value means price has varied a lot over time):\n", dframe.std()

	#rolling mean: mean from a range(aka a window of prices) -- lags behind actual price aka rolling -- simple moving average -- look at where the price crosses through the rolling average
	#hypothesis -- rolling mean may be a good representation of sort of the true underlying price of a stock, and that significant deviations from that, eventually result in a return to the mean 
	#might indicate a good buying low opportunity
	#the challenge is to know when is that deviation significant enough to that you should pay attention
	#high deviation may also indicate a sell signal/opportunity 

	#assuming we're using a rolling mean and tracking the price, and we are looking for an opportunity to find when the prices diverged significantly far from the rolling mean that might be an opportunity
	#for a buy or sell signal -- how can we decide that we're far enough away from the mean that we should consider buying or selling? -- which statistic might we use to discover this?
		#use rolling standard deviation to discover an opportunity to sell or buy
	#how can we know if a deviation from the rolling mean is significant enough to warrant a trading signal? we need some way of measuring that
	#John Bollinger -- Bollinger bands (trademark) -- Bollinger observed that we ought to take a look at the recent volatility of the stock
		# if it's very volatile we might discard movements above and below the mean 
		# if it's not very volatile a similarly sized movement may be we should pay attention to
	#Bollinger bands (trademark) -- add a band 2 std deviations above rolling mean, and a band 2 std devations below rolling average
		# the theory is that when you see excursions up to 2 sigma (aka 2 std deviations) away from the mean, you should pay attention
		# in particular, if prices drop below or above 2 sigma and then back through it, that is potentially a buy or sell signal 
			# because the hypothesis is that we've gone quite far from the simple moving average and we are now moving back towards it
	
		
	for symbol in dframe[0:]:
		axis = dframe[symbol].plot(title=symbol, label=symbol)
		rolling_mean = get_rolling_mean(dframe[symbol], windowSize=20)	
		rolling_std = get_rolling_std(dframe[symbol], windowSize=20)
		upper_band, lower_band = get_bollinger_bands(rolling_mean, rolling_std)
	
		rolling_mean.plot(label="Rolling Mean", ax=axis)
		#no need to plot rolling_std; it is just used to calculate Bollinger bands
		#rolling_std.plot(label="Rolling STD", ax=axis)
		upper_band.plot(label="upper band", ax=axis)
		lower_band.plot(label="lower band", ax=axis)	

		axis.set_xlabel("Date")
		axis.set_ylabel("Adj Close Price")
		axis.legend(loc='upper left')
		plt.show()
		

	#Daily Returns: are one of the most important stats used in financial analysis -- most informative when in daily returns are compared amongst different stocks
		# are simply how much did the price go up or down on a particular day
		# calculated : daily_ret[today] = (price[today] / price[yesterday]) - 1
		# do not iterate through days for each daily return -- too slow
		# use NumPy functions
	axis = dframe.plot(title="Daily Returns", label="Stock Prices")
	daily_ret = get_daily_returns(dframe)
	daily_ret.plot(label="Adj Close Prices", ax=axis)
	axis.set_xlabel("Date")
	axis.set_ylabel("Daily Returns")
	axis.legend(loc='upper left')
	plt.show()

	#Daily Returns -- histogram: typically looks like a Gaussian or normal distribution (bell curve)
		# can run a lot of stats on histogram of daily returns
			# mean, std, Kurtosis
			# Kurtosis: meaning curve or arching: tells us about the tails of the distribution
				# assuming a normal/Gaussian distribution: the measure of Kurtosis tells how much different our histogram is from that traditional Gaussian distribution
				# fat tails: in relation to Gaussian, there are more frequent large excursions (more occurences on tails) -- measurement of Kurtosis would be a positive number 
				# skinny tails: many fewer occurences out on the tails in relation to Gaussian distribution -- measurement of Kurtosis would be a negative number
	#plotting histogram
	for symbol in dframe[0:]:
		daily_ret_hist = get_daily_returns_histogram(dframe[symbol])
		daily_ret = get_daily_returns(dframe)
		mean = daily_ret[symbol].mean()
		print "mean of Daily Returns for ", symbol, ": " , mean
		std = daily_ret[symbol].std()
		print "std of Daily Returns for ", symbol, ": ", std
		#plt.axvline(mean,color='w', linestyle='dashed', linewidth=2)
		#plt.axvline(std,color='r', linestyle='dashed', linewidth=2)
		#plt.axvline(-std,color='r', linestyle='dashed', linewidth=2)
		plt.show()

		#compute Kurtosis
		kurtosis = get_kurtosis(daily_ret[symbol])
		print "Kurtosis of Daily Returns for ", symbol, ": " , kurtosis
	
	#plotting 2 histograms together
	daily_ret_hist = get_daily_returns_histogram(dframe)
	plt.show()

	#compute and plot 2 histograms on same chart
	daily_ret = get_daily_returns(dframe)
	for symbol in dframe[0:]:
		daily_ret[symbol].hist(bins=20, label=symbol)
	plt.legend(loc='upper right')
	plt.show()
	
	#cumulative returns: the aggregate amount an investment has gained or lost over time, independent of the period of time involved -- represented as a percentage
		# cum_ret[today] = (price{today] / price[at beginning]) - 1 -- exactly the normalize equation

	#scatter plots: number of individual points/dots; each point represents something that happened on a particular day -- if 2 stocks vs each other on a particular day 
		# stockA has daily return of 1 and stockB has daily return of -1 then 1 point represents this
	#slope: take set of data and fit a line through it using linear regression and to look at the stats of that linear fit
	#one property is slope: usually referred to as beta -- shows how reactive the stock is to the market
		# if beta(slope) is 1 then on average when the market goes up 1% that particular stock also goes up 1%
		# if beta(slope) is 2 then if market goes up to 1% we'd expect on average that the stock would go up 2%
	#alpha: where the slope intercepts the verticle axis -- means if alpha is positive: that this stock is actually on average performing a little bit better than the other stock everyday
		# if alpha negative: on average this stock is returning a little bit less than the other stock everyday
		# shows how well a stock performs with respect to other stock

	#slope != correlation
	#correlation is a measure of how tightly do these individual points fit that line -- 0 to 1 -- how close points are to the line
		# 0 means data not correlated at all
		# 1 means data is very highly correlated
		# could have a shallow slope but the data tightly fitting that line, and thus a higher correlation
		# could have a steeper line and the data fitting that line at a higher correlation
	build_scatter_plot(dframe)
	corr = get_correlation(dframe)
	print "Correlation:\n", corr
	

def get_correlation(dframe):
	daily_ret = get_daily_returns(dframe)
	return daily_ret.corr(method='pearson')

def build_scatter_plot(dframe):
	#build scatter plot: stock1 vs. stock2
	daily_ret = get_daily_returns(dframe)
	symbols = []
	for symbol in dframe[0:]:
		symbols.append(symbol)
	daily_ret.plot(kind='scatter', x=symbols[0], y=symbols[1]) 
	#use ployfit() which needs x-coords and y-coords to fit a line -- y-coords are daily return values 
	#polyfit() returns first the polynomial coefficient (beta) and second the y intercept (alpha) -- in the form y = mx + b -- m is coefficient and b is intercept
	#the idea for plotting is for every value of x we find a value of y using the line equation y = mx +b
	beta_stock1, alpha_stock1 = np.polyfit(daily_ret[symbols[1]], daily_ret[symbols[0]], 1)
	beta_stock2, alpha_stock2 = np.polyfit(daily_ret[symbols[0]], daily_ret[symbols[1]], 1)

	print "beta of ", symbols[0], "= ", beta_stock1
	print "alpha of ", symbols[0], "= ", alpha_stock1	
	print "beta of ", symbols[1], "= ", beta_stock2
	print "alpha of ", symbols[1], "= ", alpha_stock2

	plt.plot(daily_ret[symbols[0]], beta_stock2 * daily_ret[symbols[0]] + alpha_stock2, '-', color='r')
	plt.show()	

def get_kurtosis(daily_returns):
	return daily_returns.kurtosis()

def ffill_missing_data(dframe):
	#do not interpolate data, but do not leave NaN blank either
	#use fill forward: use last known data value until known data -- do not peek into future
	#missing data at the beginning: use fill backwards
	#1. use fill fowards
	#2. use fill backwards
		# using this order of filling prevents peeking into the future
	#pandas fillna() does this 
	dframe.fillna(method="ffill", inplace="TRUE") # -- does fill forwards	
	#dframe.fillna(method="bfill", inplace="TRUE") # -- does fill backwards

def bfill_missing_data(dframe):
	dframe.fillna(method="bfill", inplace="TRUE") # -- does fill backwards
	
def get_rolling_mean(df_values, windowSize):
	return pd.rolling_mean(df_values, windowSize)	

def get_rolling_std(df_values, windowSize):
	return pd.rolling_std(df_values, windowSize)

def get_bollinger_bands(rolling_mean, rolling_std):
	upper_band = rolling_mean + rolling_std * 2
	lower_band = rolling_mean - rolling_std * 2
	return upper_band, lower_band

def get_daily_returns(dframe):
	#first make a copy of the dataframe where we can save computed values
	daily_ret = dframe.copy()
	#this operation cannot be done at index = 0 because we do not have the price of the stock of the day before index 0 -- we set the values at row 0 to all 0's because 0th row now contains all NaN's
	#.values -- allows access to the underlying NumPy array -- this is necessary because when given 2 dataframes, Pandas will try to match each row based on index when performing element wise arithmetic ops
		# so all our efforts in shifting the values by 1 wuill be lost if we do not use the .values attribute 
	#daily_ret[1:] = (dframe[1:] / dframe[:-1].values) - 1
	#set daily returns for row 0 to 0  via row slicing
	
	#statment below is a Pandas alternative to above statements -- much easier -- note Pandas still leaves the 0th row full of NaN's
	daily_ret = (dframe / dframe.shift(1)) - 1
	daily_ret.ix[0, :] = 0
	return daily_ret

def get_daily_returns_histogram(dframe):
	#default bin number = 10
	#change bin number via bin arg
	return dframe.hist(bins=20)

def get_cumulative_return(dframe):
	cum_ret = dframe.copy()
	cum_ret = dframe.cumprod()
	return cum_ret

if __name__ == "__main__":
	if len(sys.argv) > 3:
		join_and_slice()
	else:
		print "usage: python multistock.py <start_date: yr-month-day> <end_date: yr-month-day> <tickerSymbol> ... <tickerSymbol_n-1> <tickerSymbol_n>"
