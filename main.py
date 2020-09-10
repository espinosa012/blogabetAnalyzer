from blogabet 	import Blogabet

try:
	#	Instancing blogabet object
	b 	=	Blogabet()

	#	Getting tipster name	
	tipster =	input('Tipster to analyze: ').strip()
	t 		=	b.scrape_tipster(tipster)

	#	Printing stats
	b.print_tipster_info(t)
	b.driver.close()

except Exception as e:
	print(e)
	b.driver.close()
	raise e