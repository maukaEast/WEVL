'''
Playlist scraper for WEVL's First Church of Rock

https://stackoverflow.com/questions/71545135/how-to-append-rows-with-concat-to-a-pandas-dataframe
https://datascientyst.com/compare-two-pandas-dataframes-get-differences/
https://stackoverflow.com/questions/20225110/comparing-two-dataframes-and-getting-the-differences
https://www.geeksforgeeks.org/how-to-compare-two-dataframes-with-pandas-compare/
https://www.statology.org/pandas-check-if-row-is-in-another-dataframe/
exit
'''
import requests
import pandas as pd
import numpy as np

from bs4 import BeautifulSoup
pd.set_option('display.width', 1000)

#- - setup variables and global uses
episode_list = []
global DBase
global Indielist
global Fulllist
global Heavylist
global Fullzig
global Indiezig

def page_search(inp_url):
	print("---- ----- -----")
		
	site_inp=inp_url
	thesite = requests.get(site_inp)
	souper =  BeautifulSoup(thesite.content, "lxml")
	show = souper.find_all("div", class_="block")
	for link in show:
		thelink = str('https://spinitron.com/'+link.find(class_='link').get('href'))
		episode_details(thelink)    
		
def episode_details(inp_url):
	global DBase
	print('')
	print(inp_url)
	
	show_details = requests.get(inp_url)
	showsoup =  BeautifulSoup(show_details.content.decode('utf-8'), "lxml")
	showdate = (showsoup.find('p', class_='timeslot').text).lstrip()[:12]
	showdate = showdate.replace(',','.')
	print(showdate)
	listings = showsoup.find_all('div', class_='spins public-spins')
	
	for each in listings:
		track_list = each.find_all('tr', class_='spin-item')
		for tracks in track_list:
			try:
				artist = tracks.find(class_='artist').text
				song = tracks.find(class_='song').text
				song = song.replace(',','.')
				album = tracks.find(class_='release').text
				album = album.replace(',','.')
				date = tracks.find(class_='released').text
				#print(artist+'  '+song+'   '+album+'  '+date)
				dict = {"show_date":showdate,
						"Artist":artist,
						"Title":song,
						"Album":album,
						"Year":date             
					}
				print(dict)
				DBase = pd.concat([DBase, pd.DataFrame([dict])])
				#DBase = DBase.drop(DBase.columns[0],axis=1)
			except:
				pass
			DBase.to_csv('offthe_recent.csv',sep=';')
			#print (DBase)

def panda_make():
	global DBase
	
	headings = ["show_date","Artist","Title","Album","Year"]
	DBase = pd.DataFrame(columns=headings)
   
def compare_monkey():
	global Fullzig
	global Indiezig
	new_df = pd.DataFrame()
	
	Fullzig = pd.read_csv("formziggy.csv",sep=';')
	Fullzig = (Fullzig.replace(',','.', regex=True))
	#Fullzig = Fullzig.drop(['Length','Genre','Rating','Bitrate','Path','Media'],axis=1)
	#Fullzig.insert(0, 'show_date', '001100')
	Fullzig['show_date']=Fullzig['show_date'].astype(str)
	Fullzig['Year']=Fullzig['Year'].astype(str)

	#Fullzig.drop(Fullzig.columns[0], axis=1, inplace=True)
	
	Indiezig = pd.read_csv("offthe_recent.csv",sep=';')
	Indiezig['show_date']=Indiezig['show_date'].astype(str)
	Indiezig['Year']=Indiezig['Year'].astype(str)
	Indiezig.drop(Indiezig.columns[0], axis=1, inplace=True)
	#Indiezig.drop(Indiezig.columns[0], axis=1, inplace=True)
	Indiezig.to_csv('offthe_recent.csv',sep=';')
		
	#Indiezig = Indiezig.drop(['Length','Genre','Rating','Bitrate','Path','Media'],axis=1)
	print(Indiezig.columns.tolist())
	print(Indiezig.dtypes)
	print(Fullzig.columns.tolist())	
	print(Fullzig.dtypes)
	#merage and compare both lists
	all_df = pd.merge(Fullzig, Indiezig, on=['show_date', 'Title','Artist','Album'], how='left', indicator='exists')

#add column to show if each row in first DataFrame exists in second
	all_df['exists'] = np.where(all_df.exists == 'both', True, False)
	new_df = all_df[all_df['exists']==True]
	#drop assists columns
	#all_df = all_df.drop('exists', axis=1)
	print("comparing csvs")
	#Fullzig.to_csv('formziggy.csv',sep=';')
	new_df.to_csv('comparison.csv',sep=';')
	
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
print("scrape complete")

compare_monkey()