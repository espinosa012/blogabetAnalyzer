

from blogabet 	import Blogabet

try:
	#	Instancing blogabet object
	b 	=	Blogabet()

	#	Login into website
	b.blogabet_login()


	tipster 	=	input('Tipster to analyze: ').strip()
	t 	=	b.scrape_tipster(tipster)

	b.print_tipster_info(t)

except Exception as e:
	raise e