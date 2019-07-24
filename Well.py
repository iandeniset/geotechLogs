import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)
import pandas as pd
from collections import OrderedDict #for removing legend duplicates

class Well:


	def __init__(self, **kwargs):
		self.name = kwargs.get('name', 'Borehole')
		self.xcoord = kwargs.get('xcoord', 0.0)
		self.ycoord = kwargs.get('ycoord', 0.0)
		self.elevation = kwargs.get('elevation', 0.0)
		self.date = kwargs.get('date', '---')
		self.project = kwargs.get('project', '---')
		self.logged_by = kwargs.get('logged_by', 'Not Specified')

	
	intervals = pd.DataFrame(columns=['Lithology', 'Top', 'Bottom', 'Description']) #empty dataframe to hold intervals

	def add_interval(self, top, bottom, lithology, description=''):
		#adds an interval to the well

		interval = {
		'Lithology':lithology,
		'Top':top,
		'Bottom':bottom,
		'Description':description
		}
		
		self.intervals = self.intervals.append(interval, ignore_index=True) #append passed values

		self.intervals = self.intervals.drop_duplicates() #drop any repeated rows incase code run twice

		self.intervals = self.intervals.sort_values(by='Top') #sorts intervals by depth; i.e. 'Top' col


	def remove_interval(self, layNum=None, lithology=None):
		#removes an interval based on its index (layer) value or lithology
		#NOTE: lithology method will remove all of that lithology type (i.e. possibly multiple layers)

		if (layNum == None) and (lithology == None):
			raise Exception('Need to specify a layer number or lithology!')

		if layNum != None:
			self.intervals = self.intervals.drop(layNum)

		if lithology != None:
			self.intervals = self.intervals[self.intervals.Lithology != lithology]


	def summary(self):
		#print out a brief summary of the well

		print('Well Name: ', self.name)
		print('Date Drilled: ', self.date)
		print('Project: ', self.project)
		print('Logged By: ', self.logged_by)
		print('Elevation: ', self.elevation)
		print('X and Y Coordinates: ', self.xcoord, self.ycoord)

		print(self.intervals)


	def plotWell(self, description=True, hatch=True, legend=False, figTitle=None, save=False):
		'''
		Plots single well log with optional hatching and description
		'''

		#set depth tick parameters first
		top = self.intervals.iloc[0]['Top']
		bttm = self.intervals.iloc[-1]['Bottom']
		z = bttm - top
		majorLocator = MultipleLocator(1) #sets the major tick interval to every meter
		majorFormatter = FormatStrFormatter('%d')
		minorLocator = MultipleLocator(0.25) #sets the minor tick interval to every 0.25 meter

		###
		#Generate Plot
		###

		fig, ax = plt.subplots(1,1, figsize=(2,12))

		#loop through each interval and plot
		for i in self.intervals.index: 
			#get the top and base of the current interval
			intTop = self.intervals.iloc[i]['Top']
			intBttm = self.intervals.iloc[i]['Bottom']

			#get the description for the current interval
			desc = self.intervals.iloc[i]['Description']

			#get plotting parameters for lithology type from pre defined dict
			lith = self.intervals.iloc[i]['Lithology'] #interval lith
			h = self.plotTemplates[lith]['hatch'] #hatch style
			c = self.plotTemplates[lith]['color'] #color
			alph = self.plotTemplates[lith]['alpha'] #alpha value

			#plot interval; nodes are uppr left, lwr left, lwr right, uppr right
			width = 1 #set the 'width' of the lith log
			x = [0,0,width,width]
			y = [intTop, intBttm, intBttm, intTop]
			ax.fill(x,y, c, hatch=h, alpha=alph, label=lith)

			#add in description text if specified
			if description:
				ax.text(width*1.1, intTop, desc, fontsize=12, verticalalignment='top')

			#set axes properties
			for spine in ['right', 'top', 'bottom']:
				ax.spines[spine].set_visible(False)

		ax.spines['left'].set_linewidth(1.5)
		ax.yaxis.set_major_locator(majorLocator)
		ax.yaxis.set_major_formatter(majorFormatter)
		ax.yaxis.set_minor_locator(minorLocator)
		ax.tick_params(axis='y', which='major', labelsize=12, width=1.5, length=10)
		ax.tick_params(axis='y', which='minor', width=1.5, length=5)
		ax.set_ylim(top, bttm)
		ax.set_xticks([])
		ax.invert_yaxis()
		ax.set_ylabel('Depth [m]', fontsize=15)

		if legend:
			h, l = ax.get_legend_handles_labels() #get handles and labels for current axis
			legDict = OrderedDict(zip(l,h)) #put labels and handles into ordered dict
			ax.legend(legDict.values(), legDict.keys(), fontsize=15 , bbox_to_anchor=(0.98,0.95))

		if save:
			figTitle = self.name
			ax.set_title(figTitle, size=15, pad=20)
			plt.savefig(figTitle.replace(' ','_'), dpi=175, bbox_inches='tight')

		plt.show()


	#################################################################
	###PLOTTING PARAMETER DICTIONARY
	#################################################################
	complex_zone = {
	'color': 'wheat',
	'hatch': '..',
	'alpha': 0.9
	}

	brown_clay = {
	'color': 'tan',
	'hatch': '---',
	'alpha': 0.7
	}

	grey_clay = {
	'color': 'dimgray',
	'hatch': '---',
	'alpha': 0.8
	}

	fill = {
	'color': 'black',
	'hatch': '..',
	'alpha': 0.7
	}

	silt = {
	'color': 'tan',
	'hatch': '\\\\\\',
	'alpha': 0.8
	}

	claySilt = {
	'color': 'tan',
	'hatch': '\\,--',
	'alpha': 0.8
	}

	clay = {
	'color': 'dimgray',
	'hatch': '---',
	'alpha': 0.8
	}

	siltClay = {
	'color': 'rosybrown',
	'hatch': '--,\\',
	'alpha': 0.8
	}

	till = {
	'color': 'peru',
	'hatch': 'xx',
	'alpha': 0.85
	}

	bedrock = {
	'color': 'khaki',
	'hatch': '\\\\',
	'alpha': 0.85
	}


	plotTemplates = {
	'Complex Zone' : complex_zone,
	'Brown Clay' : brown_clay,
	'Grey Clay' : grey_clay,
	'Fill' : fill,
	'Silt' : silt,
	'Clay Silt' : claySilt,
	'Clay' : clay,
	'Silt Clay' : siltClay,
	'Till' : till,
	'Bedrock' :  bedrock
	}


