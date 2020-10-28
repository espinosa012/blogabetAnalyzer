from blogabet 	import Blogabet
from pymongo 	import MongoClient
from getpass 	import getpass

tipster =	input('Tipster to analyze: ')

b 	=	Blogabet()
b.analyze_tipster(tipster)
b.driver.close()



