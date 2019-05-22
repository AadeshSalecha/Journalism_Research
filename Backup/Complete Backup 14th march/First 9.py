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

		elif(org == "tampabay"):
			try:
				dates = soup.find('div', {'class':'article__pubdate'}).find_all('span', {'class': 'timestamp'})
				date = '\t'.join(date['title'] for date in dates)

				if(soup.find('div', {'class':'article__hero-area'}).find('figure') != None):
					cc = soup.find('div', {'class':'article__carousel--caption'}).get_text().rstrip().lstrip()
					cr = cc[cc.rfind('['):] if(cc.rfind('[') != -1) else cc[:cc.find('|')] if(cc.find('|') != -1) else ""				
					if(cc != "" or cr != ""):			
						images.append([cc, cr.lstrip().rstrip()])

				all_images = soup.find_all('span', {'class':'inline-img'})
				for image in all_images:
					if(image.find('figcaption') == None):
						continue
					cc = image.find('figcaption').get_text().rstrip().lstrip()
					cr = cc[cc.rfind('['):] if(cc.rfind('[') != -1) else cc[:cc.find('|')] if(cc.find('|') != -1) else ""

					if(cc != "" or cr != ""):			
						images.append([cc, cr.lstrip().rstrip()])
					if(len(images) >= CONST_MAX_IMG):
						break
			except:
				date = soup.find('time')['datetime']

				all_images = soup.find_all('figure')
				for image in all_images:
					cc = "" if(image.find('figcaption') == None) else image.find('figcaption').get_text().rstrip().lstrip()
					cr = cc[cc.rfind('['):] if(cc.rfind('[') != -1) else cc[:cc.find('|')] if(cc.find('|') != -1) else ""

					if(cc != "" or cr != ""):			
						images.append([cc, cr.lstrip().rstrip()])
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

		elif(org == "oregonian"):
			# try:
			date = soup.find('time')['datetime']

			all_images = soup.find_all('figure')
			for image in all_images:
				if(image.find('img') == None):
					continue
				cc = image.find('figcaption')
				cr = cc.get_text()[cc.get_text().rfind('('):].rstrip().lstrip() if(cc != None and cc.get_text().rfind('(') != -1) else None

				cc = "" if(cc == None) else cc.get_text().rstrip().lstrip()
				cr = "" if(cr == None) else cr
				images.append([cc, cr])
					
				if(len(images) >= CONST_MAX_IMG):
					break
			# except:
			# 	# expo.oregonlive.com
			# 	date = soup.find('div', {'class':'gallery_byline byline'}).get_text().lstrip().rstrip()

			# 	all_images = soup.find_all('div', {'class':'gallery_slide border'})
			# 	print(len(all_images))
			# 	for image in all_images:
			# 		print(image.prettify() +"\n\n\n\n")
			# 		if(image.find('img') == None):
			# 			continue
			# 		image = image.find('div', {'class':'asset_caption caption'})
			# 		cc = image.get_text()
			# 		cr = image.find('div', {'class':'gallery_slide_credit'})

			# 		cc = "" if(cc == None) else cc.rstrip().lstrip()
			# 		cr = "" if(cr == None) else cr.get_text().rstrip().lstrip()
			# 		if(cc != "" or cr != ""):
			# 			images.append([cc, cr])
						
			# 		if(len(images) >= CONST_MAX_IMG):
			# 			break
	
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