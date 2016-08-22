import numpy as np
from time import time #timing operations

def test_run():
	#1. create 1 dimensional array from known values
	#numpy has an array function which can convert most array-like objects into an nd array
	#ndarray == n-dimensional array
	#list to 1D array -- this function can take a list, a tuple or a sequence
	print "example 1"
	print np.array([2, 3, 4])
	
	#2. create 2 dimensional array from known values
	#simply pass a sequence of sequences to this function
	#each tuple is enclosed in parenthesis serves as one row in the resulting array
	print "example 2"
	print np.array([(2, 3, 4), (5, 6, 7)])
	
	#note on empty arrays, the values will not be "empty" -- the values will be whatever values were present in the corresponding memory location 

	#3. create empty array with initial values 
	#help avoid growing arrays incrementally -- which can be an expensive operation
	#3a. 1 dimensional array -- a sequence of integers denoting the size in each dimension -- 5 rows 
	print "example 3a -- np.empty(5)"
	print np.empty(5) 

	#3b. 2 dimensional array -- a sequence of 2 integers is needed: the numbers of rows and the number of columns -- 5 rows and 4 columns
	print "example 3b -- np.empty((5,4))"
	print np.empty((5,4))

	#3c. 3 dimensional array or higher -- add n numbers to the array function -- will be n dimensional with n depth
	print "example 3c -- np.empty((5,4,3))"
	print np.empty((5,4,3))

	#4. create an array full of ones 
	print "example 4 -- np.ones((5,4))"
	print np.ones((5,4))

	#5. specify the type int for the value we want in each array location -- dtype is the argument passed to the function
	print "example 5 -- np.ones((5,4), dtype=np.int_)"
	print np.ones((5,4), dtype=np.int_)

	#6. generate random numbers uniformly sampled fp numbers from [0.0, 1.0] -- pass in tuple size 
	print "example 6 -- np.random.random((5,4))"
	print np.random.random((5,4))

	#7. generate random numbers uniformly sampled fp numbers from [0.0, 1.0] -- variant which randomly accepts sequence of numbers as arugment instead of the tuple -- otherwise equal/valid to above #6
	#function arguments not a tuple 
	#numpy provides this function to achieve a greater compatibility with the more established MATLAB syntax
	print "example 7 -- np.random.rand(5,4)"
	print np.random.rand(5,4)

	#8. generate random numbers from a normal distribution -- normal function
	print "example 8 -- np.random.normal(size=(2,3)) #standard normal distribution -> (mean = 0, s.d. = 1)"
	print np.random.normal(size=(2,3))

	#9. generate random numbers from a Gaussian (normal) distribution
	print "example 9 -- np.random.normal(50, 10, size=(2,3))" #change mean to 50 and s.d. to 10
	print np.random.normal(50, 10, size=(2,3))
	
	#10. generate random integers
	#10a. single integer in [0,10]
	print "example 10a -- np.random.randint(10)"
	print np.random.randint(10)	

	#10b. same as 10b specifying [low,high] explicitly
	print "example 10b -- np.random.randint(0, 10)"
	print np.random.randint(0, 10)

	#10c. 5 random integers as a 1D array
	print "example 10c -- np.random.randint(0, 10, size=5)"
	print np.random.randint(0, 10, size=5)

	#10d. 2x3 array of random integers
	print "example 10d -- np.random.randint(0, 10, size=(2,3))"
	print np.random.randint(0, 10, size=(2,3))
	
	#11. get shape of an array
	print "example 11 -- a.shape"
	a = np.random.random((5,4))
	print a
	print a.shape

	#12. get number of rows and number of columns individually
	print "example 12 -- a.shape[0] && a.shape[1]"
	print a.shape[0]
	print a.shape[1]

	#13. get number of dimensions in an array
	print "example 13 -- len(a.shape) -- number of dimensions"
	print len(a.shape)

	#14. get number of elements in an array
	#product of rows and columns but you can also access the data type of each element using dtype argument
	print "example 14a -- a.size -- number of elements in an array"
	print a.size
	print "example 14b -- a.dtype -- data type of elements in array"
	print a.dtype

	#15. math operations
	#seed random generator with constant -- gives same values for the array on different program executions
	np.random.seed(693)
	b = np.random.randint(0, 10, size=(5,4))
	print "Array b:\n", b
	
	#print sum of all elements
	print "Sum of all elements of array b:", b.sum()

	#sum in specific direction (i.e., along rows or columns)
	#axis == 1 -> rows -- iterate over over columns to compute sum of each row
	#axis == 0 -> columns -- iterate over rows to compute sum of each column
	print "sum of each column: ", b.sum(axis=0)
	print "sum of each row: ", b.sum(axis=1)

	#find min, max and mean of an array
	print "minimum of each column: ", b.min(axis=0)
	print "max of each row: ", b.max(axis=1)
	print "mean of all elements: ", b.mean()

	#get index of max value in an array -- locate the max value
	#instead of iterating through an array and keeping track of index of largest value use numpy functions
	#use argmax()
	print "index of max value: ", b.argmax()

	#time operation 
	nd1 = np.random.random((1000, 10000))
	#time the 2 functions and compare execution times

	res_manual, t_manual = how_long(manual_mean, nd1)
	res_numpy, t_numpy = how_long(numpy_mean, nd1)
	#print "Manual: {:.6f} ({:.3f} secs.) vs. NumPy: {:.6f} ({:.3f} secs.)".format(res_manual, res_numpy)
	print "Manual: " + str(res_manual) +  " (" + str(t_manual) + " secs.) vs. NumPy: " + str(res_numpy) + " (" + str(t_numpy) + " secs.)"
	assert abs(res_manual - res_numpy) <= 10e-6, "error: results aren't equal!"
	speedup = t_manual / t_numpy
	print "NumPy mean is ", speedup, "times faster than manual for loops."
	
	#accessing array elements
	c = np.random.rand(5,4)
	print "Array c:\n", c
	element = c[3,2]
	print "element c[3,2]: ", element

	#access elements in ranges
	print "element in range c[0, 1:3] -- get elements in row 0, columns 1 through 2"
	print c[0, 1:3]

	print "element in range c[0:2, 0:2] -- get elements in rows 0 through 1, columns 0 through 1"
	print c[0:2, 0:2]

	#slice n:m:t specifies a range that starts at n, and stops before m in steps of size t
	print "slice n:m:t specifies a range that starts at n, and stops before m in steps of size t"
	print "select columns 0, 2 for every row -- c[:, 0:3:2] -- gives values of column 0, skip values of column 1, and then give values in column 2"
	print c[:, 0:3:2]

	#modifying array element values
	d = np.random.rand(5,4)
	print "Array d:\n", d
	
	#assigning a value to a particular location
	d[0,0] = 1
	print "Modified Array d(replaced one element): -- row 0 column 0\n", d
	
	#assigning value to a whole row
	d[0, :] = 2
	print "Modified Array d(replaced a row with a single value 2): -- every column in row 0\n", d

	#assigning a list to a column in an array
	d[:, 3] = [1, 2, 3, 4, 5]
	print "Modified Array d(replaced a column with a list of values): -- every row in column 3\n", d

	#indexing an array with another array
	e = np.random.rand(5)
	print "Array e:\n", e
	#accessing using list of indices -- we want value at index 1, again at 1, index 2, followed by index 3
	indices = np.array([1, 1, 2, 3])
	print "access using list of indices: [1,1,2,3]", e[indices]
	
	#indexing arrays using boolean or mask index
	f = np.array([(20,25,10,23,26,32,10,5,0), (0,2,50,20,0,1,28,5,0)])
	print "Array f:\n", f	
	#example find all values that are less than the mean of the entire array
	mean = f.mean()
	print "Mean of f: ", mean
	#instead of iterating through loop and finding all indices where the values are less than the mean, we use a NumPy function for speed
	print "mask indexing of Array f: f[f<mean] = ", f[f<mean]
	
	#reassign mask indices with mean
	f[f<mean] = mean
	print "replacing mask indices with mean value: f[f<mean} = mean \n", f
	

	#arithmetic operations on arrays -- new arrays are created with each operation -- array and divisors are integers so concatenation will occur unless using fp values
	g = np.array([(1,2,3,4,5), (10,20,30,40,50)])
	print "Array g:\n", g
	#multiply this whole array by 2
	print "Multiply Array g by 2: \n", 2 * g

	#arithmetic operations using 2 arrays
	h = np.array([(100,200,300,400,500), (1,2,3,4,5)])
	print "Array h:\n", h
	
	#add the 2 arrays g + h
	print "Added Array h + Array g:\n", h+g

	#muliplying 2 arrays will not give you metric prodcut, but will do element wise multiplication
	#i.e., element h[0,0] is multiplied by g[0,0] only, h[0,1] is multiplied by g[0,1] only, etc.
	print "Multiplying (element-wise by default) Array h * Array g:\n", h*g

	
def manual_mean(arr):
	#manual computation of sum of all elements in given 2d array
	sum = 0
	for i in xrange(0, arr.shape[0]):
		for j in xrange(0, arr.shape[1]):
			sum = sum + arr[i, j]
	return sum/arr.size

def numpy_mean(arr):
	return arr.mean()

def how_long(func, *args):
	t0 = time()
	result = func(*args)
	t1 = time()
	return result, t1 - t0


if __name__ == "__main__":
	test_run()
