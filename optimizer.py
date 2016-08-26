#Optimizer: 
	# Purpose:
		# find minimum values of functions -- f(x) = x^2 + x^3 + 5 finds what value of x is this overall function minimized -- finds value of x input that yields lowest function value (usually called y)
		# build parameterized models based on data -- find parameters for parameterized models from data  -- ex: f(x) = mx + b
		# refine allocations to stocks in portfolios -- decide what percentage of funds should be allocated to each stock
	# How to use:
		# 1. Provide a function to minimize -- python calls function with many different values of input until function overall is determined smallest
		# 2. Provide an initial guess -- input guess that might be close to solution (finding minimum function)
		# 3. Call the optimizer -- with above parameters
	# How it works:
		# checks function value with initial guess input
		# tests an input value slightly above initial guess and tests an input value slightly below initial guess
		# finds slope of the equation of the newly varied guess
		# performs a gradient desent (goes downhill due to minimizing action) 
		# tests another input value down along that slope 
		# test an input value slightly below the above input, tests an input value slightly above the previous input
		# repeat

	# Convex Problems:
		# convex function: if the line segment between any two points on the graph of the function  lies above or on the graph, in a Euclidean space of at least two dimensions.
			# 1. choose two points, draw a line
			# 2. convex if: line is above the graph


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as spo

############### EXAMPLE Function to be minimized by the optimizer ###################
# MINIMIZER FINDS X THAT YIELDS LOWEST VALUE OF FUNCTION
def f(X):
	# Given a scalar X, return some value (a real number) 
	Y = (X - 1.5)**2 + 0.5 	#**2 means squared
	print "X = {}, Y = {}".format(X, Y)
	return Y


############### Optimizer Call ####################

def optimize_f():
	initial_Xguess = 2.0
	#arguments descriptions: 
		# f -- function f(X) 
		# initial_Xguess -- our initial guess input that might be close to solution
		# method='SLSQP' -- directing minimizer to use a particular minimizing algorithm called, 'SLSQP'
		# options={'disp': True} -- verbose option
	min_result = spo.minimize(f, initial_Xguess, method='SLSQP', options={'disp': True}) 
	print "Minima found at:"
	print "X = {}, Y = {}".format(min_result.x, min_result.fun)

	#plot function values, mark minima
	Xplot = np.linspace(0.5, 2.5, 21)
	Yplot = f(Xplot)
	plt.plot(Xplot, Yplot)
	plt.plot(min_result.x, min_result.fun, 'ro')
	plt.title("Minima of an objective function")
	plt.show()

############### Building a parameterized model from data ####################
# MINIMIZER FINDS PARAMETERS THE YIELD LINE WITH BEST FIT WITH DATA POINTS 
# example: f(x) = mx + b -- line equation
	# 2 parameters: m and b -- m == slope & b == y-intercept
	# goal: discover equation of the line that best fits a set of data points
	# what are we minimizing?
		# evaluate a candidate line using the that line's line equation with m and b parameters
		# minimizer is going to vary the parameter values (m, b) to try and minimize something (i.e., some equation that gets lower in value) 
			# therefore, we need an equation that gets lower in value as the line better fits the data points
				# what should we use for that equation?
					# 1. distances of each point from the line under question
						# e_sub_i == each point's distance from the line under question (with coefficient i)
							# sum of all points starting where each e_sub_i is squared to oppose any negative values 
								# using the error point sums of lines under question, the minimizer will test other parameters (m,b) until it finds "best" solution line with 
								# tested parameters
							# 1. we express problem for minimizer as a minimalization problem via error point sums of a line under question
							# 2. we give it the equation to minimize as the error (aka the sum of all the data point's distances from the line under question)
							# 3. the minimizer finds the value for the coefficients (aka parameters m,b) that yield the line with least error via equation in step 2

def errorEquation(line, data):
	# this is the equation that is given to the minimizer so that it can find the parameters that yield line with best fit with data points
	# this equation computes the error between a given line (line under question) and observered data points 
	"""
	Parameters	
	----------	
	line: tuple/list/array (m, b) where m is slope and b is y-intercept -- these are the parameters to be found by the minimizer
	data: 2D array where each row is a point (x, y) 
	error: sum of each data points distance from the line under question; each distance is squared to prevent negative values	

	Returns error as a single real value 
	"""

	# metric: sum of squared y-axis differences
	# err = sum of some point - (m(x-val at that same point) + b)^2
	# data[:, 1] == value of actual data (x,y) at each point
	# (line[0] * data[:,0] + line[1]) == estimate of the line under question would give at that same point 
	err = np.sum((data[:, 1] - (line[0] * data[:, 0] + line[1])) **2)
	return err

def fit_line(data, err_func):
	""" Fit a line to given data points, using a supplied error function

	Parameters
	----------
	data: 2d array where each row is a point (x,y)
	err_func: function that computes the error between a line and observered data points

	Returns line that minimizes the error function 
	"""
	# generate initial guess for line model (line to question)
	l = np.float32([0, np.mean(data[:, 1])]) # slope = 0 ; y-intercept = mean(y values) -- this is just a line through a y-intercept with no slope

	# plot initial guess (optional)
	x_ends = np.float32([-5, 5])
	plt.plot(x_ends, l[0] * x_ends + l[1], 'm--', linewidth=2.0, label="Initial Guess")

	# call optimizer --  build parameters from data
	result = optimize_line(err_func, data, l)
	
	return result

def optimize_line(err_func, data, line):
	# call optimizer --  build parameters from data
	#arguments descriptions: 
		# err_func -- error function to be minimized 
		# data -- observed data points -- created by generating noisy data points
		# line -- our initial guess for line model (aka line to be questioned)
		# method='SLSQP' -- directing minimizer to use a particular minimizing algorithm called, 'SLSQP'
		# options={'disp': True} -- verbose option
	result = spo.minimize(err_func, line, args=(data,), method='SLSQP', options={'disp': True})
	return result.x

def build_parameters():
	# define original line for comparison to minimizer's line
	l_orig = np.float32([4, 2]) -- minimizer doesn't know this to test minimizer (for discovery of equation of line)
	print "Original line: m = {}, b = {}".format(l_orig[0], l_orig[1])
	# generate x and y values keeping in mind that the minimizer doesn't know these
	x_orig = np.linspace(0, 10, 21)
	y_orig = l_orig[0] * x_orig + l_orig[1]	# y = mx + b of original line
	plt.plot(x_orig, y_orig, 'b--', linewidth=2.0, label="Original Line")

	# generate noisy data points -- that fit around original line with a std deviation of 3.0 and will be used by minimizer to find a line of best fit around these points
	noise_sigma = 3.0 	# sigma = std deviation
	noise = np.random.normal(0, noise_sigma, y_orig.shape)
	data = np.asarray([x_orig, y_orig + noise]).T	-- for each point along the x axis where we have data we add some noise
	plt.plot(data[:, 0], data[:, 1], 'go', label="Data Points")
 
	# call optimizer --  build parameters from data
	l_fit = fit_line(data, errorEquation)
	print "Fitted line: m = {}, b = {}".format(l_fit[0], l_fit[1])
	plt.plot(data[:, 0], l_fit[0] * data[:, 0] + l_fit[1], 'r--', linewidth=2.0, label="Optimized Fit")

	# create legend and plot
	plt.legend(loc='upper left')
	plt.show()









if __name__ == "__main__":
	optimize_f()
	build_parameters()














