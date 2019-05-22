'''

 Script to go through Result data
 and mark Professional and Citizen Sources
 and calculate total number of P, C, unmarked, nocredit

 It also removes duplicate, and also changes max 10 images
 
 @author  Aadesh Salecha (salec006@umn.edu)
 @version 1.0
 @since   21.05.2019
 
'''

import re
import sys 
import csv
import string
from os import listdir
from os.path import isfile, join


mypath = "/home/salec006/Research/Data/"

proSources = ['Associated Press', "gucci", "krispy kreme", "marvel", "doritos", ".gov", "Daily camera", "denver7", "adobe", "cinemax", "universal studios", "universal pictures", "red bull", "airbnb", "star-advertiser", "fresnobee", "modbeeyelp", "patriots", 'labratory', 'Bloomberg', 'Reuters', 'Fox News', 'Getty', 'Shutterstock', 'iStock', 'Gazette', 'daytondailynews', 'dayton daily', 'hartfordcourant', 'hartford courant', 'DispatchAlerts', 'Dispatch Alerts', 'Tennessean', 'detroitnews', 'detroit news', 'theobserver', 'the observer', 'ohiodotcom', 'akron beacon journal', 'ohio.com', 'dallasnews', 'dallas news', 'courierjournal', 'courier-journal', 'chicagotribune', 'chicago tribune', 'DMRegister', 'Des Moines Register', 'StarAdvertiser', 'Star Advertiser', 'startelegram', 'star telegram', 'projo', 'Providence Journal', 'Enquirer', 'denverpost', 'denver post', 'PittsburghPG', 'Pittsburgh Post-Gazette', 'starledger', 'star ledger', 'ocregister', 'Orange County Register', 'bostonherald', 'boston herald', 'azcentral', 'Arizona Republic', 'reviewjournal', 'review journal', 'review-journal', 'baltimoresun', 'baltimore sun', 'nytimes', 'New York Times', 'Suntimes', 'Sun times', 'sltrib', 'Salt Lake Tribune', 'ArkansasOnline', 'Arkansas Online', 'Wall Street Journal', 'Wall-Street Journal', 'MiamiHerald', 'Miami Herald', 'DeseretNews', 'Deseret News', 'ABQJournal', 'Alburquerque Journal', 'USATODAY', 'USA Netw', 'USA Network', 'WaPoExpress', 'mcall', 'Morning Call', 'stltoday', 'St. Louis Post-Dispatch', 'Post-Dispatch', 'freep', 'Detroit Free press', 'toledonews', 'toledo news', 'amNewYork', 'New York City News', 'WiStateJournal', 'Wisconsin State Journal', 'Newsday', 'PioneerPress', 'Pioneer Press', 'sacbee', 'Sacramento Bee', 'washingtonpost', 'Washington Post', 'latimes', 'Los Angeles Times', 'KCStar', 'Kansas City Star', 'DandC', 'Democrat and Chronicle', 'Democrat & Chronicle', 'dbnewsjournal', 'Daytona Beach News', 'SunSentinel', 'Sun Sentinel', 'OWHnews', 'Omaha World', 'sfchronicle', 'San Francisco Chronicle', 'virginianpilot', 'virginian pilot', 'SpokesmanReview', 'Spokesman Review', 'StarTribune', 'Star Tribune', 'memphisnews', 'memphis news', 'dailyherald', 'daily herald', 'Sand Diego Union', 'delawareonline', 'delaware', 'statesman', 'TheBuffaloNews', 'Buffalo News', 'AsburyParkPress', 'Asbury Park Press', 'mercnews', 'mercury news', 'TribLIVE', 'TheNewsPress', 'News Press', 'HeraldTribune', 'Herald Tribune', 'NYDailyNews', 'NY Daily', 'orlandosentinel', 'orlando sentinel', 'PhillyInquirer', 'Philly Inquirer', 'TheOklahoman', 'The Oklahoman', 'tampabay', 'nypost', 'jaxdotcom', 'Florida Times', 'knoxnews', 'indystar', 'pbpost', 'Palm Beach Post', 'BostonGlobe', 'Boston Globe', 'PlainDealer', 'Plain Dealer', 'newsobserver', 'news observer', 'journalsentinel', 'journal sentinel', 'seattletimes', 'seattle times', 'ExpressNews', 'Express News', 'Archive', 'Wireimage', 'European press photo', 'yakima herald-republic', 'yakima herald republic', 'Southern California news', 'contra costa times', 'walla walla union', 'daily pilot', 'santa cruz sentinel', 'winnipeg free press', 'daily breeze', 'United press international', 'press-enterprise', 'kdka-tv', 'knxv-tv', 'wcpo-tv', 'Tribune News', 'Kaiser Health News', 'courant.com', 'The Courant', 'daily news', 'daily-news', 'daily commercial', 'post-gazette', 'blade', 'palmbeachpost.com', 'dispatch', 'houston chronicle', 'tribune', 'the world', 'inverstigation discovery', 'south florida sun-sentinel', 'thisweek', 'kgun9', 'the cw', 'augusta chronicle', 'bravo', 'national geographic', 'recode', 'chicago sun-times', 'philadelphia inquirer', 'herald', 'waterloo-cedar falls courier', 'atlanta journal-constitution', 'atlanta journal constitution', 'albuquerque journal', 'fayetteville observer', 'animal planet', 'arizona daily star', 'magazine', 'honolulu star-advertiser', 'c-span', 'cq roll call', 'usa today sports', 'boulder city review', 'spokesman-review', 'correspondent', 'thinkstock', 'agence france-presse', 'alamy stock', 'library of congress prints', 'national archives', 'records administration', 'sundance institute', 'pittsburgh cultural trust', 'united way of salt lake', 'promedica', 'wikimedia', 'change the ref', 'change.org', 'google maps', 'google street ', 'university ', 'seton hill', 'seton hall', 'school', 'college', 'academy', 'annapurna pictures', 'hospitality group', 'amazon', 'apple', 'chase', 'longview power', 'public relations', 'filevine', 'aurora innovation', 'tiffany and co', 'tiffany &', 'in tune partners', 'jon kohler & associates', 'jon kohler and associates', 'nintendo', 'brewing', 'loloi ', 'architect', 'pepsi', 'foundation', 'resort skiplagged', 'vade secure', 'weisshouse', 'aerion', 'airline', 'clinic', 'auster agency', 'boka powell', 'nomad las vegas', 'colgate', 'bud light ', 'bulletproof', 'bumble ', 'caesars entertainment', 'coca-cola', 'trader joe', 'tripadvisor', 'app in the air', "george washington's mount veron", 'animal planet', 'freeform', 'channel', 'bachelor of provo', 'netflix', 'comedy', 'brewery', 'heather likes food', 'greek gourmet', 'century fox', 'theatre', 'drafthouse', 'sony pictures classics', 'warner bros', 'disney', 'elysium film', 'marvel studios', 'hollywood pictures', 'paramount pictures', 'lucas film', 'pixar', 'annapurna pictures', 'penndot', 'real estate', 'pool kremlin', 'kremlin pool', 'david bachman', 'katelyn bell', 'rex features', 'pdnb gallery', 'stanley photography', 'chanel jaali', 'libbyvision', 'benoit photo', 'two and two photography', 'blazer + bray', 'allegheny county jail', 'audubon society of western pennsylvania', 'bloomsbury', 'art center', 'institute of arts', 'invision', 'gofundme', 'carnegie museum', 'brookings ', 'healthcare', 'football', 'basketball', 'athletics', 'crew sc', 'new england patriots', 'cleveland monsters', 'oungstown phantoms', 'minnesota twins', 'allsport', 'kennywood', 'norah jones', 'sammy hagar & the circle', 'pennsylvania ', 'utah ', 'pittsburgh', 'nevada', 'chicago', 'california', 'atlanta', 'columbia', 'texas', 'dreamstime', 'everyday jenny', 'cooking with karli', 'your cup of cake', 'emojipedia', 'salt & Baker', 'salt and baker', 'dessert now dinner later', 'friends of cedar mesa', 'unsplash', 'mgn online', 'adobe stock', 'bigstock', 'misra records', 'archive', 'macmillan', 'terrace plaza playhouse', 'mote marine', 'seneca anti-wind', 'stock image', 'the white house', 'navy ', 'airnow.gov', 'blue rider', 'republic of mexico', 'brightline', 'pictorial directory', 'caltrans', 'capital weather gang', 'international center of photography', 'coast guard', 'correctionsusa', 'broadway', 'camino real playhouse', 'caprock partners', 'casa romantica', 'costar', 'international', 'cushman & wakefield', 'american', 'record', 'bureau', 'institution', 'alive', 'project', 'library', 'obituary', 'church', 'business', 'group', 'center', 'clinic', 'prison', 'police', 'studio', 'service', 'construction', 'foundation', 'clothing', 'hotel', 'performance', 'cooking', 'company', 'association', 'journal', 'press ', 'times', 'media', 'register', 'the star', 'the southern', 'uw-madison', 'wcfcourier', 'indianapolis star', 'columbus clippers', 'tennesse', 'Indy_star', 'fresno bee', 'flight photo agency', 'page six', 'the republic', 'Virginian-Pilot', 'The Commercial Appeal', 'New York Post', 'star-telegram', 'staradvertiser', 'entertainment', 'county', 'ANNAPURNA', 'observer', 'virginianpilot', 'Kstp-tv', 'staff', 'sherif', 'company', 'restaurant', 'division', 'department', 'museum', 'sports', 'hospital', 'state', 'country', 'artist', 'painter', 'USA today', 'the chronicle', 'institute', 'council', 'Google']
companies = ['AP', "SCNG", "EPA", "TCF", "NYT", "NCPD", "NYPD", "MTV", "FBI", 'mgm', 'CBS', 'NBC', 'ABC', 'WSJ', 'ajc', 'sdut', 'ndn', 'File', 'EPA', 'fox', 'pbs', 'scng', 'UPI', 'ktla', 'tns', 'bbc', 'cnn', 'wwe', 'tnt', 'bcso', 'mit ', 'unlv', 'ucla', 'sony', 'amd', 'hbo', 'hulu', 'unlv', 'nba', 'nfl', 'nasa', 'cdfw', 'cbre', 'apd', 'ice', 'gao', 'cbp', 'cdc', 'cfi', 'cwg', 'cnp', 'law', 'zoo', 'amc', 'film', 'inn', 'bell', 'co.', 'firm', 'inc.', 'news', 'UCSD', 'bcso', 'Sept', 'book', 'jail', 'city', 'Noaa']
citizenSources = ["contributed", "flickr", "twitter", "handout", "facebook", "contributed", "instagram", "family", "publicdomainpictures", "public domain", "reddit", "youtube", "submitted ", "black lives matter"]
allMarkedSources = {}
companies = list(set([tmp.lower().lstrip().rstrip() for tmp in companies]))
proSources = list(set([tmp.lower().lstrip().rstrip() for tmp in proSources]))
citizenSources = list(set([tmp.lower().lstrip().rstrip() for tmp in citizenSources]))
top70 = ["tampabay", "ABQJournal", "ajc", "amNewYork", "ArkansasOnline", "azcentral", "baltimoresun", "BostonGlobe", "bostonherald", "chicagotribune", "courierjournal", "dailyherald", "dallasnews", "DandC", "daytondailynews", "denverpost", "DeseretNews", "detroitnews", "DispatchAlerts", "DMRegister", "Enquirer", "ExpressNews", "freep", "hartfordcourant", "indystar", "journalsentinel", "KCStar", "knoxnews", "latimes", "mcall", "mercnews", "MiamiHerald", "Newsday", "newsobserver", "NYDailyNews", "nypost", "nytimes", "ocregister", "orlandosentinel", "OWHnews", "pbpost", "PhillyInquirer", "PioneerPress", "PittsburghPG", "reviewjournal", "sacbee_news", "sdut", "seattletimes", "sfchronicle", "sltrib", "SpokesmanReview", "StarAdvertiser", "starledger", "startelegram", "StarTribune", "statesman", "stltoday", "SunSentinel", "Suntimes", "TB_Times", "Tennessean", "TheBuffaloNews", "theobserver", "TheOklahoman", "ThePlainDealer", "toledonews", "TribLIVE", "USATODAY", "virginianpilot", "WaPoExpress", "washingtonpost", "WiStateJournal", "WSJ"]

