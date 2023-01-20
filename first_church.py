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
global DBase
global Fullzig
global scraped_list

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
			DBase.to_csv('first_church_recent.csv',sep=';')
			#print (DBase)

def panda_make():
	global DBase
	
	headings = ["show_date","Artist","Title","Album","Year"]
	DBase = pd.DataFrame(columns=headings)
   
def compare_monkey():
	global Fullzig
	global scraped_list
	
#List of all tracks on ziggy. depending on source, may need further formatting
	Fullzig = pd.read_csv("formziggy.csv",sep=';')
	Fullzig = (Fullzig.replace(',','.', regex=True))
	Fullzig['show_date']=Fullzig['show_date'].astype(str)
	Fullzig['Year']=Fullzig['Year'].astype(str)
#Fullzig.drop(Fullzig.columns[0], axis=1, inplace=True)
#Fullzig = Fullzig.drop(['Length','Genre','Rating','Bitrate','Path','Media'],axis=1)
#Fullzig.insert(0, '', '001100')	

#List made from scraped playlists. May need formatting to gel	
	scraped_list = pd.read_csv("first_church_recent.csv",sep=';')
	#scraped_list = scraped_list.drop(['Length','Genre','Rating','Bitrate','Path','Media'],axis=1)
	scraped_list['show_date']=scraped_list['show_date'].astype(str)
	scraped_list['Year']=scraped_list['Year'].astype(str)
	scraped_list.drop(scraped_list.columns[0], axis=1, inplace=True)
	scraped_list.to_csv('first_church_recent.csv',sep=';')
		
	ind_list = scraped_list.columns.tolist()
	zig_list = Fullzig.columns.tolist()	
	
#merage and compare both lists. fullzig is 'left', scraped_list is 'right', compares on shared columns ('on='). 'how=right' -> keep results from scraped_list. change this to get different result list contents
	all_df = pd.merge(Fullzig, scraped_list, on=['Title','Artist','Album'], how='right', indicator='exists')
	all_df.to_csv('allcompared.csv',sep=';',index=False)
#add column to show if each row in first DataFrame exists in second
	all_df['exists'] = np.where(all_df.exists == 'right_only', True, False)
	new_df = all_df.copy()
#create output frame which only contains the output where track exists in scraped but not ziggy
	new_df = new_df[new_df['exists']==False]
#clean up new frame
	new_df = new_df.drop('exists', axis=1)
	new_df.drop(['show_date_x','Year_x','Year_y'], axis=1,inplace=True)
	new_df.drop(new_df.columns[[0]], axis=1, inplace=True)
	new_df.rename(columns = {'show_date_y':'Show Date'},inplace=True)
	new_df = new_df.loc[:,['Show Date', 'Title','Artist','Album']]
	new_df = (new_df.replace('\.',',', regex=True))
	new_df.drop_duplicates(keep='first',inplace=True)
	print("comparing csvs")
	new_df.to_csv('comparison.csv',sep=';',index=False)
	
# MAIN FUNCTION
panda_make()

against ="https://spinitron.com/WEVL/show/113415/Against-The-Grain?page="
offthe = "https://spinitron.com/WEVL/show/113436/Off-The-Record?page="
church = "https://spinitron.com/WEVL/show/113358/The-1st-Church-of-Rock?page="

prefix = church

page = 1

while page !=4:
	count=str(page)
	url = prefix+count
	page = page+1
	page_search(url)
print("scrape complete")

compare_monkey()