		if(org == "usatoday"):
			dates = soup.find_all('span', {'class' : 'asset-metabar-time asset-metabar-item nobyline'})
			date = (''.join(date.get_text() for date in dates)).lstrip()
			
			raw_images = soup.find_all('div', {'class' : 'story-asset image-asset'})
			gallery = soup.find_all('div', {'class':'caption gallery-viewport-caption gallery-viewport-caption-no-mycapture'})
			if(raw_images == None and gallery == None):
				raise Exception('No images found')

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
					cr = image.find('div', {'class':'trb_em_r_cc'}).prettify()
					cr = cr[cr.rfind('('):]

				images.append(["" if(cc == None) else cc.get_text(), "" if(cr == None) else cr if(type(cr) == type("")) else cr.get_text()])
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

		elif(org == "starledger"):
			date = soup.find('time')['datetime']

			all_images = soup.find_all('figure')
			for image in all_images:
				cc = image.find('figcaption')
				cr = cc.find('cite') if(cc != None) else None

				images.append(["" if(cc == None) else cc.get_text().rstrip().lstrip(), "" if(cr == None) else cr if(type(cr) == type("")) else cr.get_text().rstrip().lstrip()])
				if(len(images) >= CONST_MAX_IMG):
					break