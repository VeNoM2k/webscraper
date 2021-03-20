#Scraper 1 Flipkart

import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as W
from selenium.webdriver.support import expected_conditions as EC
import requests
import pandas as pd
import time

#Path for chrome driver in local machine
#Change it accordingly
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver1 = webdriver.Chrome(PATH)
url = "https://www.flipkart.com"

def get_url(search_term):
	template = 'https://www.flipkart.com/search?q={}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
	search_term = search_term.replace(' ','+')
	return template.format(search_term)

data_list = []
rank = 0

#First 5 pages
for page in range(1, 2):
	print('Processing page no: ', page, ' ****************************************************************************************')

	#Change query here
	url = get_url('laptop')
	extension = '&page=' + str(page)
	url += extension
	driver.get(url)
	soup = BeautifulSoup(driver.page_source, 'html.parser')

	#for every row
	results = soup.find_all('div',{'class': '_1AtVbE col-12-12'})
	for result in results:
		next_div = result.find_all('div',{'class': '_13oc-S'})

		for item in next_div:
			divs = item.find_all('div', {'style': 'width:25%'})
			divs2 = item.find_all('div', {'style': 'width:100%'})

			#for 4 elements in a row
			if len(divs) == 4:
				for div_tab in divs:
					element_list = []
					rank = rank + 1
					element_list.append(rank)
					element_list.append(div_tab.get('data-id'))
					atags = div_tab.find_all('a')
					for a in atags:
						if a.get('title'):
							product_url = 'https://www.flipkart.com' + a.get('href')
							break
					driver.get(product_url)
					soup1 = BeautifulSoup(driver.page_source, 'html.parser')
					results = soup1.find('div',{'class': '_3_L3jD'})
					try:
						spantag = results.find_all('span')
						if len(spantag) >=2:
							element_list.append(spantag[0].text)
							element_list.append(spantag[1].text)
					except:
						element_list.append(0)	#No ratings given
						element_list.append('0 Ratings and 0 Reviews')

					results2 = soup1.find('span',{'class': 'b7864- _2Z07dN'})
					try:
						if len(results2) >= 1:
							#element_list.append(1)	#product is flipkart assured
							featured_seller_fa = 1
						else:
							featured_seller_fa = 0
					except:
						featured_seller_fa = 0


					product_price_tag = soup1.find('div',{'class': '_25b18c'})
					product_price = product_price_tag.find('div',{'class': '_30jeq3 _16Jk6d'})
					price = product_price.text

					seller_list = []

					litag = soup1.find_all('li', {'class': '_38I6QT'})

					if len(litag) > 0:
						for lis in litag:
							a_tag = lis.find('a')
							seller_url = 'https://www.flipkart.com' + a_tag.get('href')
							driver1.get(seller_url)
							time.sleep(5)
							soup2 = BeautifulSoup(driver1.page_source, 'html.parser')
							results3 = soup2.find('div',{'id': 'container'})
							results4 = results3.find_all('div',{'class': '_2Y3EWJ'})
							for each in results4:
								seller_info = []
								other_seller_name_tag = each.find('div',{'class': 'isp3v_ col-3-12'})
								other_seller_name = other_seller_name_tag.find('div',{'class': '_3enH42'})
								#print(other_seller_name.text)
								seller_info.append(other_seller_name.text)

								try:
									try:
										other_seller_rating = other_seller_name_tag.find('div',{'class': '_3LWZlK _2GCNvL'})
										#print(other_seller_rating.text)
										other_seller_rate = other_seller_rating.text
									except:
										other_seller_rating = other_seller_name_tag.find('div',{'class': '_3LWZlK _32lA32 _2GCNvL'})
										#print(other_seller_rating.text)
										other_seller_rate = other_seller_rating.text
								except:
									#print(0)
									other_seller_rate = 0

								seller_info.append(other_seller_rate)

								other_seller_price_tag = each.find('div',{'class': '_1GFtIv col-3-12'})
								other_seller_price = other_seller_price_tag.find('div',{'class': '_30jeq3'})
								#print(other_seller_price.text)
								seller_info.append(other_seller_price.text)

								other_seller_fa_tag = each.find_all('img',{'src': '//static-assets-web.flixcart.com/www/linchpin/fk-cp-zion/img/fa_62673a.png'})
								if len(other_seller_fa_tag) > 0:
									other_seller_fa = 1
								else:
									other_seller_fa = 0
								#print(other_seller_fa)
								seller_info.append(other_seller_fa)
								seller_list.append(seller_info)

					#featured seller
					else:
						sellertag = soup1.find_all('div',{'id': 'sellerName'})
						for tag in sellertag:
							seller_info = []
							spantag = tag.find('span')
							seller_name = spantag.find('span')
							seller_info.append(seller_name.text)
							#print(seller_name.text)	#featured seller name
							seller_rating = spantag.find('div')
							seller_info.append(seller_rating.text)
							#print(seller_rating.text)	#featured seller rating
							seller_info.append(price)
							seller_info.append(featured_seller_fa)
							seller_list.append(seller_info)

					element_list.append(len(seller_list))
					element_list.append(seller_list)

					data_list.append(element_list)


			#for 1 element in a row
			elif len(divs2) == 1:
				for div_tab in divs2:
					element_list = []
					rank = rank + 1
					element_list.append(rank)
					element_list.append(div_tab.get('data-id'))
					a = div_tab.find('a')
					#print(a.text)
					product_url = 'https://www.flipkart.com' + a.get('href')
					driver.get(product_url)
					soup1 = BeautifulSoup(driver.page_source, 'html.parser')
					results = soup1.find('div',{'class': '_3_L3jD'})
					try:
						spantag = results.find_all('span')
						if len(spantag) >=2:
							element_list.append(spantag[0].text)
							element_list.append(spantag[1].text)
					except:
						element_list.append(0)	#No ratings given
						element_list.append('0 Ratings and 0 Reviews')

					results2 = soup1.find('span',{'class': 'b7864- _2Z07dN'})
					try:
						if len(results2) >= 1:
							#element_list.append(1)	#product is flipkart assured
							featured_seller_fa = 1
						else:
							featured_seller_fa = 0
					except:
						featured_seller_fa = 0
					
					product_price_tag = soup1.find('div',{'class': '_25b18c'})
					product_price = product_price_tag.find('div',{'class': '_30jeq3 _16Jk6d'})
					price = product_price.text

					seller_list = []

					litag = soup1.find_all('li', {'class': '_38I6QT'})

					#for other sellers
					if len(litag) > 0:
						for lis in litag:
							a_tag = lis.find('a')
							seller_url = 'https://www.flipkart.com' + a_tag.get('href')
							driver1.get(seller_url)
							time.sleep(5)
							soup2 = BeautifulSoup(driver1.page_source, 'html.parser')
							results3 = soup2.find('div',{'id': 'container'})
							results4 = results3.find_all('div',{'class': '_2Y3EWJ'})
							for each in results4:
								seller_info = []
								other_seller_name_tag = each.find('div',{'class': 'isp3v_ col-3-12'})
								other_seller_name = other_seller_name_tag.find('div',{'class': '_3enH42'})
								#print(other_seller_name.text)
								seller_info.append(other_seller_name.text)

								try:
									try:
										other_seller_rating = other_seller_name_tag.find('div',{'class': '_3LWZlK _2GCNvL'})
										#print(other_seller_rating.text)
										other_seller_rate = other_seller_rating.text
									except:
										other_seller_rating = other_seller_name_tag.find('div',{'class': '_3LWZlK _32lA32 _2GCNvL'})
										#print(other_seller_rating.text)
										other_seller_rate = other_seller_rating.text
								except:
									#print(0)
									other_seller_rate = 0

								seller_info.append(other_seller_rate)

								other_seller_price_tag = each.find('div',{'class': '_1GFtIv col-3-12'})
								other_seller_price = other_seller_price_tag.find('div',{'class': '_30jeq3'})
								#print(other_seller_price.text)
								seller_info.append(other_seller_price.text)

								other_seller_fa_tag = each.find_all('img',{'src': '//static-assets-web.flixcart.com/www/linchpin/fk-cp-zion/img/fa_62673a.png'})
								if len(other_seller_fa_tag) > 0:
									other_seller_fa = 1
								else:
									other_seller_fa = 0
								#print(other_seller_fa)
								seller_info.append(other_seller_fa)
								seller_list.append(seller_info)

					#featured seller
					else:
						sellertag = soup1.find_all('div',{'id': 'sellerName'})
						for tag in sellertag:
							seller_info = []
							spantag = tag.find('span')
							seller_name = spantag.find('span')
							seller_info.append(seller_name.text)
							#print(seller_name.text)	#featured seller name
							seller_rating = spantag.find('div')
							seller_info.append(seller_rating.text)
							#print(seller_rating.text)	#featured seller rating
							seller_info.append(price)
							seller_info.append(featured_seller_fa)
							seller_list.append(seller_info)

					element_list.append(len(seller_list))
					element_list.append(seller_list)

					data_list.append(element_list)


frame = pd.DataFrame(data_list, columns = ['Rank', 'Data-id', 'Product Rating', 'Product Review and Rating', 'No. of Sellers', 'Seller List'])
frame.to_csv('Product_info.csv')
