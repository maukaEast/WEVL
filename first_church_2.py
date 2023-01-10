'''
Playlist scraper for WEVL's First Church of Rock
'''
import requests
import pandas as pd
import numpy as np

from bs4 import BeautifulSoup

#- - setup variables and global uses
episode_list = []
global DBase

def page_search(inp_url):
	global quote_list
	global index
	global DBase
	print("---- ----- -----")
		
	site_inp=inp_url
	thesite = requests.get(site_inp)
	souper =  BeautifulSoup(thesite.content, "html.parser")
	show = souper.find_all("div", class_="block")
	for link in show:
		thelink = str('https://spinitron.com/'+link.find(class_='link').get('href'))
		episode_details(thelink)	
		#episode_list.append(each)
	
	epURL = 'https://spinitron.com/WEVL/pl/16757704/The-1st-Church-of-Rock'
#	episode_details(epURL)	
		
def episode_details(inp_url):
	global DBase
	#this is to make up for eventual retirement of 'append' in pandas
	tmp = []
	
	print(inp_url)
	show_details = requests.get(inp_url)
	showsoup =  BeautifulSoup(show_details.content.decode('utf-8'), "lxml")
	showdate = (showsoup.find('p', class_='timeslot').text).lstrip()[:12]
	print(showdate)
	listings = showsoup.find_all('div', class_='spins public-spins')
	
	for each in listings:
		track_list = each.find_all('tr', class_='spin-item')
		for tracks in track_list:

			try:
				artist = tracks.find(class_='artist').text
				song = tracks.find(class_='song').text
				album = tracks.find(class_='release').text
				date = tracks.find(class_='released').text
				listing = (artist+' - '+song+' - '+album+' - '+date)
				dict = {"show_date":showdate,
						"artist":artist,
						"song":song,
						"album":album,
						"date":date				
					}
				tmp.append(dict, ignore_index = True)
			except:
				pass
			try:
				print (listing)
			except:
				pass
	print (" -- -- ")
	DBase = pd.concat(DBase, tmp)
	#print(DBase)
'''  
  with open('bored.txt','w') as my_list_file:
		file_content = '\n'.join(episode_list)
		my_list_file.write(file_content)
'''
def panda_make():
	global DBase
	headings = ["show_date","artist","song","album","date"]
	DBase = pd.DataFrame(columns=headings)

# MAIN FUNCTION
panda_make()

against ="https://spinitron.com/WEVL/show/113415/Against-The-Grain?page="
offthe = "https://spinitron.com/WEVL/show/113436/Off-The-Record?page="
church = "https://spinitron.com/WEVL/show/113358/The-1st-Church-of-Rock?page="

prefix = offthe

page = 1
while page !=2:
	count=str(page)
	url = prefix+count
	page = page+1
	page_search(url)
print(DBase)
print("scrape complete")

'''
'''