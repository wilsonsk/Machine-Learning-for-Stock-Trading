import pandas as pd
import sys

def test_run():
	start_date = '2016-08-01'
	end_date = '2016-08-21'
	dates = pd.date_range(start_date, end_date)
	file = "./" + sys.argv[1]

	#create empty dataframe with dates within the above range
	df1 = pd.DataFrame(index=dates)
	
	dfCsvFile = pd.read_csv(file, index_col='Date', parse_dates=True, usecols=['Date', 'Adj Close'], na_values=['nan'])

	df1 = df1.join(dfCsvFile)

	#drop NaN values
	df1 = df1.dropna()

	print df1

if __name__ == "__main__":
	test_run()
