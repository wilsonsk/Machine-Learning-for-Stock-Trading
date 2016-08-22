import sys
import pandas.io.data as web
from datetime import datetime


#read in symbol from command line
symbol = sys.argv[1] 
print "retrieving stock data from " +  sys.argv[1]


dframe = web.DataReader(symbol,  'yahoo', datetime(2000,1,1), datetime(2012,1,1))

filename = symbol + ".csv"

dframe.to_csv(filename, index_label="Date")
