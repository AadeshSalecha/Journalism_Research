import datetime
from os import listdir
from os.path import isfile, join
import requests
from bs4 import BeautifulSoup
import csv
import re
import sys 

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

def main():
	files = [f for f in listdir((mypath + "input")) if isfile(join((mypath + "input"), f))]

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

			with open(mypath + "input/" + f, mode='r') as inptr:
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
								if(org_name == "nypost" and page.url.find("pagesix") != -1):
									pass
								elif(org_name == "starledger" and page.url.find("nj") != -1):
									pass
								else:
									numWithoutHTTPS += 1
									print("\t\t\t\t" + org_name + " tried accessing " + page.url + " originally was " + link)
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


def getImagesandDate(id, soup, org):	
	images = []
	date = ""
	org = org.lower()

	try:				
		if(org == "starledger"):
			date = soup.find('time')['datetime']

			all_images = soup.find_all('figure')
			for image in all_images:
				cc = image.find('figcaption')
				cr = cc.find('cite') if(cc != None) else None

				images.append(["" if(cc == None) else cc.get_text().rstrip().lstrip(), "" if(cr == None) else cr if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()])
				if(len(images) >= CONST_MAX_IMG):
					break
		
		# misc = open("b.html", "w")
		# print(soup.prettify(), file = misc)
		# misc.close()

	except Exception as e:
		print("Exception in scrape " + str(id) + " " + org + " " + str(e))
		return [], ""

	return images, date

if __name__ == '__main__':
	main()
	# link = "https://www.nj.com/opinion/index.ssf/2019/02/im_afraid_of_donald_trumps_taxes_sheneman_cartoon.html?utm_medium=social&utm_source=twitter&utm_campaign=starledger_sf&utm_content=nj_starledger_twitter"
	# page = requests.get((link))
	# soup = BeautifulSoup(page.text, 'html.parser')
	# images, date = getImagesandDate(1, soup, "starledger")
	# print(date, len(images))
	# print()
	# print('\n'.join(map(str, images)))