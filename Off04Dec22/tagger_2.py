''''
scripts to update audacity tags with data from scrape
https://methodmatters.github.io/editing-id3-tags-mp3-meta-data-in-python/
https://stackoverflow.com/questions/50575802/convert-dataframe-row-to-dict
https://stackoverflow.com/questions/15147751/how-to-check-if-all-items-in-a-list-are-there-in-another-list
'''
import os
import re
import pandas as pd
import numpy as np
import eyed3
eyed3.log.setLevel("ERROR")	#this disables known bug in eye3d error reporting

mp3_list =[]
show_DB = pd.DataFrame()

def clean_list():		#create search exclusion criteria function
	print("cleaning list of common elements")
	bad = ['the','a','&']

def list_contains(List1, List2):  #prog to check for cell contents
#List 1 is full list, List2 is the search term list
	print("Comparing lists")
	art_list = List1.tolist()	#<- turn Artist column into a list to iterate
	for words in art_list:	#<- for each of the band names
		art_terms = words.split()	#make each band name a list of substrings
		art_terms = list(map(str.lower,art_terms))
		#print(art_terms)
		#check that all terms in the band name are in for the presence of list2
		setcheck = set(List2).issubset(art_terms)
		if setcheck is True:
			print("terms ",List2,"found in Artist column")
			return True 
		#else: 
			#return False
		#	print("not found yet")
main_scrape_list = "offthe_recent.csv"	#name the show database
if main_scrape_list:					#if it exists, create a Pandas Frame for it
	DBase = pd.read_csv('../'+main_scrape_list,sep=';',index_col=False)
	DBase.drop(DBase.columns[0], axis=1, inplace=True)
	print("Scrape list accessed")
else:
	print("No main list found")
	
all_files = os.listdir()
for x in all_files:
	if x.endswith('.mp3'):		#find and format each mp3 in the folder
		mp3_list.append(x[:-4])
		
# ---- MP3 file processing ---- #
for file in mp3_list:
#look at each songfile in mp3 list and make search criteria from name omitting "a", "the", &c.
	stopwords = ['a', 'and', '&', 'the']
	contents = list(filter(lambda w: w not in stopwords, re.split(r'\W+', file.lower())))
	print("Search parameters for "+file+" are:")
	print(contents)
	print("Column check: ", list_contains(DBase['Artist'], contents)) 
#OLD LINE -> if DBase['Artist'].str.contains(file).any(): #<- which needs entire filename
	for each in contents:
#iterate over each entry in the selected artists' name
		#print("Looking for term: "+each)
#if found in the 'Artist' cell for the given showdate, add it to that date's DBase
		if DBase['Artist'].str.contains(each,case=False).any():
			the_values = DBase[(DBase['Artist']==file) & (DBase['show_date']=="Dec 4. 2022 ")]
			#print(the_values) 
			data_dict = the_values.to_dict()
			#print(data_dict)
			show_DB = pd.concat([show_DB,the_values], axis=0,ignore_index=True)			
		else:
			print("no details found for file: "+file)
#print('')
#print('final created database row number:')
#print("\t"+str(show_DB.shape[0]))

show_DB.to_csv('Dec04_22.csv',sep=';',index=False)

#checking for index of given row
for i in range(0,show_DB.shape[0]):
	to_tag_name = str(mp3_list[i])
	to_tag_file = to_tag_name+'.mp3'
	#print("File data for "+to_tag_file+" at index "+str(i))
	#print('')
	#print("Attempting to tag "+to_tag_file)
	#print("from database"+str(show_DB.iloc[i]))
	if show_DB.iloc[i]['Artist']== to_tag_name:
		show_artist = show_DB.iloc[i]['Artist']
		show_title = show_DB.iloc[i]['Title']
		show_album = show_DB.iloc[i]['Album']
		show_date = show_DB.iloc[i]['Year']
		
		audiofile = eyed3.load(to_tag_file)
		audiofile.tag.artist = show_artist
		audiofile.tag.album = show_album
		audiofile.tag.album_artist = show_artist
		audiofile.tag.title = show_title
		audiofile.tag.genre = "Indie"
		#audiofile.tag.release-year = show_date
		audiofile.tag.save()
		
		new_name = show_title+' - '+show_artist+'.mp3'
		print ("\t"+new_name+" tagged")
	else:
		print("No tag data found for "+to_tag_file)