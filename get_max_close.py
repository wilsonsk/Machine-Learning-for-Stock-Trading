import pandas as pd
import matplotlib.pyplot as plt

def get_max_close(symbol):
	#return max closing value for stock indicated by symbol
	#note data for a stock is stored in file: ./<symbol>.csv

	dframe = pd.read_csv("./{}.csv".format(symbol))
	return dframe[['Date', 'Close']].max()

def test_run():
	for symbol in ['GOOG', 'IBM']:
		print "Max Close" 
		print symbol, get_max_close(symbol)


if __name__ == "__main__":
	test_run()
