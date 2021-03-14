#Scraper 2 Flipkart

import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as W
from selenium.webdriver.support import expected_conditions as EC
import time

#Path for chrome driver in local machine
#Change it accordingly
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
url = "https://www.flipkart.com"

def get_url(search_term):
	template = 'https://www.flipkart.com/search?q={}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
	search_term = search_term.replace(' ','+')
	return template.format(search_term)

data_list = []
rank = 0
#page = 0
#flag = 1

#change range to (1, 101)
for page in range(1, 6):
	#page = page + 1
	print('Processing page no: ', page, ' ****************************************************************************************')
	url = get_url('laptop')
	extension = '&page=' + str(page)
	url += extension
	driver.get(url)

	soup = BeautifulSoup(driver.page_source, 'html.parser')

	#for every row
	results = soup.find_all('div',{'class': '_1AtVbE col-12-12'})

	#for every element
	#results = soup.find_all('div',{'class': '_1xHGtK _373qXS'})
	for result in results:
		next_div = result.find_all('div',{'class': '_13oc-S'})

		for item in next_div:
			divs = item.find_all('div', {'style': 'width:25%'})
			divs2 = item.find_all('div', {'style': 'width:100%'})
			#print('========')
			#print(len(divs))
			#print(len(divs2))

			#for 4 elements in a row
			if len(divs) != 0:

				for div_tab in divs:
					element_list = []
					#print(div_tab.get('data-id'))
					element_list.append(div_tab.get('data-id'))
					rank = rank + 1
					element_list.append(rank)
					spantag = div_tab.find_all('span')

					#for checking AD
					for span in spantag:
						if span.text == 'Ad':
							#print('Advertised')
							element_list.append(1) #1 means it is advertised
						else:
							element_list.append(0)

					atags = div_tab.find_all('a')
					for a in atags:
						if a.get('title'):
							element_list.append(a.get('title'))
							#print(a.get('title'))
							#print('--------------------')
					data_list.append(element_list)

			#for 1 element in a row
			elif len(divs2) != 0:
				for div_tab in divs2:
					element_list = []
					element_list.append(div_tab.get('data-id'))
					rank = rank + 1
					element_list.append(rank)
					spantag = div_tab.find_all('span')

					#for checking AD
					flag = 0
					for span in spantag:
						if span.text == 'Ad':
							flag = 1 #1 means it is advertised

					element_list.append(flag)
					a = div_tab.find('a')
					#print(a.text)
					element_list.append(a.text)

					data_list.append(element_list)

for listele in data_list:
	print(listele)