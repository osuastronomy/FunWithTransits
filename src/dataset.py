r""" 
This file generates the mock data set for the transit object. 
""" 

from .transit import transit 
import random 


class dataset(transit): 

	def __init__(self, seed = 2, npoints = 1000, sigma = 0.001): 
		super().__init__(0.01423, 9582, 11893, 23806, 26097) 
		random.seed(a = seed) 
		self._data = npoints * [None] 
		self._sigma = sigma 
		for i in range(npoints): 
			x = 36000 * random.random() 
			y = super().__call__(x) + random.gauss(0, sigma) 
			self._data[i] = [x, y] 

	def show(self, ax): 
		r""" 
		Plot the data set on a set of matplotlib axes passed from the transit 
		object. 
		""" 
		ax.scatter([i[0] for i in self._data], [i[1] for i in self._data], 
			s = 5, c = 'k') 

	def chi_squared(self, model): 
		chi_squared = 0 
		for i in self._data: 
			chi_squared += (i[1] - model(i[0]))**2 / self._sigma**2 
		return chi_squared / (len(self._data) - 5) 
		# return chi_squared 

