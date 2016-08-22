import sys
import pandas.io.data as web
from datetime import datetime
import os


def symbol_to_path(symbol, base_dir="./"):
	#return CSV file path given ticker symbol
	return os.path.join(base_dir, "{}.csv".format(str(symbol)))

def retrieve():
	#read in symbol from command line
	#symbol = sys.argv[1] 
	#print "retrieving stock data from " +  sys.argv[1]
	
	
	#dframe = web.DataReader(symbol,  'yahoo', datetime(2000,1,1), datetime(2016,8,21))

	#filename = symbol + ".csv"

	#dframe.to_csv(filename, index_label="Date")


	for symbol in sys.argv[1:]:
		print "Retrieving stock data from " + symbol + " ..."
		dframe = web.DataReader(symbol,  'yahoo', datetime(2000,1,1), datetime(2016,8,21))
		dframe.to_csv(symbol_to_path(symbol), index_label='Date')
		print "file: " + symbol_to_path(symbol) + " created"

if __name__ == "__main__":
        if len(sys.argv) > 1:
                retrieve()
        else:
                print "usage: python retrieveStockData.py <tickerSymbol> ... <tickerSymbol_n-1> <tickerSymbol_n>"

