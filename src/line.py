r""" 
This file implements the line object. The transit object uses composition with 
this class, storing 5 instances under the hood to represent the light curve. 
""" 

import numbers 

class line: 

	r""" 
	A line on an arbitary x-y axis. 

	Parameters & Attributes 
	-----------------------
	slope : real number 
		The slope of the line in arbitrary units. 
	intercept : real number 
		The y-intercept in arbitrary units. 

	Calling 
	-------
	This object can be called with the x-coordinate only to determine the 
	value of the y-coordinate which lies on the line defined by the slope and 
	the intercept. 
	""" 

	def __init__(self, slope, intercept): 
		self.slope = slope 
		self.intercept = intercept 


	def __call__(self, x): 
		return self.slope * x + self.intercept 


	@classmethod 
	def from_points(cls, pt1, pt2): 
		r""" 
		Obtain a line object from two points on an x-y axis. 

		Parameters 
		----------
		pt1 : list 
			A 2-element list containing the (x, y) coordinates of one of the 
			two points to define the line. 
		pt2 : list 
			A 2-element list containing the (x, y) coordinates of the second 
			pointing defining the line. 

		Returns 
		-------
		l : line 
			The line object defined by the points ``pt1`` and ``pt2``. 

		Raises 
		------
		* TypeError	
			- Either pt1 or pt2 are not of type ``list`` 
			- Either pt1 or pt2 are not of length 2 
			- Either pt1 or pt2 contain non-numerical data. 
		""" 
		if isinstance(pt1, list) and isinstance(pt2, list): 
			if len(pt1) == 2 and len(pt2) == 2: 
				if (all([isinstance(i, numbers.Number) for i in pt1]) and 
					all([isinstance(i, numbers.Number) for i in pt2])): 
					# both parameters are length-2 lists containing numbers 
					slope = (pt2[1] - pt1[1]) / (pt2[0] - pt1[0]) 
					intercept = pt1[1] - pt1[0] * slope 
					return cls(slope, intercept) 
				else: 
					raise TypeError("Non-numerical value detected.") 
			else: 
				raise TypeError("Data must be 2-dimensional.") 
		else: 
			raise TypeError("Points must be of type list. Got: %s, %s" % (
				type(pt1), type(pt2))) 


	@property 
	def slope(self): 
		r""" 
		Type : float 

		The slope of the line, in arbitrary units. 
		""" 
		return self._slope 


	@slope.setter 
	def slope(self, value): 
		if isinstance(value, numbers.Number): 
			self._slope = float(value) 
		else: 
			raise TypeError("Slope must be a real number. Got: %s" % (
				type(value))) 


	@property 
	def intercept(self): 
		r""" 
		Type : float 

		The y-intercept of the line, in arbitrary units. 
		""" 
		return self._intercept 


	@intercept.setter 
	def intercept(self, value): 
		if isinstance(value, numbers.Number): 
			self._intercept = float(value) 
		else: 
			raise TypeError("Intercept must be a real number. Got: %s" % (
				type(value))) 

