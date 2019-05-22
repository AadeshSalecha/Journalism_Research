import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import lxml.html
import string
from urllib.request import urlopen, Request
import datetime
from os import listdir
from os.path import isfile, join
import requests
from bs4 import BeautifulSoup, Comment
import csv
import re
import sys 
import ssl

ssl.match_hostname = lambda cert, hostname: True

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
CONST_MAX_IMG = 10
CONST_DATA_COL = 11
mypath = "/home/salec006/Research/Data/"
files = []

def numFiles():
	return len(files)

def filterNonHTTPS(lst):
	ans = []
	for row in lst:
		if(row[CONST_DATA_COL].find("https") != -1):
			ans.append(row)
	return ans

def filterRT(lst):
	ans = []
	for row in lst:
		if(row[CONST_DATA_COL][:2] != "RT"):
			ans.append(row)
	return ans

def getTwittertoNewsLink(url):
	try:
		page = requests.get(url)
		soup = BeautifulSoup(page.text, 'html.parser')
		p = soup.find('p', class_="TweetTextSize TweetTextSize--jumbo js-tweet-text tweet-text").find_all('a')
		for anchor in p:
			if(anchor.has_attr('data-expanded-url')):
				return anchor['data-expanded-url']
		
		print(url + " Could not extract twitter")		
		return None
	except:
		print(url + " Could not extract twitter")
		return None

