
	#########################################
	#########################################
	#########################################
	#
	#			DOMAIN NAMES
	#
	#########################################
	#########################################
	#########################################
	
	elif(org_name == "asburyparkpress" and page.url.find("app.com") != -1):
		pass
	elif(org_name == "ndn" and page.url.find("naplesnews.com") != -1):
		pass
	elif(org_name == "thenewspress" and page.url.find("news-press.com") != -1):
		pass
	elif(org_name == "dandc" and page.url.find("democratandchronicle.com") != -1):
		pass
	elif(org_name == "pbpost" and page.url.find("palmbeachpost.com") != -1):
		pass
	elif(org_name == "dmregister" and page.url.find("desmoinesregister.com") != -1):
		pass
	elif(org_name == "ohiodotcom" and page.url.find("ohio.com") != -1):
		pass
	elif(org_name == "projo" and page.url.find("providencejournal.com") != -1):
		pass
	elif(org_name == "jaxdotcom" and page.url.find("jacksonville.com") != -1):
		pass	
	elif(org_name == "dbnewsjournal" and page.url.find("news-journalonline.com") != -1):
		pass	
	elif(org_name == "toledonews" and page.url.find("toledoblade.com") != -1):
		pass
	elif(org_name == "theoklahoman" and page.url.find("oklahoman") != -1):
		pass
	elif(org_name == "owhnews" and page.url.find("omaha") != -1):
		pass
	elif(org_name == "spokesmanreview" and page.url.find("spokesman") != -1):
		pass
	elif(org_name == "wistatejournal" and page.url.find("madison.com") != -1):
		pass
	elif(org_name == "tb_times" and page.url.find("tampabay.com") != -1):
		pass
	elif(org_name == "phillyinquirer" and page.url.find("philly") != -1):
		pass
	elif(org_name == "amnewyork" and page.url.find("amny") != -1):
		pass
	elif(org_name == "theplaindealer" and page.url.find("cleveland") != -1):
		pass
	elif(org_name == "houstonchron" and page.url.find("chron") != -1):
		pass
	elif(org_name == "pioneerpress" and page.url.find("twincities") != -1):
		pass
	elif(org_name == "sdut" and page.url.find("sandiegouniontribune") != -1):
		pass
	elif(org_name == "kcstar" and page.url.find("kansascity") != -1):
		pass
	elif(org_name == "oregonian" and page.url.find("oregon") != -1):
		pass
	elif(org_name == "hartfordcourant" and page.url.find("courant") != -1):
		pass
	elif(org_name == "mercnews" and page.url.find("mercurynews") != -1):
		pass
	elif(org_name == "journalsentinel" and page.url.find("jsonline") != -1):
		pass
	elif(org_name == "virginianpilot" and page.url.find("pilotonline") != -1):
		pass
	elif(org_name == "sacbee_news" and page.url.find("sacbee") != -1):
		pass
	elif(org_name == "thebuffalonews" and page.url.find("buffalonews") != -1):
		pass
	elif(org_name == "sunsentinel" and page.url.find("sun-sentinel") != -1):
		pass
	elif(org_name == "enquirer" and page.url.find("cincinnati") != -1):
		pass
	elif(org_name == "startelegram" and page.url.find("star-telegram") != -1):
		pass
	elif(org_name == "dispatchalerts" and page.url.find("dispatch") != -1):
		pass
	elif(org_name == "wapoexpress" and page.url.find("washingtonpost") != -1):
		pass
	elif(org_name == "courierjournal" and page.url.find("courier-journal") != -1):
		pass
	elif(org_name == "theobserver" and page.url.find("charlotteobserver") != -1):
		pass

	elif(org_name == "pittsburghpg" and page.url.find("post-gazette") != -1):
		if(page.url.find("newsinteractive.post-gazette.com") == -1):
			pass
		else:
			numWithoutHTTPS += 1
			print("\t\t\t\t" + org_name + " tried accessing " + page.url + " originally was " + link)
			break	


		elif(org == "latimes"):
			dates = soup.find('span', {'class' : 'timestamp-article'}).get_text().lstrip()
			
			all_captions = soup.find_all('figure')
			for caption in all_captions:
				caption = caption.find('figcaption')
				if(caption == None):
					continue

				tmp = "" if(caption.find('div') == None) else caption.find('div').get_text()
				if(tmp == ""):
					tmp = "" if(caption == None) else caption.get_text()

				cr = caption.find('span', {'class':'credits'})
				if(cr != None):
					cr = cr.get_text()
				else:
					cr = "" if(tmp.rfind("(") == -1) else tmp[tmp.rfind("("):]

				images.append([tmp, cr])
				if(len(images) >= CONST_MAX_IMG):
					break

		elif(org == "nypost"):
			dates = soup.find_all('p', {'class': 'byline-date'})
			date = (''.join(date.get_text() for date in dates)).lstrip()
			
			all_captions = soup.find_all(class_="wp-caption-text")
			for caption in all_captions:
				cc = caption.find('span')
				cr = caption.find('span', {'class': 'credit'})
				images.append([cc.get_text(), "" if(cr == None) else cr.get_text()])
				if(len(images) >= CONST_MAX_IMG):
					break

		elif(org == "washingtonpost"):
			date = soup.find('span', {'itemprop': 'datePublished'})['content']

			all_captions = soup.find_all('span', {'class':'pb-caption'})
			for caption in all_captions:
				cr_start = caption.get_text().find('(')
				cc = caption.get_text()[:cr_start]
				cr = "" if(cr_start == -1) else caption.get_text()[cr_start:]
				images.append([cc, cr])
				if(len(images) >= CONST_MAX_IMG):
					break

		elif(org == "newsday"):
			date = soup.find('time', {'itemprop': 'datePublished'})['datetime']

			all_captions = soup.find_all(class_="mediaCell")
			for caption in all_captions:
				tmp = caption.find('div', {'class':'video'})
				if(tmp != None and len(tmp) != 0):
					break

				caption = caption.find(class_='caption')	
				cr_start = -1 if(caption == None) else caption.get_text().find('Photo Credit:')
				cc = "" if(caption == None) else caption.get_text()[:cr_start].lstrip().rstrip()
				cr = "" if(cr_start == -1) else caption.get_text()[cr_start+len('Photo Credit:'):].rstrip().lstrip()
				images.append([cc, cr])
				if(len(images) >= CONST_MAX_IMG):
					break

		elif(org == "nytimes"):
			date = soup.find('time')['datetime']

			all_captions = soup.find_all("figcaption", {'itemprop':'caption description'})
			for caption in all_captions:
				try:
					cr = caption.find('span', {'itemprop':'copyrightHolder'}).find_all('span')[1].get_text() 
				except:
					cr = ""
				try:
					cc = caption.find('span').get_text() 
				except:
					cc = ""

				if(not(cc == "" and cr == "")):
					images.append([cc, cr])

				if(len(images) >= CONST_MAX_IMG):
					break

		elif(org == "startribune"):
			date = soup.find('div', {'class': 'article-dateline'}).get_text().lstrip().rstrip()

			featured = soup.find_all("div", {'class':'article-featured-gallery-mod'})
			for image in featured:
				image = image.prettify()
				cr_start = image.find('author')
				cr = "" if(cr_start == -1) else image[cr_start:image.find("altText")]

				cc_start = image.find('caption')
				cc = "" if(cc_start == -1 or cr == -1) else image[cc_start+10:cr_start-3]
				images.append([cc, cr])
				if(len(images) >= CONST_MAX_IMG):
					break

			related = soup.find_all('div', {'class':'related-media'})
			for image in related:
				try:
					cc = image.find('div', {'class':'related-caption toggle-photo-caption'}).get_text().lstrip().rstrip()
				except:
					cc = ""
				try:
					cr = image.find('div', {'class':'related-byline'}).get_text().lstrip().rstrip()
				except:
					cr = ""

				if(not(cc == "" and cr == "")):
					images.append([cc, cr])
				if(len(images) >= CONST_MAX_IMG):
					break

		elif(org == "nydailynews"):
			date = ""; time = "";
			date = soup.find('span', {'class':'timestamp timestamp-article '}).get_text()
			try:
				time = soup.find('span', {'class':'timestamp timestamp-article hidden-tablet '}).get_text()
			except:
				pass
			date = date + time

			all_captions = soup.find_all('div', {'class':'card-content'})
			# print(len(all_captions))
			for caption in all_captions:
				if(caption.find('figure') != None):
					caption = caption.find('figcaption')
					cc = "" if(caption.find('div') == None) else caption.find('div').get_text()
					if(cc == ""):
						cc == caption.get_text()

					cr = "" if(cc.rfind('(') == -1) else cc[cc.rfind('('):]

					if(not(cc == "" and cr == "")):
						images.append([cc, cr])

					if(len(images) >= CONST_MAX_IMG):
						break

		#doesn't work for many articles https://www.chron.com/neighborhood/katy/news/article/Memphis-based-Corkys-BBQ-chain-Houston-location-13602474.php?utm_campaign=sftwitter#photo-14541132
		elif(org == "houstonchron"):
			date = soup.find('time')['datetime']

			all_captions = soup.find_all('figcaption')
			for caption in all_captions:
				cc = "" if(caption.find('span', {'class':'caption'}) == None) else caption.find('span', {'class':'caption'}).get_text()
				cr = "" if(caption.find('span', {'class':'credits'}) == None) else caption.find('span', {'class':'credits'}).get_text()

				images.append([cc, cr])
				if(len(images) >= CONST_MAX_IMG):
					break

		elif(org == "denverpost"):
			date = soup.find('time')['datetime']

			all_images = soup.find_all('figure')
			for image in all_images:
				if(image.find('figcaption') == None):
					continue

				cc = image.find('figcaption')
				cr = image.find('div', {'class': 'photo-credit'})

				images.append(["" if(cc == None) else cc.get_text(), "" if(cr == None) else cr.get_text()])
				if(len(images) >= CONST_MAX_IMG):
					break

			slideshows = soup.find_all('div', {'class':'article-slideshow'})
			for slideshow in slideshows:
				all_images = slideshow.find_all('div', {'class':'image-wrapper'})
				for image in all_images:
					cc = image.find('p', {'class':'slide-caption'})
					cr = image.find('p', {'class':'slide-credit'})

					if(cc == None and cr == None):
						continue

					images.append(["" if(cc == None) else cc.get_text(), "" if(cr == None) else cr.get_text()])
					if(len(images) >= CONST_MAX_IMG):
						break

		elif(org == "azcentral"):
			date = soup.find('span', {'class':'asset-metabar-time asset-metabar-item nobyline'}).get_text()

			all_images = soup.find_all('div', {'class':'story-asset image-asset'})
			for image in all_images:
				cc = image.find('p')
				cr = image.find('span', {'class':'credit'})

				images.append(["" if(cc == None) else cc.get_text(), "" if(cr == None) else cr if(type(cr) == type("")) else cr.get_text()])
				if(len(images) >= CONST_MAX_IMG):
					break

			galleries = soup.find_all('div', {'class': 'story-priority-asset gallery-asset'})
			for gallery in galleries:
				all_images = gallery.find_all('div', {'itemprop':['associatedMedia', 'primaryImageOfPage']})
				for image in all_images:
					cc = image.find('div', {'class':'pag-photo-caption'})
					cr = image.find('cite', {'class':'pag-photo-credit'})
					
					images.append(["" if(cc == None) else cc.get_text().lstrip().rstrip(), "" if(cr == None) else cr if(type(cr) == type("")) else cr.get_text().lstrip().rstrip()])
					if(len(images) >= CONST_MAX_IMG):
						break	


		# Sports Articles don't work
		elif(org == "bostonglobe"):
			try:
				date = soup.find('time')['datetime']
			except:
				date = soup.find('span', {'class': 'article-header__pubdate'}).get_text() if(soup.find('span', {'class': 'article-header__pubdate'}) != None) else ""

			all_images = soup.find_all('figure')
			for image in all_images:
				if(image.find('figcaption') == None):
					continue
				cc = image.find('div', {'class':'inline-media__caption'})
				if(cc == None):
					cc = image.find('div', {'itemprop' : 'description caption'})
				cr = image.find('div', {'class':'inline-media__credit'})
				if(cr == None):
					cr = image.find('div', {'class':'lead-media__credit'})

				images.append(["" if(cc == None) else cc.get_text(), "" if(cr == None) else cr.get_text()])
				if(len(images) >= CONST_MAX_IMG):
					break
					
			all_images = soup.find_all('div', {'class':'inline-asset__caption'})
			for image in all_images:
				cr = image.find('p', {'class':'inline-asset__credit'})
				cc = image.find_all('p')
				cc = cc[1] if(len(cc) == 2) else cc[0] if (len(cc) == 1) else None

				images.append(["" if(cc == None) else cc.get_text(), "" if(cr == None) else cr.get_text()])
				if(len(images) >= CONST_MAX_IMG):
					break

		

		elif(org == "phillyinquirer"):
			tmp = soup.prettify().find('data-timestamp="')
			date = soup.prettify()[tmp+len('data-timestamp="') : soup.prettify().find('"', tmp+1+len('data-timestamp="'))]

			all_images = soup.find_all('figure')
			for image in all_images:
				cc = image.find('figcaption')
				cr = image.find('div', {'class':'spaced spaced-top spaced-bottom spaced-xs'})
				if(cr == None and cc != None):
					cr = image.find('figcaption').find('span')

				images.append(["" if(cc == None) else cc.get_text().rstrip().lstrip(), "" if(cr == None) else cr if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()])
				if(len(images) >= CONST_MAX_IMG):
					break
		
		elif(org == "amnewyork"):
			date = soup.find('time', {'itemprop':'datePublished'})['datetime']

			all_images = soup.find_all(class_="mediaCell")
			for image in all_images:
				if(image.find('img') == None or image.find('div', {'class':'video'}) != None):
					continue

				if(image.find('p', {'class':'caption'}) != None):
					cc = image.find('p', {'class':'caption'})					
				else:
					cc = image.find('figcaption')
					
				cr = "" if(cc == None) else cc.get_text()[cc.get_text().rfind('Photo Credit:'):]
				images.append(["" if(cc == None) else cc.get_text().rstrip().lstrip(), "" if(cr == None) else cr.rstrip().lstrip()])
				if(len(images) >= CONST_MAX_IMG):
					break

		elif(org == "dallasnews"):
			date = soup.find('time')['datetime']

			all_images = soup.find_all('figure', {'class':['art-story__image', 'article-content__figure']})
			for image in all_images:
				if(image.find('img') == None):
					continue

				cc = image.find('figcaption')
				cr = None if(cc == None) else cc.find('div', {'class':'art-image__credit'})
				if(cr == None and cc != None):
					cr = cc.find('p', {'class':'article__figure__attribution'})

				images.append(["" if(cc == None) else cc.get_text().rstrip().lstrip(), "" if(cr == None) else cr.get_text().rstrip().lstrip()])
				if(len(images) >= CONST_MAX_IMG):
					break

		elif(org == "starledger"):
			date = soup.find('time')['datetime']

			all_images = soup.find_all('div')
			for image in all_images:
				cc = image.find('figcaption')
				cr = cc.get_text()[cc.get_text().rfind('('):].rstrip().lstrip() if(cc != None and cc.get_text().rfind('(') != -1) else None

				cc = "" if(cc == None) else cc.get_text().rstrip().lstrip()
				cr = "" if(cr == None) else cr
				if(cc != "" or cr != ""):
					images.append([cc, cr])
					
				if(len(images) >= CONST_MAX_IMG):
					break

		elif(org == "sfchronicle"):
			try:
				date = soup.find('time')['datetime']

				all_captions = soup.find_all('section', {'data-component':'photo'})
				for caption in all_captions:					
					caption = caption.find('div', {'class':'media-meta-section media-meta-caption'})
					if(caption == None):
						images.append(["", ""])
						continue

					cc = caption.find('span', {'class':'media-meta-caption-inner'})
					cr = caption.find('div', {'class':'media-meta-credits'})
				
					images.append(["" if(cc == None) else cc.get_text().rstrip().lstrip(), "" if(cr == None) else cr.get_text().rstrip().lstrip()])
					if(len(images) >= CONST_MAX_IMG):
						break

				all_captions = soup.find_all('figcaption')
				for caption in all_captions:
					cc = caption.find('span', {'class':'caption'})
					cr = caption.find('span', {'class':'credits'})
					
					images.append(["" if(cc == None) else cc.get_text().rstrip().lstrip(), "" if(cr == None) else cr.get_text().rstrip().lstrip()])
					if(len(images) >= CONST_MAX_IMG):
						break
			except:
				#Datebook article
				dates = soup.find_all('span', {'class':'dateline'})	
				date = '\t'.join(tmp.get_text() for tmp in dates)

				all_captions = soup.find_all('figure')
				for caption in all_captions:
					if(caption.find('img') == None):
						continue

					cc = caption.find('figcaption')
					cr = "" if(caption.find('figcaption') == None) else caption.find('figcaption').find('span')
					images.append(["" if(cc == None) else cc.get_text().rstrip().lstrip(), "" if(cr == None) else cr.get_text().rstrip().lstrip()])
					if(len(images) >= CONST_MAX_IMG):
						break

			elif(org == "pioneerpress"):
				date = soup.find('div', {'class':'time'}).get_text()

				all_images = soup.find_all('figure')
				for image in all_images:
					if(image.find('img') == None):
						continue

					cc = image.find('figcaption')
					cr = cc.get_text()[cc.get_text().rfind('('):].rstrip().lstrip() if(cc != None and cc.get_text().rfind('(') != -1) else None

					cc = "" if(cc == None) else cc.get_text().rstrip().lstrip()
					cr = "" if(cr == None) else cr
					if(cc != "" or cr != ""):
						images.append([cc, cr])
						
					if(len(images) >= CONST_MAX_IMG):
						break

				slideshows = soup.find_all('div', {'class':'article-slideshow'})
				for show in slideshows:
					all_images = show.find_all('li')
					for image in all_images:
						if(image.find('p', {'class':'slide-caption'}) != None):
							cc = image.find('p', {'class':'slide-caption'})
							cr = cc.get_text()[cc.get_text().rfind('('):].rstrip().lstrip() if(cc != None and cc.get_text().rfind('(') != -1) else None

							cc = "" if(cc == None) else cc.get_text().rstrip().lstrip()
							cr = "" if(cr == None) else cr
							if(cc != "" or cr != ""):
								images.append([cc, cr])
								
							if(len(images) >= CONST_MAX_IMG):
								break

			elif(org == "orlandosentinel"):
				date = soup.find('time')['datetime']

				all_images = soup.find_all('div', {'class': 'trb_em_m'})
				for image in all_images:
					if(image.find('div', {'itemprop':'video'}) != None or image.find('img') == None):
						continue

					image = image.find('div', {'class': 'trb_em_r'})				
					if(image == None):
						continue

					cc = image.find('div', {'class':'trb_em_r_ca'})
					cr = image.find('div', {'class':'trb_em_r_cr'})

					if(cc == None and image.find('div', {'class':'trb_em_r_cc'}) != None):
						cc = image.find('div', {'class':'trb_em_r_cc'})

					images.append(["" if(cc == None) else cc.get_text().rstrip().lstrip(), "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()])
					if(len(images) >= CONST_MAX_IMG):
						break

			elif(org == "sdut"):
				date = soup.find('time')['datetime']

				all_images = soup.find_all('div', {'class': 'trb_em_m'})
				for image in all_images:
					if(image.find('div', {'itemprop':'video'}) != None or image.find('img') == None):
						continue

					image = image.find('div', {'class': 'trb_em_r'})				
					if(image == None):
						continue

					cc = image.find('div', {'class':'trb_em_r_ca'})
					cr = image.find('div', {'class':'trb_em_r_cr'})

					if(cc == None and image.find('div', {'class':'trb_em_r_cc'}) != None):
						cc = image.find('div', {'class':'trb_em_r_cc'})

					images.append(["" if(cc == None) else cc.get_text().rstrip().lstrip(), "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()])
					if(len(images) >= CONST_MAX_IMG):
						break

			
			if(org == "freep"):
				date = soup.find('span', {'class':'asset-metabar-time asset-metabar-item nobyline'}).get_text()
				try:
					date = date + "\t" + soup.find('span', {'class':'asset-metabar-time-updated'}).get_text()
				except:
					pass
				date = date.lstrip().rstrip()

				all_images = soup.find_all('div', {'class':'story-asset image-asset'})
				for image in all_images:
					if(image.find('img') == None):
						continue

					cc = image.find('p')
					cr = image.find('span', {'class':'credit'})

					images.append(["" if(cc == None) else cc.get_text().rstrip().lstrip(), "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()])							
					if(len(images) >= CONST_MAX_IMG):
						break

				#Photogalleries
				all_images = soup.find_all('div', {'class':'caption'})
				for image in all_images:
					cc = image.find('span', {'class':'js-caption'})
					cr = image.find('span', {'class':'credit'})

					if(cc != None or cr != None):
						images.append(["" if(cc == None) else cc.get_text().rstrip().lstrip(), "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()])							
						
					if(len(images) >= CONST_MAX_IMG):
						break
		
		if(org == "pittsburghpg"):
			text = soup.prettify()
			date_start = text.find('"displayUpdateDate":"') + len('"displayUpdateDate":"')
			date = text[date_start: text.find('"', date_start + 1)]

			all_images = (text[text.find('"images":') + len('images":') + 1:text.find(',"related"')])
			while(all_images.find('"caption":') != -1):
				cc_start = all_images.find('"caption":') + len('"caption":')
				cc = all_images[cc_start:all_images.find(',"linkText', cc_start+1)]
				cr_start = all_images.find('"photoCredit":') + len('"photoCredit":')
				cr = all_images[cr_start:all_images.find(',"orientation', cr_start+1)]

				all_images = all_images[all_images.find(',"orientation', cr_start+1)+1:]
				cc = "" if(cc == '"""') else cc
				cr = "" if(cr == '"""') else cr
				images.append([cc, cr])
				if(len(images) >= CONST_MAX_IMG):
					break

			while(text.find("""<span class=\\"pg-embedcode-largeimage-caption\\">""") != -1):
				cc_start = text.find("""<span class=\\"pg-embedcode-largeimage-caption\\">""") + len("""<span class=\\"pg-embedcode-largeimage-caption\\">""")
				cc = text[cc_start:text.find("<\\/span>", cc_start)]				
				cr_start = text.find("""<span class=\\"pg-embedcode-largeimage-credit\\">""") + len("""<span class=\\"pg-embedcode-largeimage-credit\\">""")
				cr = text[cr_start:text.find("<\\/span>", cr_start)]				

				text = text[text.find("<\\/span>", cr_start) + len("<\\/span>") + 1:]
				images.append([cc, cr])
				if(len(images) >= CONST_MAX_IMG):
					break

		elif(org == "hartfordcourant"):
			date = soup.find('span', {'class':'timestamp timestamp-article '}).get_text()

			all_images = soup.find_all('figure')
			for image in all_images:
				if(image.find('img') == None):
					continue
				cc = image.find('figcaption')
				cr = cc.get_text()[cc.get_text().rfind('('):].rstrip().lstrip() if(cc != None and cc.get_text().rfind('(') != -1) else None

				if(cc != None or cr != None):
					images.append(["" if(cc == None) else cc.get_text().rstrip().lstrip(), "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()])
				if(len(images) >= CONST_MAX_IMG):
					break

			text = soup.prettify()
			while(text.find("caption:") != -1):
				cc_start = text.find("caption:") + len("caption:")
				cc = text[cc_start:text.find("credit:", cc_start)]				
				cr_start = text.find("credit:", cc_start) + len("credit:")
				cr = text[cr_start:text.find("authorsHtml:", cr_start)]				

				text = text[text.find("authorsHtml:", cr_start) + 1:]
				images.append([cc.lstrip().rstrip(), cr.lstrip().rstrip()])
				if(len(images) >= CONST_MAX_IMG):
					break

		if(org == "kcstar"):
			date = soup.find('div', {'class':'article-dates'}).get_text().lstrip().rstrip()

			text = soup.prettify()
			while(text.find("""<div class="caption">""") != -1):
				cc_start = text.find("""<div class="caption">""")
				cc_end = text.find("""</div>""", cc_start)+ len("</div>")

				image = BeautifulSoup(text[cc_start:cc_end], 'html.parser')
				# print(cc_start, cc_end)
				cc = image.find('span', {'class':'caption-text'})
				cr = image.find('span', {'class':'credits'})

				text = text[cc_end:]
				images.append(["" if(cc == None) else cc if(type(cc) == type("")) else cc.get_text().lstrip().rstrip(), "" if(cr == None) else cr if(type(cr) == type("")) else cr.get_text().lstrip().rstrip()])
				if(len(images) >= CONST_MAX_IMG):
					break

		
	
		if(org == "staradvertiser"):
			date = soup.find('div', {'class':'custom_byline postdate'}).get_text()

			all_images = soup.find_all('div', {'class':'carousel-story'})
			for tmp in all_images:
				for image in tmp.find_all('li'):
					if(image.find('div', {'class':'video-container'}) != None):
						continue
					cc = image.find('div', {'class':'caption'})
					cr = cc.find('p')

					images.append(["" if(cc == None) else cc.get_text().rstrip().lstrip(), "" if(cr == None) else cr.get_text().rstrip().lstrip()])
					if(len(images) >= CONST_MAX_IMG):
						break

		if(org == "ajc"):
			date = soup.find('time')['data-timestamp']

			all_images = soup.find_all('div', {'class':'tease__img tease__img--photo'})
			all_images.extend(soup.find_all('div', {'class': 'inline-media-container inline-media-container--align-center'}))
			for image in all_images:
				if(image.find('img') == None):
					continue
				cc = image.find('div', {'class':'photo__caption__text'})
				cr = image.find('div', {'class':'photo__credit__text'})
				if(cr == None and cc != None):
					cc = cc.get_text()
					cr = cc[cc.rfind('['):] if(cc.rfind('[') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else None

				images.append(["" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip(), "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()])			
				if(len(images) >= CONST_MAX_IMG):
					break

		if(org == "expressnews"):
			dates = soup.find_all('time')
			date = '\t'.join(tmp['datetime'] for tmp in dates)

			all_images = soup.find_all('section', {'class':'media-photo'})
			for image in all_images:
				if(image.find('img') == -1):
					continue
				cc = image.find('span', {'class':'media-meta-caption-inner'})
				cr = image.find('div', {'class':'media-meta-credits'})

				images.append(["" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip(), "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()])			
				if(len(images) >= CONST_MAX_IMG):
					break

			galleries = soup.find_all('div', {'class':'gallery__slider'})
			for gallery in galleries:
				all_images = gallery.find_all('figure')
				for image in all_images:
					if(image.find('img') == -1):
						continue

					cc = image.find('span', {'class':'caption'})
					cr = image.find('span', {'class':'credits'})

					images.append(["" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip(), "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()])			
					if(len(images) >= CONST_MAX_IMG):
						break

		if(org == "mercnews"):
			date = soup.find('div', {'class':'time'}).get_text().lstrip().rstrip()
			
			soup = soup.find('div', {'class':'article-content'})
			if(soup == None):
				raise Exception("Merc News no article-content")
			all_images = soup.find_all('figure')
			for image in all_images:
				if(image.find('img') == None):
					continue

				cc = image.find('figcaption')
				cr = image.find('div', {'class':'photo-credit'})
				if(cr == None and cc != None):
					cc = cc.get_text()
					cr = cc[cc.rfind('['):] if(cc.rfind('[') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else None

				images.append(["" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip(), "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()])			
				if(len(images) >= CONST_MAX_IMG):
					break

			galleries = soup.find_all('div', {'class':'article-slideshow'})
			for gallery in galleries:
				all_images = gallery.find_all('li')

				for image in all_images:
					if(image.find('img') == None):
						continue

					cc = image.find('p', {'class':'slide-caption'})
					cr = image.find('p', {'class':'slide-credit'})
					if((cr == None or cr.get_text() == "") and cc != None):
						cc = cc.get_text()
						cr = cc[cc.rfind('['):] if(cc.rfind('[') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else None

					images.append(["" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip(), "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()])			
					if(len(images) >= CONST_MAX_IMG):
						break

		if(org == "journalsentinel"):
			date = soup.find('span', {'class':'asset-metabar-time asset-metabar-item nobyline'}).get_text().lstrip().rstrip()
			
			# lastpic = soup.find('div', {'id':'module-position-RocQG-FsX1Y'})
			# print(lastpic)
			# if(lastpic != None):
			# 	print('here')
			# 	if(lastpic.find('img') != None):
			# 		lastpic.find(p)
			# 		cc = image.find('p')
			# 		cr = image.find('span', {'class':'credit'})
			# 		if(cr == None and cc != None):
			# 			cc = cc.get_text()
			# 			cr = cc[cc.rfind('['):] if(cc.rfind('[') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else None

			# 		if(not(len(images) >= CONST_MAX_IMG)):
			# 			images.append(["" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip(), "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()])						

			all_images = soup.find_all('div', {'class':'story-asset image-asset'})
			for image in all_images:
				if(image.find('img') == None):
					continue

				cc = image.find('p')
				cr = image.find('span', {'class':'credit'})
				if(cr == None and cc != None):
					cc = cc.get_text()
					cr = cc[cc.rfind('['):] if(cc.rfind('[') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else None

				images.append(["" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip(), "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()])			
				if(len(images) >= CONST_MAX_IMG):
					break

			soup = soup.prettify()
			soup = soup[:soup.rfind('p-text-last')]
			soup = BeautifulSoup(soup, 'html.parser')
			
			galleries = soup.find_all('div', {'class':'companion-story-gallery'})
			for gallery in galleries:
				captions = gallery.find_all('div', {'class':'caption'})
				for caption in captions:
					cc = caption
					cr = caption.find('span', {'class':'credit gallery-viewport-credit'})

					if(cr == None and cc != None):
						cc = cc.get_text()
						cr = cc[cc.rfind('['):] if(cc.rfind('[') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else None

					cc = "" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip()					
					cr = "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()
					if(not(cc == "" and cr == "")):
							images.append([cc, cr])			
					if(len(images) >= CONST_MAX_IMG):
						break

		if(org == "virginianpilot"):
			date = soup.find('time')['datetime']
			
			all_images = soup.find_all('figure')
			for image in all_images:
				if(image.find('img') == None):
					continue

				cc = image.find('span', {'class':'caption-text'})
				cr = image.find('span', {'class':'credit'})
				if(cr == None and cc != None):
					cc = cc.get_text()
					cr = cc[cc.rfind('['):] if(cc.rfind('[') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else None
				
				cc = "" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip()
				cr = "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()	
				if(not(cc == "" and cr == "")):
					images.append([cc, cr])			
				if(len(images) >= CONST_MAX_IMG):
					break

			galleries = soup.find_all('div', {'id': 'asset-photo-carousel'})
			for gallery in galleries:
				all_images = soup.find_all('div', {'class':'item-container'})
				for image in all_images:
					if(image.find('img') == None):
						continue

					cc = image.find('div', {'class':'caption-text'})
					cr = image.find('li', {'class':'credit'})
					if(cr == None and cc != None):
						cc = cc.get_text()
						cr = cc[cc.rfind('['):] if(cc.rfind('[') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else None
					
					cc = "" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip()
					cr = "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()	
					if(not(cc == "" and cr == "") and [cc, cr] not in images):
						images.append([cc, cr])			
					if(len(images) >= CONST_MAX_IMG):
						break

		if(org == "suntimes"):
			date = soup.find('span', {'class':'post-relative-date top-date'}).get_text().lstrip().rstrip()
			
			all_images = soup.find_all('div', {'class':'image-caption'}) + soup.find_all('div', {'class':'slideshow-slide-caption'}) + soup.find_all('p', {'class':'wp-caption-text'})
			for image in all_images:
				cc = image
				cr = None
				if(cr == None and cc != None):
					cc = cc.get_text()
					cr = cc[cc.rfind('|'):] if(cc.rfind('|') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else None
				
				cc = "" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip()
				cr = "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()	

				images.append([cc, cr])			
				if(len(images) >= CONST_MAX_IMG):
					break

		if(org == "ocregister"):
			dates = soup.find_all('time')
			date = "\t".join(tmp.get_text() for tmp in dates)
			
			soup = soup.find('div', {'class':'article-content'}) 
			all_images = soup.find_all('figure')
			for image in all_images:
				if(image.find('img') == -1):
					continue

				cc = image.find('figcaption')
				cr = None
				if(cr == None and cc != None):
					cc = cc.get_text()
					cr = cc[cc.rfind('['):] if(cc.rfind('[') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else None
				
				cc = "" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip()
				cr = "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()	
				if(not(cc == "" and cr == "")):
					images.append([cc, cr])			
				if(len(images) >= CONST_MAX_IMG):
					break

			all_images = soup.find_all('p', {'class':'slide-caption'}) 
			for image in all_images:
				cc = image
				cr = None
				if(cr == None and cc != None):
					cc = cc.get_text()
					cr = cc[cc.rfind('['):] if(cc.rfind('[') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else None
				
				cc = "" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip()
				cr = "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()	
				if(not(cc == "" and cr == "")):
					images.append([cc, cr])			
				if(len(images) >= CONST_MAX_IMG):
					break


		if(org == "sunsentinel"):
			date = soup.find('time')['datetime']
			
			all_images = soup.find_all('div', {'class':'trb_em_m'})
			for image in all_images:
				if(image.find('svg', {'class':'trb_em_v_figure_video_svg'}) != None):
					continue

				cc = image.find('div', {'class':'trb_em_r_cc'})
				cr = image.find('div', {'class':'trb_em_r_cr'})
				if(cr == None or cc.get_text().lstrip().rstrip() == ""):
					cr = image.find('div', {'class':'trb_em_r_ca'})

				if(cr == None and cc != None):
					cc = cc.get_text()
					cr = cc[cc.rfind('['):] if(cc.rfind('[') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else None
				
				cc = "" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip()
				cr = "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()	
				if(not(cc == "" and cr == "")):
					images.append([cc, cr])			
				if(len(images) >= CONST_MAX_IMG):
					break		

		


		if(org == "indystar"):
			date = soup.find('span', {'class':'asset-metabar-time asset-metabar-item nobyline'}).get_text().lstrip().rstrip()

			soup = soup.find('div', {'class':'asset-double-wide double-wide p402_premium'})
			all_images = soup.find_all('div', {'class':'story-asset image-asset'})
			for image in all_images:
				if(image.find('img') == None):
					continue

				cc = image.find('p')
				cr = image.find('span', {'class':'credit'})
				if(cr == None and cc != None):
					cc = cc.get_text()
					cr = cc[cc.rfind('['):] if(cc.rfind('[') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else None

				images.append(["" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip(), "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()])			
				if(len(images) >= CONST_MAX_IMG):
					break
			
			galleries = soup.find_all('div', {'class':'companion-story-gallery'})
			for gallery in galleries:
				captions = gallery.find_all('div', {'class':'caption'})
				for caption in captions:
					cc = caption
					cr = caption.find('span', {'class':'credit gallery-viewport-credit'})

					if(cr == None and cc != None):
						cc = cc.get_text()
						cr = cc[cc.rfind('['):] if(cc.rfind('[') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else None

					cc = "" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip()					
					cr = "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()
					if(not(cc == "" and cr == "")):
							images.append([cc, cr])			
					if(len(images) >= CONST_MAX_IMG):
						break

		if(org == "metronewyork"):
			date = soup.find('span', {'class':'article-pub-date'}).get_text().lstrip().rstrip()

			soup = soup.find('div', {'class':'article-container'})
			all_images = soup.find_all('div', {'class':'article-media'})
			for image in all_images:
				if(image.find('picture') == None):
					continue

				cc = image.find('div', {'class':'article-caption'})
				cr = image.find('span', {'class':'article-cradit'})
				if(cr == None and cc != None):
					cc = cc.get_text()
					cr = cc[cc.rfind('['):] if(cc.rfind('[') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else None

				images.append(["" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip(), "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()])			
				if(len(images) >= CONST_MAX_IMG):
					break



		if(org == "courierjournal"):
			date = soup.find('span', {'class':'asset-metabar-time asset-metabar-item nobyline'}).get_text().lstrip().rstrip()

			soup = soup.find('div', {'class':'asset-double-wide double-wide p402_premium'})
			all_images = soup.find_all('div', {'class':'story-asset image-asset'})
			for image in all_images:
				if(image.find('img') == None):
					continue

				cc = image.find('p')
				cr = image.find('span', {'class':'credit'})
				if(cr == None and cc != None):
					cc = cc.get_text()
					cr = cc[cc.rfind('['):] if(cc.rfind('[') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else None

				images.append(["" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip(), "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()])			
				if(len(images) >= CONST_MAX_IMG):
					break
			
			galleries = soup.find_all('div', {'class':'companion-story-gallery'})
			for gallery in galleries:
				captions = gallery.find_all('div', {'class':'caption'})
				for caption in captions:
					cc = caption
					cr = caption.find('span', {'class':'credit gallery-viewport-credit'})

					if(cr == None and cc != None):
						cc = cc.get_text()
						cr = cc[cc.rfind('['):] if(cc.rfind('[') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else None

					cc = "" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip()					
					cr = "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()
					if(not(cc == "" and cr == "")):
							images.append([cc, cr])			
					if(len(images) >= CONST_MAX_IMG):
						break

		if(org == "daytondailynews"):
			date = soup.find('time')['data-timestamp']

			# First image
			all_images = soup.find_all('div', {'class':'tease__img tease__img--photo'})
			for image in all_images:
				if(image.find('img') == None):
					continue

				cc = image.find('div', {'class':'photo__caption'})
				cr = image.find('div', {'class':'photo__credit'})
				if(cr == None and cc != None):
					cc = cc.get_text()
					cr = cc[cc.rfind('['):] if(cc.rfind('[') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else None

				images.append(["" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip(), "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()])			
				if(len(images) >= CONST_MAX_IMG):
					break

			all_images = soup.find_all('div', {'class':'inline-media-container inline-media-container--align-center'})
			for image in all_images:
				if(image.find('img') == None):
					continue

				cc = image.find('div', {'class':'photo__caption'})
				cr = image.find('div', {'class':'photo__credit'})
				if(cr == None and cc != None):
					cc = cc.get_text()
					cr = cc[cc.rfind('['):] if(cc.rfind('[') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else None

				images.append(["" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip(), "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()])			
				if(len(images) >= CONST_MAX_IMG):
					break





		if(org == "thebuffalonews"):
			date = soup.find('time')['datetime']

			all_images = soup.find_all('section', {'class':'featured-image'})
			for image in all_images:
				if(image.find('img') == None):
					continue

				cc = image.find('label', {'class':'featured-image-caption'})
				cr = None
				if(cr == None and cc != None):
					cc = cc.get_text()
					cr = cc[cc.rfind('['):] if(cc.rfind('[') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else None
				
				if(not(cc == "" and cr == "")):
					images.append(["" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip(), "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()])			
				if(len(images) >= CONST_MAX_IMG):
					break

			all_images = soup.find_all('p', {'class':'wp-caption-text'})
			for image in all_images:
				cc = image
				cr = None
				if(cr == None and cc != None):
					cc = cc.get_text()
					cr = cc[cc.rfind('['):] if(cc.rfind('[') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else ""
				
				images.append(["" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip(), "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()])			
				if(len(images) >= CONST_MAX_IMG):
					break

		if(org == "wapoexpress"):
			date = soup.find('span', {'itemprop': 'datePublished'})['content']

			all_captions = soup.find_all('div', {'class':'inline-photo'})
			for caption in all_captions:
				cc = caption.find('span', {'class':'pb-caption'})
				cr = None
				if(cr == None and cc != None):
					cc = cc.get_text()
					cr = cc[cc.rfind('['):] if(cc.rfind('[') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else None
				
				images.append(["" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip(), "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()])								
				if(len(images) >= CONST_MAX_IMG):
					break

		if(org == "stltoday"):
			date = soup.find('time')['datetime']
			
			all_images = soup.find_all('figure')
			for image in all_images:
				if(image.find('img') == -1):
					continue

				cc = image.find('span', {'class':'caption-text'})
				cr = None #image.find('span', {'class':'credit'})
				if(cr == None and cc != None):
					cc = cc.get_text()
					cr = cc[cc.rfind('['):] if(cc.rfind('[') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else None
				
				cc = "" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip()
				cr = "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()	
				if(not(cc == "" and cr == "")):
					images.append([cc, cr])			
				if(len(images) >= CONST_MAX_IMG):
					break

			galleries = soup.find_all('div', {'id': 'asset-photo-carousel'})
			for gallery in galleries:
				all_images = gallery.find_all('div', {'class':'caption-container'})
				for image in all_images:
					cc = image.find('div', {'class':'caption-text'})
					cr = None #image.find('li', {'class':'credit'})

					if(cr == None and cc != None):
						cc = cc.get_text()
						cr = cc[cc.rfind('['):] if(cc.rfind('[') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else None
					
					cc = "" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip()
					cr = "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()	
					images.append([cc, cr])			
					if(len(images) >= CONST_MAX_IMG):
						break

		if(org == "arkansasonline"):
			date = soup.find('span', {'class':'most-recent-article-bi-line'}).get_text().lstrip().rstrip()
			
			all_images = soup.find_all('span', {'class':'article-image-credit'}) 
			for image in all_images:
				cc = image
				cr = None
				if(cr == None and cc != None):
					cc = cc.get_text()
					cr = cc[cc.rfind('/'):] if(cc.rfind('/') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else None
				
				cc = "" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip()
				cr = "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()	
				if(not(cc == None and cr == None)):
					images.append([cc, cr])			
				if(len(images) >= CONST_MAX_IMG):
					break

			all_images = soup.find_all('div', {'class':'inline__block'})
			for image in all_images:
				if(image.find('img') == None):
					continue

				cc = image.find('span')
				if(cc == None):
					cc = image.find_all('div', {'class':'inline_item'})[-1]
				cr = None
				if(cr == None and cc != None):
					cc = cc.get_text()
					cr = cc[cc.rfind('/'):] if(cc.rfind('/') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else None
				
				cc = "" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip()
				cr = "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()	
				if(not(cc == None and cr == None)):
					images.append([cc, cr])			
				if(len(images) >= CONST_MAX_IMG):
					break

		


		if(org == "bostonherald"):
			date = soup.find('time')['datetime']

			all_images = soup.find_all('figure')
			for image in all_images:
				if(image.find('img') == None):
					continue

				cc = image.find('figcaption')
				cr = None
				if(cr == None and cc != None):
					cc = cc.get_text()
					cr = cc[cc.rfind('['):] if(cc.rfind('[') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else None

				cc = "" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip()
				cr = "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()
				if(not(cc == "" and cr == "")):
					images.append([cc, cr])			
				if(len(images) >= CONST_MAX_IMG):
					break

			slideshows = soup.find_all('div', {'class':'article-slideshow'})
			for show in slideshows:
				all_images = show.find_all('li')
				for image in all_images:
					if(image.find('p', {'class':'slide-caption'}) != None):
						cc = image.find('p', {'class':'slide-caption'})
						cr = cc.get_text()[cc.get_text().rfind('('):].rstrip().lstrip() if(cc != None and cc.get_text().rfind('(') != -1) else None

						cc = "" if(cc == None) else cc.get_text().rstrip().lstrip()
						cr = "" if(cr == None) else cr
						if(cc != "" or cr != ""):
							images.append([cc, cr])
							
						if(len(images) >= CONST_MAX_IMG):
							break

		if(org == "triblive"):
			date = soup.find('div', {'class':'author-info'}).get_text().lstrip().rstrip()

			# First image
			all_images = soup.find_all('div', {'class':'slide'})
			for image in all_images:
				if(image.find('img') == None):
					continue

				cc = image.find('div', {'class':'caption'})
				cr = image.find('div', {'class':'credit'})
				if(cr == None and cc != None):
					cc = cc.get_text()
					cr = cc[cc.rfind('['):] if(cc.rfind('[') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else None

				images.append(["" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip(), "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()])			
				if(len(images) >= CONST_MAX_IMG):
					break

		

	if(org == "sacbee_news"):
			date = soup.find('div', {'class':'article-dates'}).get_text().lstrip().rstrip()

			# LEAD ITEM
			image = soup.find('div', {'class':'lead-item'})
			skip = False
			if(image != None and image.find('img') != None):
				cc = image.find('div', {'class':'lead-caption'})
				cr = image.find('span', {'class':'credits'})

				if(cr == None and cc != None):
					cc = cc.get_text()
					cr = cc[cc.rfind('['):] if(cc.rfind('[') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else None
				
				skip = True
				images.append(["" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip(), "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()])			

			all_images = soup.find_all('div', {'class':'img-container picture '})
			first = True
			for image in all_images:
				if(image.find('img') == None):
					continue

				cc = image.find('div', {'class':'inline-caption-text'})
				cr = image.find('div', {'class':'inline-creditInfo'})
				if(cr == None):
					cr = image.find('span', {'class':'credits'})

				if(cr == None and cc != None):
					cc = cc.get_text()
					cr = cc[cc.rfind('['):] if(cc.rfind('[') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else None
				
				if(not(cc == "" and cr == "")):
					if(skip):
						skip = False
					else:
						images.append(["" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip(), "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()])			

				if(len(images) >= CONST_MAX_IMG):
					break

			text = soup.prettify()
			if(text.find("""<script id="inlinegallery-template-""") != -1):				
				index = text.find("""<script id="inlinegallery-template-""") + len("""<script id="inlinegallery-template-""")
				text = text[text.find('div', index):text.find('</script>', index)]
				soup = BeautifulSoup(text, 'html.parser')
				all_images = soup.find_all('div', {'class':'gallery-item image'})
				for image in all_images:
					cc = image.find('span', {'class':'caption-text'})
					cr = ("" if(image.find('span', {'class':'photographer'}) == None) else image.find('span', {'class':'photographer'}).get_text()) + " " + ("" if(image.find('span', {'class':'credits'}) == None) else image.find('span', {'class':'credits'}).get_text())
					cr = cr.lstrip().rstrip()

					if(cr == "" and cc != None):
						cc = cc.get_text()
						cr = cc[cc.rfind('['):] if(cc.rfind('[') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else None
					
					images.append(["" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip(), "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()])			
					if(len(images) >= CONST_MAX_IMG):
						break

		if(org == "abqjournal"):
			try:
				date = soup.find('div', {'class':'published'}).get_text().lstrip().rstrip()
			except:
				date = soup.find('h6').get_text().lstrip().rstrip()

			# First image
			all_images = soup.find_all('section', {'class':'featured-photo'})
			for image in all_images:
				if(image.find('img') == None):
					continue

				cc = image.find('div', {'class':'caption'})
				cr = None
				if(cr == None and cc != None):
					cc = cc.get_text()
					cr = cc[cc.rfind('['):] if(cc.rfind('[') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else None

				images.append(["" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip(), "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()])			
				if(len(images) >= CONST_MAX_IMG):
					break

			all_images = soup.find_all('div', {'class':'wp-caption'})
			for image in all_images:
				if(image.find('img') == None):
					continue

				cc = image.find('p', {'class':'wp-caption-text'})
				cr = None
				if(cr == None and cc != None):
					cc = cc.get_text()
					cr = cc[cc.rfind('['):] if(cc.rfind('[') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else None

				images.append(["" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip(), "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()])			
				if(len(images) >= CONST_MAX_IMG):
					break

			#Galleries
			soup = soup.prettify()
			if(soup.find('Galleria.run') != -1):
				start = soup.find('Galleria.run') + len('Galleria.run')
				all_images = soup[start : soup.find('</script>', start)]

				while(all_images.find('"description":') != -1):
					cc_start = all_images.find('"description":') + len('"description":')
					cc = all_images[cc_start:all_images.find(',"link', cc_start+1)]

					all_images = all_images[all_images.find(',"link', cc_start+1)+1:]
					cc = "" if(cc == '"""') else cc
					cr = cc[cc.rfind('['):] if(cc.rfind('[') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else ""

					images.append([cc, cr])
					if(len(images) >= CONST_MAX_IMG):
						break

		if(org == "sltrib"):
			date = soup.find('div', {'class':'publish-wrap d-flex align-items-end'}).get_text().rstrip().lstrip()

			all_images = soup.find_all('figure')
			for image in all_images:
				if(image.find('img') == None):
					continue

				cc = image.find('figcaption')
				cr = None
				if(cr == None and cc != None):
					cc = cc.get_text()
					cr = cc[:cc.rfind('|')] if(cc.rfind('|') != -1) else cc[cc.rfind('['):] if(cc.rfind('[') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else None

				cc = "" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip()
				cr = "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()
				if(not(cc == "" and cr == "")):
					images.append([cc, cr])			
				if(len(images) >= CONST_MAX_IMG):
					break

			captions  = soup.find_all('span', {'class':'caption caption-full-text'})
			for image in captions:
				cc = image.get_text()
				cr = None

				if(cr == None and cc != None):
					cr = cc[cc.rfind('['):] if(cc.rfind('[') != -1) else cc[cc.rfind('('):cc.rfind(')', cc.rfind('('))] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else None
				
				cc = "" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip()
				cr = "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()	
				if(not(cc == "" and cr == "")):
					images.append([cc, cr])			
				if(len(images) >= CONST_MAX_IMG):
					break
	# Based on Sacbee code but dandC is USATODAY network
	# if(org == "dandc"):
	# 		date = soup.find('span', {'class':'asset-metabar-time asset-metabar-item nobyline'}).get_text()

	# 		all_images = soup.find_all('div', {'class':'story-asset image-asset'})
	# 		for image in all_images:
	# 			cc = image.find('p')
	# 			cr = image.find('span', {'class':'credit'})

	# 			images.append(["" if(cc == None) else cc.get_text(), "" if(cr == None) else cr if(type(cr) == type("")) else cr.get_text()])
	# 			if(len(images) >= CONST_MAX_IMG):
	# 				break

	# 		galleries = soup.find_all('div', {'class': 'companion-story-gallery js-llc'})+ soup.find_all('div', {'class': 'story-priority-asset gallery-asset'})
	# 		for gallery in galleries:
	# 			all_images = gallery.find_all('div', {'itemprop':['associatedMedia', 'primaryImageOfPage']})
	# 			for image in all_images:
	# 				cc = image.find('span', {'class':'js-caption'})
	# 				cr = image.find('span', {'class':'credit'})
					
	# 				images.append(["" if(cc == None) else cc.get_text().lstrip().rstrip(), "" if(cr == None) else cr if(type(cr) == type("")) else cr.get_text().lstrip().rstrip()])
	# 				if(len(images) >= CONST_MAX_IMG):
	# 					break
						
		

	if(org in ["dmregister", "dandc", "tennessean", "memphisnews", "knoxnews", "asburyparkpress", "ndn", "delawareonline", "thenewspress", "usatoday"]):
			dates = soup.find_all('span', {'class' : 'asset-metabar-time asset-metabar-item nobyline'})
			date = (''.join(date.get_text() for date in dates)).lstrip()
			
			raw_images = soup.find_all('div', {'class' : 'story-asset image-asset'})
			gallery = soup.find_all('div', {'class':'gallery-viewport-caption'})# + soup.find_all('div', {'class':'gallery-viewport-caption'})
			# if(raw_images == None and gallery == None):
			# 	raise Exception('No images found')

			for image in raw_images:
				if(image.find('p') != None):
					p = image.find('p')
					credit = p.find('span', {'class' : 'credit'})
					credit = "" if (credit == None) else credit.get_text() 
					images.append([p.get_text(), credit])

				if(len(images) >= CONST_MAX_IMG):
					break

			for image in gallery:
				cc = image.find('span', {'class':'js-caption'}).get_text()
				cr = "" if(image.find('span', {'class':'credit'}) == None) else image.find('span', {'class':'credit'}).get_text().lstrip().rstrip()
				images.append([cc, cr])

				if(len(images) >= CONST_MAX_IMG):
					break

	if(org == "toledonews"):
			# Remove comments
			comments = soup.findAll(text=lambda text:isinstance(text, Comment))
			[comment.extract() for comment in comments]

			all_images = soup.prettify()
			date_start = all_images.find('"pubDate":') + len('"pubDate":')
			# print(date_start)
			date = all_images[date_start:all_images.find('",', date_start)]
			if(len(date) > 300):
				raise Exception('Probably weather')

			while(all_images.find('"caption":') != -1):
				cc_start = all_images.find('"caption":') + len('"caption":')
				cc = all_images[cc_start:all_images.find('"linkText', cc_start+1)].lstrip().rstrip()
				cr_start = all_images.find('"photoCredit":') + len('"photoCredit":')
				cr = all_images[cr_start:all_images.find('"orientation', cr_start+1)].lstrip().rstrip()

				all_images = all_images[all_images.find('"orientation', cr_start+1)+1:]
				cr = "" if(cr.translate(str.maketrans('', '', string.punctuation)) == '') else cr
				cc = "" if(cc.translate(str.maketrans('', '', string.punctuation)) == '') else cc
				images.append([cc, cr])
				if(len(images) >= CONST_MAX_IMG):
					break


				
if(org in ["projo", "jaxdotcom", "dbnewsjournal", "heraldtribune", "ohiodotcom", "pbpost", "statesman"]):
			date = soup.find('span', {'class':'article-meta-date'}).get_text().rstrip().lstrip() + " \t" + ("" if(soup.find('span', {'class':'article-meta-updated'}) == None) else soup.find('span', {'class':'article-meta-updated'}).get_text().rstrip().lstrip())
			if(date.lstrip().rstrip() == "xxxxxxxxxx"):
				raise Exception("Photogallery article")

			text = soup.prettify()
			while(text.find('"type":') != -1):
				cat_start = text.find('"type":') + len('"type":')
				first_quote = text.find('"', cat_start+1)
				second_quote = text.find('"', first_quote+1)
				cat = text[first_quote:second_quote+1]

				start = cat_start
				end = text.find('"type":', cat_start)

				# Ignore this
				if(cat != '"story"'):
					extractImage(text[start:end], images)

				text = text[end:]

		if(org == "detroitnews"):
			dates = soup.find_all('span', {'class' : 'asset-metabar-time asset-metabar-item nobyline'})
			date = (''.join(date.get_text() for date in dates)).lstrip()
			
			raw_images = soup.find_all('div', {'class' : 'story-asset image-asset'})
			gallery = soup.find_all('div', {'class':'gallery-viewport-caption'})# + soup.find_all('div', {'class':'gallery-viewport-caption'})
			jsimages = soup.find_all('span', {'class':'js-caption-wrapper'})

			for image in jsimages:
				cc = image.get_text()
				cr = image.find('span', {'class':'credit'})

				if(cr == None and cc != None):
					cc = cc.get_text()
					cr = cc[cc.rfind('['):] if(cc.rfind('[') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else None
					
				cc = "" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip()
				cr = "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()	
				if(not(cc == "" and cr == "")):
					images.append([cc, cr])

				if(len(images) >= CONST_MAX_IMG):
					break

			# if(raw_images == None and gallery == None):
			# 	raise Exception('No images found')

			for image in raw_images:
				if(image.find('p') != None):
					p = image.find('p')
					credit = p.find('span', {'class' : 'credit'})
					credit = "" if (credit == None) else credit.get_text() 
					images.append([p.get_text(), credit])

				if(len(images) >= CONST_MAX_IMG):
					break

			for image in gallery:
				cc = image.find('span', {'class':'js-caption'}).get_text()
				cr = "" if(image.find('span', {'class':'credit'}) == None) else image.find('span', {'class':'credit'}).get_text().lstrip().rstrip()
				images.append([cc, cr])

				if(len(images) >= CONST_MAX_IMG):
					break

		

		if(org in ["theobserver", "startelegram", "miamiherald", "newsobserver"]):
			date = soup.find('div', {'class':'article-dates'}).get_text().lstrip().rstrip()
			# LEAD ITEM
			image = soup.find('div', {'class':'lead-item'})
			skip = False
			if(image != None and image.find('img') != None):
				cc = image.find('div', {'class':'lead-caption'})
				cr = ("" if(image.find('span', {'class':'photographer'}) == None) else image.find('span', {'class':'photographer'}).get_text()) + " " + ("" if(image.find('span', {'class':'credits'}) == None) else image.find('span', {'class':'credits'}).get_text())

				if((cr == None or cr.lstrip().rstrip() == "") and cc != None):
					cc = cc.get_text()
					cr = cc[cc.rfind('['):] if(cc.rfind('[') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('Courtesy'):] if(cc.rfind('Courtesy') != -1) else None

				skip = True
				images.append(["" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip(), "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()])			

			all_images = soup.find_all('div', {'class':'img-container picture '})
			first = True
			for image in all_images:
				if(image.find('img') == None):
					continue

				cc = image.find('div', {'class':'inline-caption-text'})
				cr = image.find('div', {'class':'inline-creditInfo'})
				if(cr == None):
					cr = image.find('span', {'class':'credits'})

				if((cr == None or cr.get_text().lstrip().rstrip() == "") and cc != None):
					cc = cc.get_text()
					cr = cc[cc.rfind('['):] if(cc.rfind('[') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('Courtesy'):] if(cc.rfind('Courtesy') != -1) else None

				
				if(not(cc == "" and cr == "")):
					if(skip):
						skip = False
					else:
						images.append(["" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip(), "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()])			

				if(len(images) >= CONST_MAX_IMG):
					break

			text = soup.prettify()
			if(text.find("""<script id="inlinegallery-template-""") != -1):				
				index = text.find("""<script id="inlinegallery-template-""") + len("""<script id="inlinegallery-template-""")
				text = text[text.find('div', index):text.find('</script>', index)]
				soup = BeautifulSoup(text, 'html.parser')
				all_images = soup.find_all('div', {'class':'gallery-item image'})
				for image in all_images:
					cc = image.find('span', {'class':'caption-text'})
					cr = ("" if(image.find('span', {'class':'photographer'}) == None) else image.find('span', {'class':'photographer'}).get_text()) + " " + ("" if(image.find('span', {'class':'credits'}) == None) else image.find('span', {'class':'credits'}).get_text())
					cr = cr.lstrip().rstrip()

					if(cr == "" and cc != None):
						cc = cc.get_text()
						cr = cc[cc.rfind('['):] if(cc.rfind('[') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('Courtesy'):] if(cc.rfind('Courtesy') != -1) else None
					
					images.append(["" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip(), "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()])			
					if(len(images) >= CONST_MAX_IMG):
						break

		if(org == "baltimoresun" or org == "mcall"):
			date = soup.find('time')['datetime']
			
			all_images = soup.find_all('div', {'class':'trb_em_m'})
			for image in all_images:
				if(image.find('svg', {'class':'trb_em_v_figure_video_svg'}) != None):
					continue

				# Ignore duplicate
				if(image.find('aside', {'class':'trb_em trb_embed trb_em_th'}) != None):
					continue

				cc = image.find('div', {'class':'trb_em_r_cc'})
				cr = image.find('div', {'class':'trb_em_r_cr'})
				if(cr == None or cc.get_text().lstrip().rstrip() == ""):
					cr = image.find('div', {'class':'trb_em_r_ca'})

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
			script_start = text.find('<script id="embed_')
			if(script_start != -1):
				script_start = text.find('<span', script_start)
				text = text[script_start:text.find('</script>', script_start)]
				soup = BeautifulSoup(text, 'html.parser')
				all_images = soup.find_all('div', {'class':'trb_em_m'})
				for image in all_images:
					if(image.find('svg', {'class':'trb_em_v_figure_video_svg'}) != None):
						continue
					cc = image.find('div', {'class':'trb_em_r_cc'})
					cr = image.find('div', {'class':'trb_em_r_cr'})
					if(cr == None or cc.get_text().lstrip().rstrip() == ""):
						cr = image.find('div', {'class':'trb_em_r_ca'})

					if(cr == None and cc != None):
						cc = cc.get_text()
						cr = cc[cc.rfind('['):] if(cc.rfind('[') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else None
					
					cc = "" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip()
					cr = "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()	
					if(not(cc == "" and cr == "")):
						images.append([cc, cr])			
					if(len(images) >= CONST_MAX_IMG):
						break
						
			if(org == "baltimoresun" or org == "mcall"):
			date = soup.find('time')['datetime']
			
			all_images = soup.find_all('div', {'class':'trb_em_m'})
			for image in all_images:
				if(image.find('svg', {'class':'trb_em_v_figure_video_svg'}) != None):
					continue

				# Ignore duplicate
				if(image.find('aside', {'class':'trb_em trb_embed trb_em_th'}) != None):
					continue

				cc = image.find('div', {'class':'trb_em_r_cc'})
				cr = image.find('div', {'class':'trb_em_r_cr'})
				if(cr == None or cc.get_text().lstrip().rstrip() == ""):
					cr = image.find('div', {'class':'trb_em_r_ca'})

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
			script_start = text.find('<script id="embed_')
			if(script_start != -1):
				script_start = text.find('<span', script_start)
				text = text[script_start:text.find('</script>', script_start)]
				soup = BeautifulSoup(text, 'html.parser')
				all_images = soup.find_all('div', {'class':'trb_em_m'})
				for image in all_images:
					if(image.find('svg', {'class':'trb_em_v_figure_video_svg'}) != None):
						continue
					cc = image.find('div', {'class':'trb_em_r_cc'})
					cr = image.find('div', {'class':'trb_em_r_cr'})
					if(cr == None or cc.get_text().lstrip().rstrip() == ""):
						cr = image.find('div', {'class':'trb_em_r_ca'})

					if(cr == None and cc != None):
						cc = cc.get_text()
						cr = cc[cc.rfind('['):] if(cc.rfind('[') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else None
					
					cc = "" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip()
					cr = "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()	
					if(not(cc == "" and cr == "")):
						images.append([cc, cr])			
					if(len(images) >= CONST_MAX_IMG):
						break

	if(org == "deseretnews"):
			date = soup.find('span', {'class':'ftime'}).get_text().lstrip().rstrip()

			# all_images = soup.find_all('div', {'class':'photo-caption margin-top-sm font-size-smaller line-height-lg'})
			# for image in all_images:
			# 	cc = image
			# 	cr = None
			# 	if(cr == None and cc != None):
			# 		cc = cc.get_text()
			# 		cr = cc[cc.rfind('['):cc.rfind(']', cc.rfind('['))] if(cc.rfind('[') != -1) else cc[cc.rfind('([)'):cc.rfind(')', cc.rfind('([)'))] if(cc.rfind('([)') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('{'):cc.rfind('}', cc.rfind('{'))] if(cc.rfind('{') != -1) else cc[cc.rfind('Courtesy'):] if(cc.rfind('Courtesy') != -1) else None

			# 	images.append(["" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip(), "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()])			
			# 	if(len(images) >= CONST_MAX_IMG):
			# 		break

			text = soup.prettify()
			all_images = text[text.find('<div class="article-body">'):text.find('ReactDOM.render', text.find('<div class="article-body">'))]
			while(all_images.find('"caption":') != -1):
				cc_start = all_images.find('"caption":') + len('"caption":')
				cc = all_images[cc_start:all_images.find(',"credit":', cc_start+1)]
				cr_start = all_images.find('"credit":', cc_start) + len('"credit":')
				video = all_images.find('"externalId":', cr_start+1)
				non_video = all_images.find('"source":', cr_start+1)
				if(video == -1 or (video > non_video and non_video != -1)):
					cr = all_images[cr_start:all_images.find('"source":', cr_start+1)]

					all_images = all_images[all_images.find('"source":', cr_start+1)+1:]
					cr = "" if(cr.translate(str.maketrans('', '', string.punctuation)) == '') else cr
					cc = "" if(cc.translate(str.maketrans('', '', string.punctuation)) == '') else cc
					images.append([cc, cr])
					if(len(images) >= CONST_MAX_IMG):
						break
				else:
					all_images = all_images[all_images.find('"externalId":', cr_start+1)+1:]					

		if(org == "owhnews"):
			date = soup.find('time')['datetime']

			all_images = soup.find_all('div', {'class':'item-container'})
			for image in all_images:
				if(image.find('div', {'itemprop':'image'}) == None):
					continue

				cc = image.find('div', {'class':'caption-text'})
				cr = image.find(class_='credit')
				if(cr == None and cc != None):
					cc = cc.get_text()
					cr = cc[cc.rfind('['):] if(cc.rfind('[') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else None
				
				cc = "" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip()
				cr = "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()	
				if(not(cc == "" and cr == "")):
					images.append([cc, cr])			
				if(len(images) >= CONST_MAX_IMG):
					break

			# Other non-gallery images
			all_images = soup.find_all('figure', {'class':'photo'})
			for image in all_images:
				if(image.find('img') == None or image.find('figcaption') == None):
					continue

				cc = image.find('figcaption').find('span', {'class':'caption-text'})
				cr = image.find('figcaption').find('span', {'class':'credit'})

				if(cr == None and cc != None):
					cc = cc.get_text()
					cr = cc[cc.rfind('['):] if(cc.rfind('[') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('('):] if(cc.rfind('(') != -1) else None
				
				cc = "" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip()
				cr = "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()	
				if(not(cc == "" and cr == "")):
					images.append([cc, cr])			
				if(len(images) >= CONST_MAX_IMG):
					break

		if(org == "spokesmanreview"):
			date = (("" if(soup.find('p', {'itemprop':'dateModified'}) == None) else soup.find('p', {'itemprop':'dateModified'}).get_text().lstrip().rstrip()) + "    " + ("" if(soup.find('p', {'itemprop':'datePublished'}) == None) else soup.find('p', {'itemprop':'datePublished'}).get_text().lstrip().rstrip())).lstrip().rstrip()

			all_images = soup.find_all('figure')
			for image in all_images:
				if(image.find('img') == None):
					continue
				cc = image.find('figcaption')
				if(cc == None or image.prettify().find('class="dib dn-ns"') != -1):
					continue

				cr = None
				if(cr == None and cc != None):
					cc = cc.get_text()
					cr = cc[cc.rfind('['):cc.rfind(']', cc.rfind('['))] if(cc.rfind('[') != -1) else cc[cc.rfind('('):cc.rfind(')', cc.rfind('('))] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('{'):cc.rfind('}', cc.rfind('{'))] if(cc.rfind('{') != -1) else cc[cc.rfind('Courtesy'):] if(cc.rfind('Courtesy') != -1) else None

				images.append(["" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip(), "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()])			
				if(len(images) >= CONST_MAX_IMG):
					break

			all_images = soup.prettify()
			while(all_images.find('"description":') != -1):
				cc_start = all_images.find('"description":') + len('"description":')
				cc = all_images[cc_start:all_images.find('"pubdate":', cc_start+1)].lstrip().rstrip()
				cr_start = all_images.find('"author":', cc_start) + len('"author":')
				cr = all_images[cr_start:all_images.find('"categories":', cr_start+1)].lstrip().rstrip()

				all_images = all_images[all_images.find('"categories":', cr_start+1)+1:]
				cr = "" if(cr.translate(str.maketrans('', '', string.punctuation)) == '') else cr
				cc = "" if(cc.translate(str.maketrans('', '', string.punctuation)) == '') else cc
				if(len(cr) > 500):
					cr = ""
				if(cr == "" and cc != None):
					cc = cc.get_text()
					cr = cc[cc.rfind('['):cc.rfind(']', cc.rfind('['))] if(cc.rfind('[') != -1) else cc[cc.rfind('('):cc.rfind(')', cc.rfind('('))] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('{'):cc.rfind('}', cc.rfind('{'))] if(cc.rfind('{') != -1) else cc[cc.rfind('Courtesy'):] if(cc.rfind('Courtesy') != -1) else None

				images.append([cc, cr])
				if(len(images) >= CONST_MAX_IMG):
					break

		if(org == "dailyherald"):
			date = soup.find('div', {'class':'artDates'}).get_text().rstrip().lstrip()

			all_images = soup.find_all('p', {'class':'captionBox clearFix'})
			for image in all_images:
				cc = image.find('span', {'class':'caption'})
				if(cc == None):
					cc = image.find('span', {'class':'captionFull'})
				if(cc == None):
					cc = image
				cr = image.find('span', {'class':'credit'})

				if(cr == None and cc != None):
					cc = cc.get_text()
					cr = cc[cc.rfind('['):cc.rfind(']', cc.rfind('['))] if(cc.rfind('[') != -1) else cc[cc.rfind('('):cc.rfind(')', cc.rfind('('))] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('{'):cc.rfind('}', cc.rfind('{'))] if(cc.rfind('{') != -1) else cc[cc.rfind('Courtesy'):] if(cc.rfind('Courtesy') != -1) else None

				images.append(["" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip(), "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()])			
				if(len(images) >= CONST_MAX_IMG):
					break

			for div in soup.find_all('div', {'style':'margin:10px 5%;font-size:14px;line-height:17px;width:90%;font-weight:bold;padding:0;'}):
				cc = div
				cr = div.find('span', {'style':'font-weight:normal;margin-left:5px;color:#000;'})

				if(cr == None and cc != None):
					cc = cc.get_text()
					cr = cc[cc.rfind('['):cc.rfind(']', cc.rfind('['))] if(cc.rfind('[') != -1) else cc[cc.rfind('('):cc.rfind(')', cc.rfind('('))] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('{'):cc.rfind('}', cc.rfind('{'))] if(cc.rfind('{') != -1) else cc[cc.rfind('Courtesy'):] if(cc.rfind('Courtesy') != -1) else None

				images.append(["" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip(), "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()])			
				if(len(images) >= CONST_MAX_IMG):
					break


		if(org == "wistatejournal"):
			date = soup.find('time')['datetime']

			all_images = soup.find_all('figure', {'class':'photo'})				
			for image in all_images:
				if(image.find('img') == None or image.find('figcaption') == None):
					continue

				cc = image.find('figcaption', {'class':'caption'})
				cr = image.find('span', {'class':'credit'})

				if(cr == None and cc != None):
					cc = cc.get_text()
					cr = cc[cc.rfind('['):cc.rfind(']', cc.rfind('['))] if(cc.rfind('[') != -1) else cc[cc.rfind('('):cc.rfind(')', cc.rfind('('))] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('{'):cc.rfind('}', cc.rfind('{'))] if(cc.rfind('{') != -1) else cc[cc.rfind('Courtesy'):] if(cc.rfind('Courtesy') != -1) else None

				if(["" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip(), "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()] not in images):
					images.append(["" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip(), "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()])			
				if(len(images) >= CONST_MAX_IMG):
					break

			# captions = soup.find_all('div', {'class':'caption-container'})
			# for caption in captions:
			# 	cc = caption.find('div', {'class':'caption-text'})
			# 	cr = caption.find(class_="credit")
			# 	if(cr == None and cc != None):
			# 		cc = cc.get_text()
			# 		cr = cc[cc.rfind('['):cc.rfind(']', cc.rfind('['))] if(cc.rfind('[') != -1) else cc[cc.rfind('('):cc.rfind(')', cc.rfind('('))] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('{'):cc.rfind('}', cc.rfind('{'))] if(cc.rfind('{') != -1) else cc[cc.rfind('Courtesy'):] if(cc.rfind('Courtesy') != -1) else None

			# 	images.append(["" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip(), "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()])			
			# 	if(len(images) >= CONST_MAX_IMG):
			# 		break

		elif(org == "chicagotribune"):
			date = soup.find('time', {'itemprop':'datePublished'})
			date = date['data-dt'] + " " + date['datetime']

			all_images = soup.find_all('div', {'class': 'trb_em_m'})
			for image in all_images:
				if(image.find('div', {'itemprop':'video'}) != None):
					continue

				image = image.find('div', {'class': 'trb_em_r'})				
				if(image == None):
					continue

				cc = image.find('div', {'class':'trb_em_r_ca'})
				cr = image.find('div', {'class':'trb_em_r_cr'})

				if(cc == None and image.find('div', {'class':'trb_em_r_cc'}) != None):
					cc = image.find('div', {'class':'trb_em_r_cc'}).find('p')
					if(cr == None):
						cr = image.find('div', {'class':'trb_em_r_cc'}).prettify()
						cr = cr[cr.rfind('('):]

				cc = "" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip()
				cr = "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()	
				images.append([cc, cr])		

				if(len(images) >= CONST_MAX_IMG):
					break

	if(org == "tb_times"):
			try:
				dates = soup.find('div', {'class':'article__pubdate'}).find_all('span', {'class': 'timestamp'})
				date = '\t'.join(date['title'] for date in dates)

				if(soup.find('div', {'class':'article__hero-area'}).find('figure') != None):
					cc = soup.find('div', {'class':'article__carousel--caption'}).get_text().rstrip().lstrip()
					cr = cc[cc.rfind('['):cc.rfind(']', cc.rfind('['))] if(cc.rfind('[') != -1) else cc[cc.rfind('('):cc.rfind(')', cc.rfind('('))] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('{'):cc.rfind('}', cc.rfind('{'))] if(cc.rfind('{') != -1) else cc[cc.rfind('Courtesy'):] if(cc.rfind('Courtesy') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else ""
					
					if(cc != "" or cr != ""):			
						images.append([cc, cr.lstrip().rstrip()])

				all_images = soup.find_all('span', {'class':'inline-img'})
				for image in all_images:
					if(image.find('figcaption') == None):
						continue
					cc = image.find('figcaption').get_text().rstrip().lstrip()
					cr = cc[cc.rfind('['):cc.rfind(']', cc.rfind('['))] if(cc.rfind('[') != -1) else cc[cc.rfind('('):cc.rfind(')', cc.rfind('('))] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('{'):cc.rfind('}', cc.rfind('{'))] if(cc.rfind('{') != -1) else cc[cc.rfind('Courtesy'):] if(cc.rfind('Courtesy') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else None

					images.append(["" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip(), "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()])			
					if(len(images) >= CONST_MAX_IMG):
						break
			except:
				date = soup.find('time')['datetime']

				all_images = soup.find_all('figure')
				for image in all_images:
					cc = "" if(image.find('figcaption') == None) else image.find('figcaption').get_text().rstrip().lstrip()
					cr = cc[cc.rfind('['):cc.rfind(']', cc.rfind('['))] if(cc.rfind('[') != -1) else cc[cc.rfind('('):cc.rfind(')', cc.rfind('('))] if(cc.rfind('(') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else cc[cc.rfind('{'):cc.rfind('}', cc.rfind('{'))] if(cc.rfind('{') != -1) else cc[cc.rfind('Courtesy'):] if(cc.rfind('Courtesy') != -1) else cc[cc.rfind('Photo'):] if(cc.rfind('Photo') != -1) else None

					images.append(["" if(cc == None) else cc.get_text().rstrip().lstrip() if(type(cc) != type("")) else cc.lstrip().rstrip(), "" if(cr == None) else cr.lstrip().rstrip() if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()])			
					if(len(images) >= CONST_MAX_IMG):
						break