first = True

def isCompany(toCheck):
	toCheck = " " + toCheck.lower() + " "
	if(toCheck[-3:] == "ap "):
		return "Professional - AP"

	for s in companies:
		if(re.findall(re.compile(('[,/().,\n\t";\[ ](' + s + ')[,/()\n\t.,";\] ]')), toCheck) != []):
			return "Professional - " + s
	return 'Unknown'
	
def allstrip(st, strL, strL1):
	s = st
	for c in strL:
		s = s.lstrip(c).rstrip(c)
	for t in strL1:
		if(s.find(t) == 0):
			s = s[len(t):]

	return s

def unknownPart(toCheck):
	toCheck = allstrip(toCheck, [" ", "\"", "(", ")", '[', ']'], ["photo:", "photo", 'author":"', '","credit":null,"'])
	for mSource in allMarkedSources:
		if(toCheck in mSource):
			return allMarkedSources[mSource]
	return "Unknown"

def notFinished(toCheck):		
	global first
	global proSources

	toCheck = toCheck.lower()
	if(isCompany(toCheck) != 'Unknown'):
		return isCompany(toCheck)
		
	for proS in proSources:
		if(toCheck.find(proS) != -1):
			return "Professional - " + proS		

	for proS in citizenSources:
		if(toCheck.find(proS) != -1):
			return "Citizen - " + proS		

	return unknownPart(toCheck)
	