def main(onlyFilter):
	files = [f for f in listdir((mypath + "result_output")) if isfile(join((mypath + "result_output"), f))]

	new_files = []
	if(len(sys.argv) > 1):
		for i in range(1, len(sys.argv)):
			if(sys.argv[i] + ".out.csv" in files):
				new_files.append(sys.argv[i]+".out.csv")
		files = new_files
	print(files)
	
	for f in files:	
		try:
			raw_data = []
			data = []
			article_index = 0; twitter = 0; broken = 0; skipped = 0; numReTweets = 0; numWithoutHTTPS = 0; 

			with open(mypath + "result_output/" + f, mode='r') as inptr:
				reader = csv.reader(inptr)
				for row in reader:
					raw_data.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11]])
				
				data = filterRT(raw_data)
				numReTweets = len(raw_data) - len(data)
				data = filterNonHTTPS(data)
				numWithoutHTTPS = len(raw_data) - numReTweets - len(data)
			
			with open(mypath + "output/Filtered" + f, mode='w', encoding="utf-8") as outptr:
				writer = csv.writer(outptr, dialect='excel', delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
				writer.writerow(["Index", "ID", "User_ID", "Friends_Count", "Followers_Count", "Favourites_Count", "Listed_Count", "Status_Count", "Created_at", "Retweet_Count", "Favourite_Count", "Created_at", "Text"])
				for i in range(len(data)):
					row = data[i]
					writer.writerow([i+1, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11]])
			
			if(onlyFilter):
				continue				

			login_url = "https://www.wsj.com/"
			browser = webdriver.Firefox()
			browser.get(login_url)

			browser.find_element_by_link_text("Sign In").click()
			browser.find_element_by_id("username").send_keys('journalism.jisu@gmail.com')             # Input username
			browser.find_element_by_id("password").send_keys('rawork11')     # Input password
			browser.find_element_by_class_name("sign-in").click()

			time.sleep(10)

			with open(mypath + "output/Result" + f, mode='w', encoding="utf-8") as outptr:
				writer = csv.writer(outptr, dialect='excel', delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
				writer.writerow(["Index", "Publisher", "URL", "Date", "Num_Images", "Caption", "Credit/Source"]);
				org_name = f[:f.find(".out")].lower()

				for i in range(len(data)):
					row = data[i]
					links = re.findall(r'(https?://\S+)', row[CONST_DATA_COL])
					flag = False

					print(f[:3], i)
					try:
						for link in links:
							if(flag == True):
								break

							page = requests.get(link)
							# print(page.url)
							if((re.findall(r'^(http:|https:|)[/][/]([^/]+[.])', page.url))[0][1].find("twitter") != -1):
								twitter += 1
								news_link = getTwittertoNewsLink(page.url)
								if(news_link == None):
									break

								page = requests.get(news_link)

							# if page doesn't exists
							if(page.ok == False):
								broken += 1
								break;
							# if page is not of organisation
							if(page.url.find(org_name) == -1):
								numWithoutHTTPS += 1
								print("\t\t\t\t" + org_name + " tried accessing " + page.url + " originally was " + link)
								break

							# Find images
							browser.get(page.url)	
							time.sleep(10)

							soup = BeautifulSoup(browser.page_source, 'lxml') #html.parser')
							images, date = getImagesandDate(i+1, soup, org_name)
							if(images == [] and date == ""):
								break

							article_index += 1		
							flag = True		
							if(len(images) == 0):
								writer.writerow([i+1, org_name, page.url, date, len(images),"NA", "NA"])

							for img_num in range(min(CONST_MAX_IMG, len(images))):
								if(img_num == 0):
									writer.writerow([i+1, org_name, page.url, date, len(images), "NA" if(images[img_num][0] == "") else images[img_num][0], "NA" if(images[img_num][1] == "") else images[img_num][1]])
								else:
									writer.writerow([i+1, org_name, "", "", len(images), "NA" if(images[img_num][0] == "") else images[img_num][0], "NA" if(images[img_num][1] == "") else images[img_num][1]])

					except Exception as e:
						print(str(i+1) + " " + f + " Skipped one Article " + str(e))
						skipped += 1

				writer.writerow(["\n\n" + str(datetime.datetime.now()) + "\n"])
				writer.writerow(['%-40s %-10s %-10s %-10s %-10s' % ("News Org", "Input", "RTs", "NoLinks", "Output")])
				writer.writerow(['%-40s %-10s %-10s %-10s %-10s' % (org_name, len(raw_data), numReTweets, numWithoutHTTPS + skipped + broken, article_index)])
			
			browser.quit()

		except Exception as e:
			print("Tried reading " + f + " file, something went wrong " + str(e))


def getImagesandDate(id, soup, org):	
	images = []
	date = ""
	org = org.lower()

	try:
		
		if(org == "wsj"):
			date = soup.find('time').get_text().lstrip().rstrip()
			
			all_images = soup.find_all('div', {'class':'media-object-image'})
			for image in all_images:
				if(image.find('img') == None):
					continue

				cc = image.find('span', {'class':'wsj-article-caption-content'})
				cr = image.find('span', {'class':'wsj-article-credit'})

				if(cr == None and cc != None):
					cc = cc.get_text()
					cr = cc[cc.rfind('['):] if(cc.rfind('[') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else None
				
				cc = "" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip()
				cr = "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()	
				if(not(cc == "" and cr == "")):
					images.append([cc, cr])			
				if(len(images) >= CONST_MAX_IMG):
					break

			text = soup.prettify()
			gallery_start = text.find('window.WEBUI_SLIDESHOWS.push')
			if(gallery_start != -1):
				gallery = text[gallery_start:text.find('</script>', gallery_start)]

				while(text.find('"caption":') != -1):
					cc_start = text.find('"caption":') + len('"caption":')
					cc = text[cc_start:text.find('"credit":', cc_start)]				
					cr_start = text.find('"credit":', cc_start) + len('"credit":')
					cr = text[cr_start:text.find('"imageSrc":', cr_start)]				

					text = text[text.find('"imageSrc":', cr_start) + 1:]
					images.append([cc.lstrip().rstrip(), cr.lstrip().rstrip()])
					if(len(images) >= CONST_MAX_IMG):
						break

		# misc = open("a.html", "w")
		# print(soup.prettify(), file = misc)
		# misc.close()

	except Exception as e:
		print("Exception in scrape " + str(id) + " " + org + " " + str(e))
		return [], ""

	return images, date



if __name__ == '__main__':
	if(len(sys.argv) > 2 and sys.argv[2] == "test"):

		# login_url = "https://sso.accounts.dowjones.com/login?state=g6Fo2SBPZGdNT0lKTzlBazJ3OHRTYVhWZU1Mb3lCN2Q1UVBBZ6N0aWTZMmdhRm8yU0JUY1djM01VYzNjVWxUTlZjMFluZHZRemR1VkVaUVQzbHZlSGhYVDA1S1ZBo2NpZNkgNWhzc0VBZE15MG1KVElDbkpOdkM5VFhFdzNWYTdqZk8&client=5hssEAdMy0mJTICnJNvC9TXEw3Va7jfO&protocol=oauth2&prompt=login&scope=openid%20idp_id%20roles%20email%20given_name%20family_name%20djid%20djUsername%20djStatus%20trackid%20tags&response_type=code&redirect_uri=https%3A%2F%2Faccounts.wsj.com%2Fauth%2Fsso%2Flogin&nonce=4a1fabf8-9706-4162-ad47-45d690e5266b&connection=DJldap&ui_locales=en-us-x-wsj-83-2&ns=prod%2Faccounts-wsj#!/signin"
		# s = requests.Session()
		# response = s.post(login_url, data = {"email":'journalism.jisu@gmail.com', 'password':'rawork11'})
		# print(response.text)
		### Here, we're getting the login page and then grabbing hidden form
		### fields.  We're probably also getting several session cookies too.
		
		link1 = "https://www.wsj.com/articles/a-pitcher-called-thor-learns-how-less-is-more-at-the-gym-11553338800?mod=cx_picks&cx_navSource=cx_picks&cx_tag=undefined&cx_artPos=5#cxrecs_s"
		link = "https://www.wsj.com/articles/men-ditch-suits-and-retailers-struggle-to-adapt-11553511602?mod=trending_now_3"
		
		# page = requests.get((link))
		print(browser.current_url)
		soup = BeautifulSoup(browser.page_source, 'lxml') #html.parser')
		images, date = getImagesandDate(1, soup, sys.argv[1])
		print(date, len(images))
		print()
		print('\n'.join(map(str, images)))

		time.sleep(10)
		browser.get(link1)
		print(browser.current_url)
		soup = BeautifulSoup(browser.page_source, 'lxml') #html.parser')
		images, date = getImagesandDate(1, soup, sys.argv[1])
		print(date, len(images))
		print()
		print('\n'.join(map(str, images)))

		browser.quit()

	elif(len(sys.argv) > 2 and sys.argv[2] == "filter"):
		main(1)
	else:
		main(0)