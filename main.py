from blogabet 	import Blogabet
from pymongo 	import MongoClient
from getpass 	import getpass


db_uri 				=	open('db_conn_string.txt', 'r').read().strip()
following_tipsters 	=	MongoClient(db_uri).betshit4.following_tipsters



b 	=	Blogabet()
b.analyze_tipster('fabiolo')



b.driver.close()



