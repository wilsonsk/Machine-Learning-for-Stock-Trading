import pandas as pd

def test_run():
	df = pd.read_csv("data/AAPL.csv");
	print df #print entire dataframe
	#print df.head() -- print first 5 rows
	#print df.tail() -- print last 5 rows
	#print df.tail(n) -- print last n rows

if __name__ == "__main__":
	test_run()
