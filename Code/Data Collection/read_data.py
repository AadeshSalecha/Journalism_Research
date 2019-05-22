'''

 Opens twitter link, scrapes link from tweet, 
 opens article and scrapes
 
 @author  Aadesh Salecha (salec006@umn.edu)
 @version 1.0
 @since   21.05.2019
 
'''

import time
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

			with open(mypath + "output/Result" + f, mode='w', encoding="utf-8") as outptr:
				writer = csv.writer(outptr, dialect='excel', delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
				writer.writerow(["Index", "Publisher", "URL", "Date", "Num_Images", "Caption", "Credit/Source"]);
				org_name = f[:f.find(".out")].lower()

				for i in range(len(data)):
					row = data[i]
					links = re.findall(r'(https?://\S+)', row[CONST_DATA_COL])
					flag = False

					if(i % 10 == 0):
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
								if(org_name == "memphisnews" and page.url.find("commercialappeal") != -1):
									pass
								
								else:
									numWithoutHTTPS += 1
									print("                " + org_name + " tried accessing " + page.url + " originally was " + link)
									break

							# Find images
							soup = BeautifulSoup(page.text, 'html.parser')
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
		
		except Exception as e:
			print("Tried reading " + f + " file, something went wrong " + str(e))


def extractImage(all_images, images):
	while(all_images.find('"credit":') != -1):
		cr_start = all_images.find('"credit":') + len('"credit":')
		cr = all_images[cr_start:all_images.find('"caption"', cr_start+1)].lstrip().rstrip()
		cc_start = all_images.find('"caption":') + len('"caption":')
		cc = all_images[cc_start:all_images.find('"myCapture"', cc_start+1)].lstrip().rstrip()
		cr = "" if(cr.translate(str.maketrans('', '', string.punctuation)) == '') else cr
		cc = "" if(cc.translate(str.maketrans('', '', string.punctuation)) == '') else cc

		cc = cc if(cc.find('"rowend":') == -1) else cc[:cc.find('"rowend":')]
		if(cr == ""):
			cr = cc[cc.rfind('['):] if(cc.rfind('[') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else ""

		all_images = all_images[all_images.find('"myCapture', cc_start+1)+1:]
		images.append([cc, cr])
		if(len(images) >= CONST_MAX_IMG):
			break

def getImagesandDate(id, soup, org):	
	images = []
	date = ""
	org = org.lower()

	try:
		

		

		# misc = open("a.html", "w")
		# print(soup.prettify(), file = misc)
		# misc.close()

	except Exception as e:
		print("Exception in scrape " + str(id) + " " + org + " " + str(e))
		return [], ""

	return images, date

if __name__ == '__main__':
	if(len(sys.argv) > 2 and sys.argv[2] == "test"):
		link = "https://www.omaha.com/momaha/reasons-why-winter-is-the-worst-season-when-you-have/article_2f3c7a5f-b0db-5128-8739-c683d1033a46.html"
		page = requests.get((link))
		soup = BeautifulSoup(page.text, 'lxml') #html.parser')
		images, date = getImagesandDate(1, soup, sys.argv[1])
		print(date, len(images))
		print()
		print('\n'.join(map(str, images)))

	elif(len(sys.argv) > 2 and sys.argv[2] == "filter"):
		main(1)
	else:
		main(0)