from blogabet 	import Blogabet

try:
	#	Instancing blogabet object
	b 	=	Blogabet()

	#	Login into website
	#b.blogabet_login()

	tipster =	input('Tipster to analyze: ').strip()
	#t 		=	b.scrape_tipster(tipster)


	b.download_xls(tipster)


	b.print_tipster_info(t)
	b.driver.close()

except Exception as e:
	print(e)
	b.driver.close()
	raise e