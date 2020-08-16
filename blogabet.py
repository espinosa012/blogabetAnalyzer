from __future__										import 	print_function
import  time
import 	datetime
import 	platform
from 	getpass 									import 	getpass

import 	bba_image

from 	bs4 										import 	BeautifulSoup
from 	PIL 										import 	Image
from 	selenium.webdriver 							import 	Chrome
from    selenium.webdriver.support.wait     		import 	WebDriverWait
from    selenium.webdriver.chrome.options   		import 	Options
from 	selenium.webdriver.common.keys 				import 	Keys
from 	selenium.webdriver.common.by 				import 	By
from 	selenium.webdriver.support 					import 	expected_conditions as EC
from 	selenium.webdriver.common.action_chains 	import 	ActionChains



class Blogabet(object):
	email 		=	''
	password 	=	''
	driver 		=	None

	logged_in 	=	False
	
	def __init__(self):
		#self.email, self.password   	=	self.get_credentials()
		self.driver 					=	self.get_driver()
		


	def get_credentials(self, credentials_path='credentials.csv'):
		#	Get credentials
		try:
			email, password 	=	open(credentials_path, 'r').readlines()[0].split(';')
		except Exception as e:
			email 		=	input('Could not get Blogabet credentials from credentials file. Please, introduce your email (the one you registered with): ')
			password	=	getpass('Introduce your blogabet password: ')

		return email, password

	def get_driver(self):
		options 		= 	Options()

		#	Comment this line to not headless web navigator
		#options.add_argument('--headless')

		webdriver_path 	= 	'webdriver/chromedriver'
		if 'Win' in str(platform.system()):
			webdriver_path	=	webdriver_path+'.exe'

		try:
			driver 	=	Chrome(executable_path=webdriver_path, chrome_options=options)
			driver.maximize_window()
			return driver
		except Exception as e:
			raise Exception('Could not get webdriver ({}), please download webdriver for your platform from https://chromedriver.chromium.org/'.format(e))


	def blogabet_login(self):

		#	Login info
		self.email 		=	input('Blogabet email: ')
		self.password 	=	input('Blogabet password: ')

		#!!!!
		email 		=	self.email
		password	=	self.password	

		self.driver.get('https://blogabet.com/')

		#	Login 
		login_button	=	'.//*[contains(text(), "LOG IN")]'
		WebDriverWait(self.driver,50).until(EC.presence_of_element_located((By.XPATH, login_button))).click()

		login_form 		=	WebDriverWait(self.driver,50).until(EC.presence_of_element_located((By.CLASS_NAME, "form-horizontal")))	
		
		time.sleep(0.6)
		print('Login into blogabet...')
		time.sleep(0.6)
		login_form.find_elements_by_tag_name('input')[0].send_keys(email)
		time.sleep(0.6)
		login_form.find_elements_by_tag_name('input')[1].send_keys(password + Keys.TAB + Keys.RETURN)
		print('Login done')

		self.logged_in 	=	True
		time.sleep(3)
		



	def go_to_tipster_page(self, tipster):
		try:
			self.driver.get('https://{}.blogabet.com/'.format(tipster))

			try:
				WebDriverWait(self.driver,20).until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Win rate")]')))
				return True
			except:
				if 'Blog not found' in self.driver.page_source:
					raise Exception('Blog not found for tipster: {}'.format(tipster))
				else:
					raise Exception('Could not get tipster page')

		except Exception as e:
			raise Exception(e)


	def export_stats_to_html(self):
		pass




	def print_tipster_info(self, t):
		#	Method to print information in a more kind manner. Receives tipster dict
		'''
		print('Tipster: ', t['name'])
		print('Total picks: ', t['n_picks'])
		print('Blogabet followers: ', t['n_followers'])
		print('----------------------------------------')
		print('Total profit: ', t['profit'])
		print('Total yield: ', t['yield'])
		print('----------------------------------------')
		print('-----------------SPORTS-----------------')
		for sp in t['sports']:
			print(sp['sport'], '\ttotal picks: ', sp['picks'])
			print('\t\twin rate: ', sp['win_rate'], ' - ', 'profit: ', sp['profit'],  ' - ', 'yield: ', sp['yield'])
			print('\t\todds average: ', sp['odds_avg'], ' - ', 'Stake average: ',  sp['stake_avg'])

		'''		
		print(t)



	def get_last_year_profits(self, tipster):
		#self.save_profit_chart_image(tipster)

		profit_chart 	=	self.driver.find_element_by_class_name('stats').find_elements_by_class_name('col-md-12')[2]#.find_elements_by_tag_name('path')
		#value_elements	=	profit_chart.find_elements_by_tag_name('text')	

		#	Obtenemos los valores del eje 'y' de la gráfica
		y_values 			=	bba_image.get_values_from_elements(profit_chart.find_elements_by_tag_name('text'))
		

		#	Obtenemos los valores reales del gráfico
		values 	=	bba_image.get_chart_values(self.driver)		


		#bba_image.get_profit_chart_info(tipster, value_elements)



	def save_profit_chart_image(self, tipster):
		#	Guarda una imagen png del elemento web del gráfico de beneficios del último año

		profit_chart 	=	self.driver.find_element_by_class_name('stats').find_elements_by_class_name('col-md-12')[2]#.find_elements_by_tag_name('path')

		location 	= 	profit_chart.location
		size 		= 	profit_chart.size

		self.driver.save_screenshot("./profit_charts/{}.png".format(tipster))
		
		x 	= 	location['x']
		y 	= 	location['y']
		
		width 	= 	location['x']+size['width'] 
		height 	= 	location['y']+size['height'] 




		#	.convert('RGB') si se somite, incluye canal alpha
		im 	= 	Image.open('profit_charts/{}.png'.format(tipster)).convert('RGB')

		#	Recortamos la porción de la pantalla correspondiente a la gráfica 
		im 	= 	im.crop((int(x), int(y), int(width), int(height)))
		im.save('./profit_charts/{}.png'.format(tipster))





	def scrape_tipster(self, tipster):
		#	Scrape tipster stats from its blog page. Method returns a dict with stats
		#if not self.logged_in:
			#self.blogabet_login()
		try:
			self.go_to_tipster_page(tipster)
		except Exception as e:
			raise e

		#driver 	=	self.driver


		tipster_dict 	=	{'name':tipster}
		self.go_to_tipster_page(tipster)

		tipster_dict['n_picks']		=	self.driver.find_element_by_id('header-picks').get_attribute('innerHTML').strip()
		tipster_dict['profit']		=	self.driver.find_element_by_id('header-profit').get_attribute('innerHTML').strip()
		tipster_dict['yield']		=	self.driver.find_element_by_id('header-yield').get_attribute('innerHTML').strip()
		tipster_dict['n_followers']	=	self.driver.find_element_by_id('header-followers').get_attribute('innerHTML').strip()

		try:
			tipster_dict['month_price']	=	self.driver.find_element_by_class_name('tipster-price').get_attribute('innerHTML').strip().split('/')[0].strip()
		except:
			tipster_dict['month_price']	=	'free'



		




		#	Entramos en el menú de estadísticas
		WebDriverWait(self.driver,50).until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Blog menu")]'))).click()

		options_menu 	=	WebDriverWait(self.driver,30).until(EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "modal-body blog-menu")]')))
		time.sleep(1)

		options_menu.find_elements_by_tag_name('a')[1].click()

		#	Clickamos en 'All-times' para obtener las estadísticas totales de los tipsters de pago (no funciona)
		pass


		#	Agregar al bucle 'CATEGORIES' y 'ARCHIVE'
		stats_categories 	=	['SPORTS', 'STAKES', 'BOOKIES', 'ODDS RANGE', 'ARCHIVE']
		for sc in stats_categories:
			try:
				#	Comprobamos si el menú esta desplegado
				collapse 		=	WebDriverWait(self.driver,30).until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "{}")]'.format(sc)))).find_element_by_xpath('../../..').find_element_by_id('collapse{}alltime'.format(sc.lower().replace(' ', '_')))
				collapse_class	=	collapse.get_attribute('class')

				table 			=	collapse.find_element_by_tag_name('table')

				sc_dicts		=	[]											
				table_headers 	=	table.find_elements_by_tag_name('th')		#	encabezados de la tabla
				regs 			=	table.find_elements_by_tag_name('tr')[1:]	#	cada uno de los registros de la tabla

				for r in regs:
					cols 			=	[]
					col_0 	=	r.find_element_by_tag_name('td').get_attribute('innerHTML').replace('\n','')[28:].strip()
					if 'Bet365' in col_0: col_0 = 'Bet365'
					cols.append(col_0)
					for col in r.find_elements_by_tag_name('td')[1:]:
						try:
							col = 	col.find_element_by_tag_name('span').get_attribute('innerHTML').strip()
						except:
							col = 	col.get_attribute('innerHTML').strip()

						cols.append(col)

					ths 	=	[]
					sc_dict	=	{}											#	diccionario para almacenar cada registro de la tabla
					for th in table_headers:
						sc_dict[th.get_attribute('innerHTML').strip().lower().replace(' ', '_').replace('.','').replace('stakes', 'stake').replace('sports', 'sport').replace('bookies', 'bookie')] 	=	cols[table_headers.index(th)] 
				
					sc_dicts.append(sc_dict)

				tipster_dict[sc.lower()]	=	sc_dicts
			except:
				#print('Error gettin stats ({})'.format(sc))
				pass

		#	Corregimos el error que aparece al tomar la info de bookies con bloqueo
		for b in tipster_dict['bookies']:
			b['bookie'] 	=	b['bookie'].split('&')[0].strip()



		#	Datos por meses
		history 	=	[]

		WebDriverWait(self.driver,50).until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "STATISTICS")]'))).click()
		time.sleep(1.5)
		WebDriverWait(self.driver,30).until(EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "modal-body blog-menu")]'))).find_elements_by_tag_name('a')[2].click()


		time.sleep(1.5)

		trs 	=	self.driver.find_elements_by_class_name('tbl')[5].find_elements_by_tag_name('tr')
		for tr in trs[1:]:
			tds 	= 	tr.find_elements_by_tag_name('td')

			month 	=	tds[0].get_attribute('innerHTML').strip().split('</label>')[1].strip()
			n_picks	=	tds[1].get_attribute('innerHTML').strip()
			profit 	=	tds[2].get_attribute('innerHTML').strip().split('>')[1].strip().split('<')[0]

			history.append({
				'month':month,
				'n_picks':n_picks,
				'profit':profit
			})

			'''
			'''

		tipster_dict['history'] 	=	history
		print(tipster_dict)

		return tipster_dict

			 
