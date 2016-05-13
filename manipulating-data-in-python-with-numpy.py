import numpy as np

# create and print a few arrays
zeroArray = np.zeros((2,3))
onesArray = np.ones((2,3))
randomArray = np.random.random((2,3))

print zeroArray
print onesArray
print randomArray

# print value using array index
print randomArray[1,1]

# create and print range array
rangeArray = np.arange(6,12)
print rangeArray

# reshaping arrays
rangeArray = rangeArray.reshape((3,2))
print rangeArray

# slicing values in square array
squareArray = np.arange(1,10).reshape((3,3))
print squareArray

print squareArray[0,0:2] # 1 2
print squareArray[0,1:2] # 2
print squareArray[1:3,1:3] # lower corner
print squareArray[:,1:3] # column 2 and 3

# create a random row and print by array indexes
randomRow = np.random.random((10,1))
print randomRow

fibIndices = np.array([1,1,2,3])
print fibIndices # 1 1 2 3

print randomRow[fibIndices]

# print values in squareArray by array indexes
boolIndices = np.array([[True,False,True],
						[False,True,False],
						[True,False,True]])
print boolIndices
print squareArray[boolIndices] # 1 3 5 7 9

# using numpy operations
print np.average(squareArray) 			# 5
print np.median(squareArray) 			# 5
print np.sum(squareArray) 				# 45
print np.sum(squareArray[:,0]) 			# 12

# find values in squareArray that are better then average
sqAverage = np.average(squareArray)
betterThanAverage = squareArray > sqAverage

print squareArray # reference
print betterThanAverage

# standard deviation
sqStdDev = np.std(squareArray)
print sqStdDev # 2.5819...

# copy and manipulate arrays
fred = squareArray.copy()
fred[1,1] = 0
print squareArray # reference
print fred

# conditional assignment of values in copy of array
clampedSqArray = np.array(squareArray.copy(), dtype=float)
clampedSqArray[(squareArray - sqAverage) > sqStdDev] = sqAverage + sqStdDev
print clampedSqArray

clampedSqArray[(squareArray - sqAverage) < -sqStdDev] = sqAverage - sqStdDev
print clampedSqArray

# other operations
print squareArray * 2
print squareArray / 2
print squareArray + np.ones((3,3))
print squareArray + 1
print squareArray * np.arange(1,10).reshape((3,3))

# matrix multiplication
matA = np.array( [[1,2],[3,4]] )
matB = np.array( [[5,6],[7,8]] )

print matA # reference
print matB # reference
print np.dot(matA,matB)
