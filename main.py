from getpass 	import getpass

from blogabet 	import Blogabet



#	Get credentials
try:
	email, password 	=	open('credentials.csv', 'r').readlines()[0].split(';')
except Exception as e:
	email 		=	input('Could not get Blogabet credentials from credentials file. Please, introduce your email (the one you registered with): ')
	password	=	getpass('Introduce your blogabet password: ')






b 	=	Blogabet(email, password)

b.blogabet_login()
b.go_to_tipster_page('dakson')

t 	=	b.scrape_tipster('dakson')


print(t)