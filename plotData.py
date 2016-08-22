import pandas as pd
import matplotlib.pyplot as plt
import sys

file = sys.argv[1]

def test_run():
	dframe = pd.read_csv("./" + file)
	print dframe[['Close', 'Adj Close']]
	dframe[['Close', 'Adj Close']].plot()
	plt.show()


if __name__ == "__main__":
        test_run()
