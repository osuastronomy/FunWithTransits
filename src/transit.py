r""" 
This file implements the transit light-curve object. 
""" 

from .line import line 
import numbers 
try: 
	ModuleNotFoundError 
except NameError: 
	ModuleNotFoundError = ImportError 
try: 
	import matplotlib as mpl 
except (ModuleNotFoundError, ImportError): 
	raise ModuleNotFoundError("Matplotlib required.") 
import matplotlib.pyplot as plt 

# matplotlib presets that make the graphs look not hideous 
mpl.rcParams["font.family"] = "serif"
mpl.rcParams["errorbar.capsize"] = 5
mpl.rcParams["axes.linewidth"] = 2
mpl.rcParams["xtick.major.size"] = 16
mpl.rcParams["xtick.major.width"] = 2 
mpl.rcParams["xtick.minor.size"] = 8 
mpl.rcParams["xtick.minor.width"] = 1 
mpl.rcParams["ytick.major.size"] = 16
mpl.rcParams["ytick.major.width"] = 2 
mpl.rcParams["ytick.minor.size"] = 8 
mpl.rcParams["ytick.minor.width"] = 1 
mpl.rcParams["axes.labelsize"] = 30
mpl.rcParams["xtick.labelsize"] = 25
mpl.rcParams["ytick.labelsize"] = 25
mpl.rcParams["legend.fontsize"] = 25
mpl.rcParams["xtick.direction"] = "in"
mpl.rcParams["ytick.direction"] = "in"
mpl.rcParams["ytick.right"] = True
mpl.rcParams["xtick.top"] = True
mpl.rcParams["xtick.minor.visible"] = True
mpl.rcParams["ytick.minor.visible"] = True


class transit: 

	r""" 
	A transit light-curve as a function of time. 

	Parameters 
	----------
	depth : real number 
		The fractional depth of the transit. Must be between 0 and 1. 
	t1 : real number 
		The time of the start of ingress. Must be positive. 
	t2 : real number 
		The time of the end of the ingress. Must be larger than t1. 
	t3 : real number 
		The time of the start of egress. Must be larger than t2. 
	t4 : real number 
		The time of the end of egress. Must be larger than t3. 

	Calling 
	-------
	This object can be called with only the time coordinate, and it will 
	evaluate and return the relative flux from the star at that time. 
	""" 

	def __init__(self, depth, t1, t2, t3, t4): 
		if all([isinstance(i, numbers.Number) for i in [t1, t2, t3, t4]]): 
			if 0 < t1 < t2 < t3 < t4: 
				if 0 <= depth <= 1: 
					# Use composition to store a set of line objects 
					self._times = [t1, t2, t3, t4] 
					self._lines = 5 * [None] # 5 piece-wise components 
					self._lines[0] = line.from_points([0, 1], [t1, 1]) 
					self._lines[1] = line.from_points([t1, 1], [t2, 1 - depth]) 
					self._lines[2] = line.from_points([t2, 1 - depth], 
						[t3, 1 - depth]) 
					self._lines[3] = line.from_points([t3, 1 - depth], [t4, 1]) 
					self._lines[4] = line.from_points([t4, 1], 
						[float("inf"), 1]) 
				else: 
					raise ValueError("Depth must be between 0 and 1. Got: %g" % (
						depth)) 
			else: 
				raise ValueError("""Invalid times. Must be positive and in \
ascending order.""") 
		else: 
			raise ValueError("Non-numerical value detected.") 


	def __call__(self, t): 
		# Determine the proper index of the line object to call 
		if isinstance(t, numbers.Number): 
			if t < self._times[0]: 
				index = 0 
			elif t > self._times[-1]: 
				index = 4 
			else: 
				for i in range(len(self._times) - 1): 
					if self._times[i] <= t <= self._times[i + 1]: 
						index = i + 1 
						break 
			return self._lines[index](t) 
		else: 
			raise TypeError("Expected real number. Got: %s" % (type(t))) 


	def show(self): 
		r""" 
		Plot the transit light-curve on the relative flux vs. time axis and 
		show to the user. 
		""" 
		from .dataset import dataset 
		fig = plt.figure(figsize = (12, 7)) 
		ax = fig.add_subplot(111, facecolor = "white") 
		ax.set_xlabel("Time (seconds)") 
		ax.set_ylabel("Relative Brightness") 
		ax.set_xlim([0, 36000]) 
		ax.set_ylim([0.98, 1.01]) 
		ax.yaxis.set_ticks([0.98, 0.99, 1.0, 1.01]) 
		data = dataset() 
		data.show(ax) 
		ax.text(13000, 1.002, r"$\chi_{dof}^2$ = %.2f" % (
			data.chi_squared(self)), fontsize = 25) 
		time = (
			(self._times[2] - self._times[0]) + 
			(self._times[3] - self._times[1]) 
		) / 2. 
		ax.text(13000, 1.005, "Transit Time: %.2f seconds" % (time), 
			fontsize = 25) 
		xvals = [ax.get_xlim()[0] + (ax.get_xlim()[1] - 
			ax.get_xlim()[0]) * i / 1000. for i in range(1001)] 
		ax.plot(xvals, [self.__call__(i) for i in xvals], c = 'r') 
		plt.tight_layout() 
		plt.show() 

