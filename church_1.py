'''
Playlist scraper for WEVL's First Church of Rock
'''
import requests
from bs4 import BeautifulSoup

#- - setup variables and global uses
episode_list = []

def page_search(inp_url):
	global quote_list
	global index
	print("---- ----- -----")
		
	site_inp=inp_url
	thesite = requests.get(site_inp)
	souper =  BeautifulSoup(thesite.content, "html.parser")
	show = souper.find_all("div", class_="block")
	for link in show:
		thelink = str('https://spinitron.com/'+link.find(class_='link').get('href'))
		theday = link.find(class_="day").text
		themonth = link.find(class_='month').text
		theyear = link.find(class_='year').text
		#print(theday+" "+themonth+" "+theyear+' '+thelink)
		#print(' --*-*-*-*--')
		#episode_list.append(each)
	
	epURL = 'https://spinitron.com/WEVL/pl/16757704/The-1st-Church-of-Rock'
	episode_details(epURL)	
		
def episode_details(inp_url):
	print(inp_url)
	show_details = requests.get(inp_url)
	showsoup =  BeautifulSoup(show_details.content, "lxml")
	showdate = (showsoup.find('p', class_='timeslot').text).lstrip()[:12]
	print(showdate)
	listings = showsoup.find_all('div', class_='spins public-spins')
	
	for each in listings:
		track_list = each.find_all('tr', class_='spin-item')
		for tracks in track_list:
			artist = tracks.find(class_='artist').text
			song = tracks.find(class_='song').text
			album = tracks.find(class_='release').text
			date = tracks.find(class_='released').text
			print(artist+' - '+song+' - '+album+' - '+date)
	print (" -- -- ")
'''  
  with open('bored.txt','w') as my_list_file:
		file_content = '\n'.join(episode_list)
		my_list_file.write(file_content)
'''
# MAIN FUNCTION
prefix = "https://spinitron.com/WEVL/show/113358/The-1st-Church-of-Rock?page="
page = 1
while page !=3:
	count=str(page)
	url = prefix+count
	page = page+1
	page_search(url)
print("scrape complete")

'''
'''