def generateTotalTweets():
	files = [f for f in listdir((mypath + "final_output/Filtered")) if isfile(join((mypath + "final_output/Filtered"), f))]

def main():
	files = [f for f in listdir((mypath + "final_output/Result")) if isfile(join((mypath + "final_output/Result"), f))]
	duplicate_data = []
	totalSources_list = {}
	finishedtotList = {}
	totalSources = 0
	stats = []
	
	# print("Org, Total Tweets, RTs, NoLinks, Output, #Articles")
	
	# try:
	for f in files:
		articles = {}

		# Read in file and remove duplicates
		with open(mypath + "final_output/Result/" + f, mode='r') as inptr:
			reader = csv.reader(inptr)
			data = []
			for row in reader:
				data.append(row)

			# Ignore first line
			i = 1
			while(i < len(data)-3):
				row = data[i]
				index = row[0]; org = row[1]; url = row[2]; date = row[3]; num_images = int(row[4]); cc = row[5]; cr = row[6];

				# New article starts
				# if article doesn't exist
				if(url not in articles):
					if(num_images > 10):
						tmp_article = [[index, org, url, date, 10, cc, cr]]						
					else:
						tmp_article = [[index, org, url, date, num_images, cc, cr]]
					
					for tmp_i in range(max(0, min(9, int(num_images)-1))):
						i += 1
						if(len(tmp_article) < 10):
							if(num_images > 10):
								data[i][4] = 10
							tmp_article.append(data[i])
					
					# total_images += data[i][4]
					articles[url] = tmp_article				
				else:
					for tmp_i in range(max(0, min(9, int(num_images)-1))):
						i += 1
				i += 1

			# print(f)
			num_input = (data[-1][0].split()[4])
			total_tweets = (data[-1][0].split()[1])
			rts = (data[-1][0].split()[2])
			nolinks = (data[-1][0].split()[3])
			# print(f, total_images) #total_tweets, rts, nolinks, num_input, end='', sep = ',')

		all_sources = {}
		f = f[f.find("Result") + len('Result'):]
		printed = True
		with open(mypath + "final_output/Rem_dup/RemDup_" + f, mode='w', encoding="utf-8") as outptr:
			writer = csv.writer(outptr, dialect='excel', delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			writer.writerow(["Index", "Publisher", "URL", "Date", "Num_Images", "Caption", "Credit/Source"]);			
			
			total_images = 0
			for data in articles.values():
				total_images += int(data[0][4])

				for row in data:
					if((row[6] == "NA" or row[6].translate(str.maketrans('', '', string.punctuation)) == "")):
						if(row[4] != 0):
							row[6] = "No Credit"
						else:
							row[6] = "No Image"

					if(notFinished(row[6]) == 'Unknown'):
						totalSources_list[row[6]] = 1
					else:
						finishedtotList[row[6]] = notFinished(row[6])

					if(row[6] in all_sources):
						all_sources[row[6]] += 1
					else:
						all_sources[row[6]] = 1
					writer.writerow(row)

			# if(f[:f.find('.out')].lower() in top70):
				# print(f[:f.find('.out')], total_images)
			writer.writerow(['Number of articles in this file: ', len(articles)])			
			writer.writerow(['Number of duplicate articles removed: ', int(num_input) - len(articles)])
			duplicate_data.append(f[:f.find('.out')] + "    " + str(int(num_input) - len(articles)))
			# print(" " + str(len(articles)) + ", " + total_images)

		blank = "                              "
		citizen = 0; professional = 0; unmarked = 0; noImg = 0; noCredit = 0;
		with open(mypath + "final_output/Source/Source_" + f, mode='w', encoding="utf-8") as outptr:
			writer = csv.writer(outptr, dialect='excel', delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			writer.writerow(["Index", "Source", "P/C", "", "", "", "Count"])

			index = 1
			source_list = all_sources.keys()
			for source in source_list:
				if(notFinished(source) == "Unknown"):
					writer.writerow([index, source, blank, "", "", "", all_sources[source]])
				else:
					writer.writerow([index, source, notFinished(source), "", "", "", all_sources[source]])

				tmp = notFinished(source)
				if(source == "No Image"):
					noImg += all_sources[source]
				elif(source == "No Credit"):
					noCredit += all_sources[source]
				elif("Citizen" in tmp):
					citizen += all_sources[source]
				elif("Professional" in tmp):
					professional += all_sources[source]
				else:
					unmarked += all_sources[source]
				index += 1
			totalSources += index

			# writer.writerow([])
			# writer.writerow(["Citizen", "Professional", "Unknown"])
			# writer.writerow([citizen, professional, unmarked])
			total = citizen + professional + noCredit + unmarked
			stats += [(f, [professional, citizen, unmarked, noImg, noCredit, total])]

	with open(mypath + "final_output/Source/All_Sources.csv", mode='w', encoding="utf-8") as outptr:
		writer = csv.writer(outptr, dialect='excel', delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		writer.writerow(["Index", "Source", "P/C"])

		index = 1
		for source in finishedtotList:
			writer.writerow([index, source, finishedtotList[source]])
			index += 1

		for source in totalSources_list:
			writer.writerow([index, source, blank])
			index += 1

	blank = "                              "	
	with open("Marked_All_Sources.csv", mode='w', encoding="utf-8") as outptr:
		writer = csv.writer(outptr, dialect='excel', delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		writer.writerow(["Index", "Source", "P/C"])

		index = 1
		for source in finishedtotList:
			allMarkedSources[source.lower()] = finishedtotList[source]
			writer.writerow([index, source, finishedtotList[source]])
			index += 1

	with open("Not_Marked_Sources.csv", mode='w', encoding="utf-8") as outptr:
		writer = csv.writer(outptr, dialect='excel', delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		writer.writerow(["Index", "Source", "P/C"])
		
		index = 1
		for source in totalSources_list:
			writer.writerow([index, source, blank])
			index += 1
	print(stats)

# We run it twice because we want to build dictionary
if __name__ == '__main__':
	main()
	main()