/* 
* Skyler Wilson
* project description:
*	implement machine learning based strategies to make trading decisions using real-world data 
*/

program run sequence:
	1. run retrieveStockData <tickerSymbol> first to obtain stock data from yahoo and output it to a .csv file
	2a. run individual stock program with correct usage -- use stock symbols of any of the .csv files as input
	2b. run portfolio manager program with correct usage -- use stock symbols of any of the .csv files as input
