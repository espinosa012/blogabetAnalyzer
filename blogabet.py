from __future__										import 	print_function
import  time
import 	datetime
from 	bs4 										import 	BeautifulSoup
from    selenium.webdriver.support.wait     		import 	WebDriverWait
from    selenium.webdriver.chrome.options   		import 	Options
from 	selenium.webdriver.common.keys 				import 	Keys
from 	selenium.webdriver.common.by 				import 	By
from 	selenium.webdriver.support 					import 	expected_conditions as EC
from 	pymongo 									import	MongoClient 	

import 	undetected_chromedriver as uc
import	getpass

from Pick 		import 	Pick
from Tipster 	import 	Tipster


class Blogabet(object):
	email 		=	''
	password 	=	''
	driver 		=	None

	logged_in 	=	False
	

	def __init__(self):
		self.driver	=	self.get_driver()
		

	def get_driver(self):
		options 		= 	Options()
		#options.add_argument("download.default_directory=/home/espinosa012/Documents/blogabetAnalyzer/xls/")

		#	Comment this line to not headless web navigator
		options.add_argument('--headless')
		driver 	=	uc.Chrome(options=options)
		driver.maximize_window()
		return driver

	def get_blogabet_credentials(self):
		pass

	def login(self):
		if self.logged_in:
			print('Already logged in.')
			return True

		print('Login into blogabet.com...')
		if not self.driver:
			self.set_driver()

		if not self.email: 
			self.email 		=	input('Blogabet email: ').strip()
		if not self.password:
			self.password 	=	getpass.getpass('Blogabet password: ').strip()
		

		self.driver.get('https://blogabet.com/')

		#	Login 
		login_button	=	'.//*[contains(text(), "LOG IN")]'
		WebDriverWait(self.driver,50).until(EC.presence_of_element_located((By.XPATH, login_button))).click()

		login_form 		=	WebDriverWait(self.driver,50).until(EC.presence_of_element_located((By.CLASS_NAME, "form-horizontal")))	
		
		time.sleep(0.6)
		print('Login into blogabet...')
		time.sleep(0.6)
		login_form.find_elements_by_tag_name('input')[0].send_keys(self.email)
		time.sleep(0.6)
		login_form.find_elements_by_tag_name('input')[1].send_keys(self.password + Keys.TAB + Keys.RETURN)
		

		print('Login done')
		self.logged_in 	=	True
		



	def analyze_tipster(self, tipster=None):
		#	Getting tipster name	
		if not tipster:
			tipster =	input('Tipster to analyze: ').strip()

		t 	=	self.scrape_tipster_(tipster)

		#	Printing stats
		self.print_tipster_info(t)
		




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
		print(t)


	def download_xls(self, tipster):
		#	Download xls file with picks history (not available for all tipsters).
		#	Yo need to login in order to download xls file.
		self.login()

		time.sleep(5)
		print('Downloading xls file')
		self.driver.get('https://{}.blogabet.com/blog/sellerPicksExport'.format(tipster))
		#	si nos lleva a la página del tipster, no hemos podido descargar el xls (comprobar current url)
		time.sleep(5)
		if tipster in self.driver.current_url:
			print('Could not download xls file for {}'.format(tipster))



	def save_profit_chart_image(self, tipster):
		#	Save a png image of last year profit graphic
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




	def scrape_tipster_(self, tipster):
		#	Scrape tipster bet365 stats from its blog page. Method returns a dict with stats
		tipster_dict 	=	{
			'name':tipster, 
			'analysis_date':datetime.date.today().strftime("%d/%m/%Y"),
			'n_followers':'',
			'month_price':'',

			'stat_types':[],
			'bet365':{'n_picks':'', 'profit':''},

			'stakes':[],
			'sports':[],
			'history':[],
		}

		try:
			self.go_to_tipster_page(tipster)
		except Exception as e:
			raise e

		tipster_dict['n_followers']	=	self.driver.find_element_by_id('header-followers').get_attribute('innerHTML').strip()

		try:
			tipster_dict['month_price']	=	self.driver.find_element_by_class_name('tipster-price').get_attribute('innerHTML').strip().split('/')[0].strip()
		except:
			tipster_dict['month_price']	=	'free'

		WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Blog menu")]'))).click()
		
		options_menu 	=	WebDriverWait(self.driver,30).until(EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "modal-body blog-menu")]')))
		time.sleep(1)

		#	Click on PICKS ARCHIVE
		options_menu.find_elements_by_tag_name('a')[2].click()


		#	Cookies holder
		try:
			self.driver.find_element_by_xpath('//*[contains(@class, "cookiesHolder")]').find_element_by_tag_name('button').click()
		except:
			pass



		#	Wait the lateral panel to completly load
		table 	=	WebDriverWait(self.driver,15).until(EC.presence_of_element_located((By.XPATH, '//table[contains(@class, "tbl")]')))
		tables 	=	self.driver.find_elements_by_xpath('//table[contains(@class, "tbl")]')

		#	Click in "All" to not to see only "Paid" picks info and get stat_types to study proportion of free and premium picks
		for table in tables:
			if 'Stat type' in table.get_attribute('innerHTML'):

				#	Click in "All" to not to see only "Paid" picks
				table.find_elements_by_tag_name('tr')[1].find_elements_by_tag_name('td')[0].click()
				
				#	Reload elements
				table_index 	=	tables.index(table)
				table 	=	WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, '//table[contains(@class, "tbl")]')))
				table 	=	self.driver.find_elements_by_xpath('//table[contains(@class, "tbl")]')[table_index]

				#	Get tipster stat_type
				for tr in table.find_elements_by_tag_name('tr')[1:]:
					tds	=	tr.find_elements_by_tag_name('td')
					tipster_dict['stat_types'].append({
						'stat_type':tds[0].get_attribute('innerHTML').split('</label>')[1].strip(),
						'n_picks':int(tds[1].get_attribute('innerHTML').strip()),
						'profit':float(tds[2].find_element_by_tag_name('span').get_attribute('innerHTML').strip()),
					})

				#	Get "Free" stat_type
				free_n_picks 	=	tipster_dict['stat_types'][0]['n_picks'] - tipster_dict['stat_types'][1]['n_picks']
				try:
					free_n_picks 	=	free_n_picks - tipster_dict['stat_types'][2]['n_picks']
				except:
					pass

				free_profit 	=	tipster_dict['stat_types'][0]['profit'] - tipster_dict['stat_types'][1]['profit']
				try:
					free_profit 	=	free_profit - tipster_dict['stat_types'][2]['profit']
				except:
					pass

				tipster_dict['stat_types'].append({
					'stat_type':'Free', 
					'n_picks':free_n_picks,
					'profit':free_profit
				})


		#	Analyze only bet 365 picks (all, not only paid)
		WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Picks archive"]')))

		table 	=	WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, '//table[contains(@class, "tbl")]')))
		tables 	=	self.driver.find_elements_by_xpath('//table[contains(@class, "tbl")]')
		for table in tables:
			if 'Bookmakers' in table.get_attribute('innerHTML'):
				for tr in table.find_elements_by_tag_name('tr'):
					if 'Bet365' in tr.get_attribute('innerHTML'):
						tipster_dict['bet365']['n_picks'] 	=	int(tr.find_elements_by_tag_name('td')[1].get_attribute('innerHTML').strip())
						tipster_dict['bet365']['profit'] 	=	int(tr.find_elements_by_tag_name('td')[2].find_element_by_tag_name('span').get_attribute('innerHTML').strip())
						tr.click()

		#	Get 'All' stats (not only paid) (after clicking)		
		WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Stat type"]')))
		


		table 	=	WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, '//table[contains(@class, "tbl")]')))
		tables 	=	self.driver.find_elements_by_xpath('//table[contains(@class, "tbl")]')

		time.sleep(3)
		'''
		Tables: Stakes, Leagues, Month
		'''
		stakes_table 	=	WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, '//th[contains(text(), "Stakes")]')))
		for tr in stakes_table.find_element_by_xpath('../../..').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr'):
			tipster_dict['stakes'].append({
				'stake':tr.find_elements_by_tag_name('td')[0].get_attribute('innerHTML').split('</label>')[1].strip(),
				'n_picks':tr.find_elements_by_tag_name('td')[1].get_attribute('innerHTML').strip(),
				'profit':int(tr.find_elements_by_tag_name('td')[2].find_element_by_tag_name('span').get_attribute('innerHTML').strip())
			})

		sports_table 	=	WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, '//th[contains(text(), "Leagues")]')))
		for tr in sports_table.find_element_by_xpath('../../..').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr'):
			tipster_dict['sports'].append({
				'sport':tr.find_element_by_xpath('.//i[contains(@class, "enable-tooltip sport-icon ")]').get_attribute('data-original-title'),
				'n_picks':tr.find_elements_by_tag_name('td')[1].get_attribute('innerHTML'),
				'profit':tr.find_elements_by_tag_name('td')[2].find_element_by_tag_name('span').get_attribute('innerHTML')
			})

		history_table 	=	WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, '//th[contains(text(), "Month")]')))
		for tr in history_table.find_element_by_xpath('../../..').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr'):
			tipster_dict['history'].append({
				'month':tr.find_elements_by_tag_name('td')[0].get_attribute('innerHTML').split('</label>')[1].strip(),
				'n_picks':tr.find_elements_by_tag_name('td')[1].get_attribute('innerHTML').strip(),
				'profit':int(tr.find_elements_by_tag_name('td')[2].find_element_by_tag_name('span').get_attribute('innerHTML').strip())
			})


		return tipster_dict
						


	 


	def lab(self):
		'''
		Looks for picks in 'lab' collection and determine result
		'''	
		db_uri 	=	open('db_conn_string.txt', 'r').read().strip()
		lab 	=	MongoClient(db_uri).betshit4.lab

		for p in lab.find():
			pick 	=	Pick(p)
			pick.print_pick()

			input('continue?')

		

