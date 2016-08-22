import pandas as pd

def get_max_close(symbol):
	#return max closing value for stock indicated by symbol
	#note data for a stock is stored in file: ./<symbol>.csv

	dframe = pd.read_csv("./{}.csv".format(symbol))
	return dframe['Close'].max()

def test_run():
	for symbol in ['GOOG', 'IBM']:
		print "Max close" 
		print symbol, get_max_close(symbol)


if __name__ == "__main__":
	test_run()
