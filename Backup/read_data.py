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
		return None
	except:
		return None

def main():
	files = [f for f in listdir((mypath + "input")) if isfile(join((mypath + "input"), f))]

	stats = open("Stats.txt", "a")
	print("\n\n" + str(datetime.datetime.now()) + "\n", file=stats)
	print('%-40s %-10s %-10s %-10s %-10s' % ("News Org", "Input", "RTs", "NoLinks", "Output"), file=stats)
	for f in files:
		raw_data = []
		data = []
		with open(mypath + "input/" + f, mode='r') as inptr:
			reader = csv.reader(inptr)
			for row in reader:
				raw_data.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11]])
			
			data = filterRT(raw_data)
			numReTweets = len(raw_data) - len(data)
			data = filterNonHTTPS(data)
			numWithoutHTTPS = len(raw_data) - numReTweets - len(data)

			print('%-40s %-10s %-10s %-10s' % (f, len(raw_data), numReTweets, numWithoutHTTPS), end='', file=stats)
		
		with open(mypath + "output/Filtered" + f, mode='w', encoding="utf-8") as outptr:
			writer = csv.writer(outptr, dialect='excel', delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			writer.writerow(["Index", "ID", "User_ID", "Friends_Count", "Favourites_Count", "Listed_Count", "Status_Count", "Created_at", "Retweet_Count", "Favourite_Count", "Created_at", "Text"])
			for i in range(len(data)):
				row = data[i]
				writer.writerow([i+1, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11]])
			
		with open(mypath + "output/Result" + f, mode='w', encoding="utf-8") as outptr:
			writer = csv.writer(outptr, dialect='excel', delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			writer.writerow(["Index", "Publisher", "URL", "Date", "Num_Images", "Caption", "Credit/Source"]);
			article_index = 0; twitter = 0; broken = 0; 

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

						if(page.url.find("twitter.com") != -1):
							twitter += 1
							news_link = getTwittertoNewsLink(page.url)
							if(news_link == None):
								break

							page = requests.get(news_link)

						# if page doesn't exists
						if(page.ok == False):
							broken += 1
							break;

						# Find images
						soup = BeautifulSoup(page.text, 'html.parser')
						images, date = getImagesandDate(soup, f[:f.find(".out")])
						
						article_index += 1		
						flag = True		
						if(len(images) == 0):
							writer.writerow([i+1, f[:f.find(".out")], page.url, date, len(images),"NA", "NA"])

						for img_num in range(min(CONST_MAX_IMG, len(images))):
							if(img_num == 0):
								writer.writerow([i+1, f[:f.find(".out")], page.url, date, len(images), "NA" if(images[img_num][0] == "") else images[img_num][0], "NA" if(images[img_num][1] == "") else images[img_num][1]])
							else:
								writer.writerow([i+1, f[:f.find(".out")], "", "", len(images), "NA" if(images[img_num][0] == "") else images[img_num][0], "NA" if(images[img_num][1] == "") else images[img_num][1]])
				except Exception as e:
					print("Skipped one Article" + str(e))
					
		print(' %-10s' % (article_index), file=stats)
	stats.close()


def getImagesandDate(soup, org):	
	images = []
	date = ""

	try:
		if(org == "USATODAY"):
			dates = soup.find_all('span', {'class' : 'asset-metabar-time asset-metabar-item nobyline'})
			date = (''.join(date.get_text() for date in dates)).lstrip()
			
			raw_images = soup.find_all('div', {'class' : 'story-asset image-asset'})
			if raw_images == None:
				return images, date

			for image in raw_images:
				if(image.find('p') != None):
					p = image.find('p')
					credit = p.find('span', {'class' : 'credit'})
					credit = "" if (credit == None) else credit.get_text() 
					images.append([p.get_text(), credit])

				if(len(images) >= CONST_MAX_IMG):
					break

		# Not Implemented
		if(org == "WSJ"):
			dates = soup.find_all('time')
			date = (''.join(date.get_text() for date in dates)).lstrip()				
			
			return [], date

		if(org == "latimes"):
			dates = soup.find_all('span', {'class' : 'timestamp-article'})
			date = (''.join(date.get_text() for date in dates)).lstrip()
			
			all_captions = soup.find_all('figcaption')
			for caption in all_captions:
				tmp = caption.find('div').get_text()

				images.append([tmp, "" if(tmp.find("(") == -1) else tmp[tmp.find("("):]])
				if(len(images) >= CONST_MAX_IMG):
					break

		if(org == "chicagotribune"):
			date = soup.find('time', {'itemprop':'datePublished'})
			date = date['data-dt'] + " " + date['datetime']

			all_images = soup.find_all('div', {'class': 'trb_em_r'})
			for image in all_images:
				cc = image.find('div', {'class':'trb_em_r_ca'}).find('p')
				cr = image.find('div', {'class':'trb_em_r_cr'})
				images.append(["" if(cc == None) else cc.get_text(), "" if(cr == None) else cr.get_text()])
				if(len(images) >= CONST_MAX_IMG):
					break

		if(org == "nypost"):
			dates = soup.find_all('p', {'class': 'byline-date'})
			date = (''.join(date.get_text() for date in dates)).lstrip()
			
			all_captions = soup.find_all(class_="wp-caption-text")
			for caption in all_captions:
				cc = caption.find('span')
				cr = caption.find('span', {'class': 'credit'})
				images.append(["" if(cc == None) else cc.get_text(), "" if(cr == None) else cr.get_text()])
				if(len(images) >= CONST_MAX_IMG):
					break

		if(org == "washingtonpost"):
			date = soup.find('span', {'itemprop': 'datePublished'})['content']

			all_captions = soup.find_all('span', {'class':'pb-caption'})
			for caption in all_captions:
				cr_start = caption.get_text().find('(')
				cc = caption.get_text()[:cr_start]
				cr = "" if(cr_start == -1) else caption.get_text()[cr_start:]
				images.append([cc, cr])
				if(len(images) >= CONST_MAX_IMG):
					break

		if(org == "Newsday"):
			date = soup.find('time', {'itemprop': 'datePublished'})['datetime']

			all_captions = soup.find_all(class_="mediaCell")
			print(all_captions)
			for caption in all_captions:
				tmp = caption.find('div', {'class':'video'})
				if(tmp != None and len(tmp) != 0):
					break

				caption = caption.find('p', {'class':'caption'})	
				cr_start = caption.get_text().find('Photo Credit:')
				cc = caption.get_text()[:cr_start].lstrip().rstrip()
				cr = "" if(cr_start == -1) else caption.get_text()[cr_start+len('Photo Credit:'):].rstrip().lstrip()
				images.append([cc, cr])
				if(len(images) >= CONST_MAX_IMG):
					break


		# misc = open("a.html", "w")
		# print(soup.get_text(), file = misc)
		# misc.close()

		return images, date

	except Exception as e:
		print(str(e))
		return images, date

if __name__ == '__main__':
	main()
	# link = "https://www.newsday.com/travel/long-island-getaways/hamptons-inns-bedside-reading-weekend-1.26393562?utm_source=tw_nd"
	# page = requests.get(link)
	# soup = BeautifulSoup(page.text, 'html.parser')
	# images, date = getImagesandDate(soup, "Newsday")
	# print(date, images)
