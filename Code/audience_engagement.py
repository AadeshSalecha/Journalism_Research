'''

 Script to calculate audience engagement scores 
 from Filtered data
 
 @author  Aadesh Salecha (salec006@umn.edu)
 @version 1.0
 @since   21.05.2019
 
'''

import sys 
import csv
from os import listdir
from os.path import isfile, join

mypath = "/home/salec006/Research/Data/"
files = [f for f in listdir((mypath + "final_output/Filtered")) if isfile(join((mypath + "final_output/Filtered"), f))]

new_files = []
if(len(sys.argv) > 1):
	for i in range(1, len(sys.argv)):
		if("Filtered" + sys.argv[i] + ".out.csv" in files):
			new_files.append("Filtered" + sys.argv[i]+".out.csv")
	files = new_files

print()
print("News Org", "No. of Likes", "No. of Retweets", "No. of Tweets (no RTs)", "No. Followers", " ", "Likes", "Retweets", sep=',')
for f in files:	
	filteredData = []

	likes = 0; retweets = 0; num_followers = 0;
	first = True;
	with open(mypath + "final_output/Filtered/" + f, mode='r') as inptr:
		reader = csv.reader(inptr)
		for row in reader:
			if(first):
				first = False
				continue
			# Index	ID	User_ID	Friends_Count	Followers_Count	Favourites_Count	Listed_Count	Status_Count	Created_at	Retweet_Count	Favourite_Count	Created_at	Text
			filteredData.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12]])
			# print([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12]])
			retweets += int(row[9])
			likes += int(row[10])
			num_followers = int(row[4])

	aud_likes = (likes) / (len(filteredData) + num_followers)
	aud_retweets = (retweets) / (len(filteredData) + num_followers)

	print(f[len('Filtered'):f.find(".out")], likes, retweets, len(filteredData), num_followers, " ", aud_likes, aud_retweets, sep=', ')		