def plotSection(wells, width=5, grid=True, save=False, title='Cross-section', north=False, elevation=True, wellLabelHeight=1.5):
	'''
	Takes in a list of Well objects and plots them as a cross-section
	'''

	fig, ax = plt.subplots(1,1, figsize=(15,12))

	#first loop through each well in the list
	for w in wells:
		#next loop through each interval of each well
		for i in w.intervals.index: 
			#get the top and base of the current interval
			intTop = w.elevation - w.intervals.iloc[i]['Top'] #subtract from elevation
			intBttm = w.elevation - w.intervals.iloc[i]['Bottom'] #subtract from elevation

			#get plotting parameters for lithology type from pre defined dict
			lith = w.intervals.iloc[i]['Lithology'] #interval lith
			h = w.plotTemplates[lith]['hatch'] #hatch style
			c = w.plotTemplates[lith]['color'] #color
			alph = w.plotTemplates[lith]['alpha'] #alpha value

			#plot interval; nodes are uppr left, lwr left, lwr right, uppr right
			width = width #set the 'width' of the lith log
			xx = w.xcoord #xloc of well
			x = [xx,xx,xx+width,xx+width] #adds width to xlocation for box fill
			y = [intTop, intBttm, intBttm, intTop]
			ax.fill(x, y, c, hatch=h, alpha=alph, label=lith)

		#add well label at top
		wellTitleElevation = wellLabelHeight
		ax.text(xx+width*0.5, w.elevation+wellTitleElevation, w.name, rotation=90, fontsize=15, horizontalalignment='center') #plots in middle

	#axis format
	#set axis properties
	for spine in ['right', 'top']:
		ax.spines[spine].set_visible(False)

	ax.spines['left'].set_linewidth(1.5) #axis width
	ax.spines['bottom'].set_linewidth(1.5) #axis width

	majorLocator = MultipleLocator(1) #sets the major tick interval to every meter
	majorFormatter = FormatStrFormatter('%d')
	minorLocator = MultipleLocator(0.25) #sets the minor tick interval to every 0.25 meter
	ax.yaxis.set_major_locator(majorLocator)
	ax.yaxis.set_major_formatter(majorFormatter)
	ax.yaxis.set_minor_locator(minorLocator)

	if grid:
		ax.set_axisbelow(True)
		ax.yaxis.grid(which='major', alpha=0.75, ls='--')

	ax.tick_params(axis='both', which='major', labelsize=12, width=1.5, length=10)
	ax.tick_params(axis='both', which='minor', width=1.5, length=5)

	if north: ax.set_xlabel('Northing [m]', fontsize=15)
	else: ax.set_xlabel('Easting [m]', fontsize=15)
	if elevation: ax.set_ylabel('Elevation [m]', fontsize=15)
	else: ax.set_ylabel('Depth [m]', fontsize=15)
	ax.xaxis.set_major_formatter(majorFormatter)

	#ax.legend(fontsize=12.5,bbox_to_anchor=(1.28,1.1))
	h, l = ax.get_legend_handles_labels() #get handles and labels for current axis
	legDict = OrderedDict(zip(l,h)) #put labels and handles into ordered dict
	ax.legend(legDict.values(), legDict.keys(), fontsize=15 , bbox_to_anchor=(0.98,0.95))

	if save:
		figTitle = title
		plt.savefig(figTitle.replace(' ','_'), dpi=300, bbox_inches='tight')

	plt.show()

	return