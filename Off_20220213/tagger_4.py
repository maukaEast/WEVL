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
import csv

eyed3.log.setLevel("ERROR")	#this disables known bug in eye3d error reporting

mp3_list =[]
show_DB = pd.DataFrame()
episode_DB = pd.DataFrame()

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
			#print("terms ",List2,"found in column")
			return True 
def clear_tags():
	audiofile = eyed3.load(to_tag_file)
	audiofile.tag.artist = "UNK"
	audiofile.tag.album = "UNK"
	audiofile.tag.album_artist = "UNK"
	audiofile.tag.title = "UNK"
	audiofile.tag.genre = "UNK"
		#audiofile.tag.release-year = show_date
	audiofile.tag.save()
	print("Tags Cleared")
	
main_scrape_list = "offthe_recent.csv"	#name the show database
if main_scrape_list:					#if it exists, create a Pandas Frame for it
	DBase = pd.read_csv('../'+main_scrape_list,sep=';',index_col=False)
	DBase.drop(DBase.columns[0], axis=1, inplace=True)
	print("Scrape list accessed")
else:
	print("No file found for that show")

# ---- MP3 file processing ---- #
	
all_files = os.listdir()
for x in all_files:
	if x.endswith('.mp3'):		#find and format each mp3 in the folder
		mp3_list.append(x[:-4])
		df = pd.DataFrame(data={"col1": mp3_list})
		df.to_csv("Off_20220213_mp3s.csv", sep=',',index=False)

for file in mp3_list:
#look at each songfile in mp3 list and make search criteria from name omitting "a", "the", &c.
	file_title = [x.strip() for x in file.split("-")][0]
	print("The title of the song file is: ",file_title)
	art_list, tit_list = [x.strip() for x in file.split("-")]
	print(art_list)
	print(tit_list)
	stopwords = ["a", "and", "&", "_", "the"]
	art_contents = list(filter(lambda w: w not in stopwords, re.split(" ", art_list.lower())))
	tit_contents = list(filter(lambda w: w not in stopwords, re.split(" ", tit_list.lower())))
	#print("Search parameters for "+file+" artist name: ",art_contents," and title: ",tit_contents)
		
	if ( (list_contains(DBase['Artist'],art_contents)), (list_contains(DBase['Title'],tit_contents)) ):
		print("Both criteria are valid for this MP3 file")
		print(DBase['Artist'],DBase['Title'])
		full_values = DBase[(DBase['Title']==file_title) & (DBase['show_date']=="Dec 4. 2022 ")]
		full_dict_title = full_values.to_dict()
		print(type(full_dict_title))
		print(full_dict_title)
		episode_DB = pd.concat([episode_DB,full_values], axis=0,ignore_index=True)
	else:
		print("One or both criteria are not valid for this file")
	print('')
#print('')
#print('final created database row number:')
#print("\t"+str(episode_DB.shape[0]))
#print(episode_DB)
episode_DB.drop_duplicates(keep=False,inplace=True)
episode_DB.to_csv('Dec04_22.csv',sep=';',index=False)

# --- TAGGING FUNCTION --- #
#looking at main DB. possible why are getting doubles
for i in range(0,episode_DB.shape[0]):	#checking for index of given row
	to_tag_name = str(mp3_list[i])
	to_tag_file = to_tag_name+'.mp3'
	#print("File data for "+to_tag_file+" at index "+str(i))
	#print('')
	#print("Attempting to tag "+to_tag_file)
	#print("from database"+str(show_DB.iloc[i]))
	if episode_DB.iloc[i]['Artist']== to_tag_name:
		show_artist = episode_DB.iloc[i]['Artist']
		show_title = episode_DB.iloc[i]['Title']
		show_album = episode_DB.iloc[i]['Album']
		show_date = episode_DB.iloc[i]['Year']
		
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