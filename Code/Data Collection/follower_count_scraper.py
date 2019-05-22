import csv
from os import listdir
from os.path import isfile, join
import time
import os
import urllib
from urllib.request import urlopen, Request
import lxml.html
from bs4 import BeautifulSoup

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

orgs = ["ohiodotcom", "abqjournal", "amnewyork", "azcentral", "arkansasonline", "asburyparkpress ", "ajc", "statesman", "toledonews", "bostonglobe", "bostonherald", "thebuffalonews", "theobserver", "suntimes", "chicagotribune", "enquirer", "dispatchalerts", "memphisnews", "courierjournal", "dailyherald", "nydailynews", "Dallasnews", "daytondailynews", "dbnewsjournal ", "dandc", "dmregister", "deseretnews", "freep", "owhnews", "jaxdotcom ", "startelegram", "hartfordcourant", "staradvertiser", "indystar", "kcstar", "knoxnews", "reviewjournal", "latimes", "journalsentinel", "mcall", "ndn ", "nypost", "nytimes", "newsobserver", "thenewspress ", "newsday", "theoklahoman", "owhnews", "ocregister", "orlandosentinel", "phillyinquirer", "pittsburghpg", "Theplaindealer", "projo", "sacbee_news", "expressnews", "sfchronicle", "heraldtribune ", "seattletimes", "sunsentinel", "spokesmanreview", "stltoday", "pioneerpress", "startribune", "tb_times", "tennessean", "baltimoresun", "denverpost", "detroitnews", "mercnews", "miamiherald", "delawareonline ", "pbpost", "sltrib", "sdut", "starledger", "triblive", "usatoday", "virginianpilot", "wsj", "washingtonpost", "wistatejournal"]

def extract_follower_counts(org):
  link = "https://mobile.twitter.com/" + org
  req = Request(link, headers=headers)
  page = urlopen(req)
  soup = BeautifulSoup(page.read(), 'lxml')

  try:
    stats = soup.find_all('div', {'class':'statnum'})
    num_followers = int(stats[2].get_text().replace(',', '')) 
    num_followees = int(stats[1].get_text().replace(',', '')) 
    return (num_followees, num_followers)
  except:
    print("Error on ", org)
    misc = open("a.html", "w")
    print(soup.prettify(), file = misc)
    misc.close()
    return (0, 0)

def printPage(page, name):
  
  if not os.path.exists('ErrorFiles/'):
    os.makedirs('ErrorFiles')
  misc = open("ErrorFiles/" + name + ".html", "w")
  print(soup.prettify(), file = misc)
  misc.close() 

d = {}
def main():
  global orgs
  orgs = [org.lower() for org in orgs]
  for org in orgs:
    d[org] = []


  files = [f for f in listdir("/home/salec006/Research/Code/Data Collection/Filtered/") if isfile(join("/home/salec006/Research/Code/Data Collection/Filtered/", f))]
  
  for f in files: 
    with open("./Filtered/" + f, mode='r') as inptr:
      reader = csv.reader(inptr) 
      next(reader)
      row = next(reader)     

      if(f[len("Filtered"):f.find(".out")].lower() in d):
        d[f[len("Filtered"):f.find(".out")].lower()].append([int(row[3]), int(row[4])])

  # for org in orgs:
  #   tmp = extract_follower_counts(org)
  #   d[org].append([tmp[0], tmp[1]])
  #   time.sleep(1)

  for org in sorted(d.keys()):
    print(org, d[org])

if __name__=="__main__":
  main()