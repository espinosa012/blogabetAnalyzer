from 	bs4 										import 	BeautifulSoup

from 	selenium.webdriver 							import 	FirefoxOptions, Firefox
from    selenium.webdriver.support.wait     		import 	WebDriverWait
from    selenium.webdriver.chrome.options   		import 	Options
from 	selenium.webdriver.common.keys 				import 	Keys
from 	selenium.webdriver.common.by 				import 	By
from 	selenium.webdriver.support 					import 	expected_conditions as EC

#import 	blogabet

class Tipster():
	name 		=	''
	n_picks 	=	''
	profit 		=	''
	yield_  	=	''
	n_followers	=	''
	history		=	False	
	month_price	=	''

	sports_stats	=	[]
	stakes_stats 	=	[]

	bet365_stats 	=	[]

	def __init__(self, args):

		self.name 			=	args['name']
		self.n_picks		=	args['n_picks']
		self.profit			=	args['profit']
		self.yield_			=	args['yield']
		self.n_followers	=	args['n_followers']
		self.month_price	=	args['month_price']

		for sp in args['sports']:
			self.sports_stats.append(sp)

		self.bet365_stats 	=	args['bookies'][0]


	def to_dict(self):
		#	Return a dict with tipster basic information
		return {
			'name'			:	self.name,
			'n_picks'		:	self.n_picks,
			'profit'		:	self.profit,
			'yield'			:	self.yield_,
			'n_followers'	:	self.n_followers,
		}


