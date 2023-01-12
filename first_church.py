'''
Playlist scraper for WEVL's First Church of Rock

https://stackoverflow.com/questions/71545135/how-to-append-rows-with-concat-to-a-pandas-dataframe
https://datascientyst.com/compare-two-pandas-dataframes-get-differences/
https://stackoverflow.com/questions/20225110/comparing-two-dataframes-and-getting-the-differences
https://www.geeksforgeeks.org/how-to-compare-two-dataframes-with-pandas-compare/
https://www.statology.org/pandas-check-if-row-is-in-another-dataframe/
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
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

def page_search(inp_url):
    global quote_list
    global index
    global DBase
    global Indielist
    print("---- ----- -----")
        
    site_inp=inp_url
    thesite = requests.get(site_inp)
    souper =  BeautifulSoup(thesite.content, "lxml")
    show = souper.find_all("div", class_="block")
    for link in show:
        thelink = str('https://spinitron.com/'+link.find(class_='link').get('href'))
        episode_details(thelink)    
        #episode_list.append(each)

#   episode_details(epURL)  
        
def episode_details(inp_url):
    global DBase
    global Indielist
    #print(inp_url)
    
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
                listing = (artist+' - '+song+' - '+album+' - '+date)
                dict = {"show_date":showdate,
                        "Artist":artist,
                        "Title":song,
                        "Album":album,
                        "Year":date             
                    }
                DBase = pd.concat([DBase, pd.DataFrame([dict])])
                DBase = DBase.drop(DBase.columns[0],axis=1)
            except:
                pass
            try:
                DBase.to_csv('offthe_recent.csv',sep=';')
                print (DBase)
            except:
                pass
'''  
'''
def panda_make():
    global DBase
    
    headings = ["show_date","artist","title","album","year"]
    DBase = pd.DataFrame(columns=headings)
   
def compare_monkey():
	global Fulllist
	global shortlist
	list_headings = [" ","show_date","Artist","Title","Album","Year","exists"]
	new_df = pd.DataFrame()
	
	Fulllist = pd.read_csv("offthe_full.csv",sep = ';')
	shortlist = pd.read_csv("offthe_recent.csv",sep = ';')
	#merage and compare both lists
	all_df = pd.merge(Fulllist, shortlist, on=["show_date","Title","Artist","Year","Album"], how='left', indicator='exists')
	all_df['exists'] = np.where(all_df.exists == 'both', True, False)
	#create list with just songs not on smaller list
	new_df= all_df.loc[all_df['exists'] == False]
	#remove comparison column and add placeholder for episode airdate
	new_df = new_df.drop(['exists'],axis=1)
	#new_df.insert(0, 'play_date', '0_UNK_0')
		
	print("comparing csvs")
	new_df.to_csv('comparison.csv',sep=';')
	
	#with open('comparison.txt','w') as my_list_file:
	#	file_content = '\n'.join(all_df)
	#	my_list_file.write(file_content)	
	#print(new_df)
    
# MAIN FUNCTION
panda_make()

against ="https://spinitron.com/WEVL/show/113415/Against-The-Grain?page="
offthe = "https://spinitron.com/WEVL/show/113436/Off-The-Record?page="
church = "https://spinitron.com/WEVL/show/113358/The-1st-Church-of-Rock?page="

prefix = offthe

page = 1
'''
while page !=2:
    count=str(page)
    url = prefix+count
    page = page+1
    page_search(url)
print("scrape complete")
'''
compare_monkey()