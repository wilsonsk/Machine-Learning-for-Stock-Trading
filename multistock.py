import pandas as pd
import sys
import os

def symbol_to_path(symbol, base_dir="./"):
	#return CSV file path given ticker symbol
	return os.path.join(base_dir, "{}.csv".format(str(symbol)))

def test_run():
	start_date = '2016-08-01'
	end_date = '2016-08-21'
	dates = pd.date_range(start_date, end_date)
	#file = "./" + sys.argv[1]
	#create empty dataframe with dates within the above range
	df1 = pd.DataFrame(index=dates)

	for symbol in sys.argv[1:]:
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

	print df1

if __name__ == "__main__":
	test_run()
