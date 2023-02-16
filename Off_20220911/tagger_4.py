''''
scripts to update audacity tags with data from scrape
https://methodmatters.github.io/editing-id3-tags-mp3-meta-data-in-python/
https://stackoverflow.com/questions/50575802/convert-dataframe-row-to-dict
https://stackoverflow.com/questions/15147751/how-to-check-if-all-items-in-a-list-are-there-in-another-list
#https://www.statology.org/pandas-get-index-of-row/
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

def list_contains(shortList, bigList):  #function to check if all items in one list are in another
	listToStr = ' '.join([str(elem) for elem in shortList])
	print("Search criteria: ",listToStr)
	lowList = [x.lower() for x in bigList]
	stopwords = ["a", "and", "&", "_", "in", "the"]
	low_contents = [word for word in lowList if word not in stopwords]
	with open(r'bigList.txt', 'w') as doc:
			for item in low_contents:
				doc.write("%s\n" % item)
	for names in lowList:
		print("Checking if",listToStr,"is a subset of",names)
		print(lowList.index(names))
		if(set(listToStr).issubset(set(names))):
			print("Confirming that",listToStr,"is subset of the main list")
			break
		#else:
		#	print("No subset found")
		#break	#exits loops when found.
	print("Comparison completed")
# ---- MP3 file processing function ---- #
def get_mp3s():
	all_files = os.listdir()
	cur_dir = os.getcwd().rsplit('\\',1)[-1]
	print("Show date:",cur_dir)
	print("")

	for x in all_files:
		if x.endswith('.mp3'):		#find and format each mp3 in the folder
			mp3_list.append(x[:-4])
			df = pd.DataFrame(data={"FileNames": mp3_list})
			df.to_csv(cur_dir+"mp3s.csv", sep=',',index=False)
# -- Utility to clear tags of all present MP3s in folder -- #			
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

# -- main program functions
main_scrape_list = "offthe_recent.csv"	#name the show database
if main_scrape_list:					#if it exists, create a Pandas Frame for it
	DBase = pd.read_csv('../'+main_scrape_list,sep=';',index_col=False)
	DBase.drop(DBase.columns[0], axis=1, inplace=True)
	print("Scrape list ",main_scrape_list,"accessed")
	print("")
else:
	print("No file found for that show")

get_mp3s()
for file in mp3_list:
	file_art, file_tit = [x.strip() for x in file.split("-")]
	print("Examining file:",file_tit,"by",file_art)
	#print(file_tit)
	#print(file_art)
	stopwords = ["a", "and", "&", "_", "in", "the"]
	art_contents = list(filter(lambda w: w not in stopwords, re.split(" ", file_art.lower())))
	tit_contents = list(filter(lambda w: w not in stopwords, re.split(" ", file_tit.lower())))
	print("Searching using artist name:",art_contents,"and title:",tit_contents)
    
	#Look over main show list and see if artist/title are in respective columns	
	for each in art_contents:
		Base_Art = list(DBase["Artist"])
		Base_Tit = list(DBase["Title"])
		if (list_contains(art_contents,Base_Art)):
			if (DBase['Artist'].str.contains(each,case=False).any()):
				print("artist name found as",each)
				found_artist = DBase.loc[DBase['Artist'].str.contains(each, case=False)]
			#found_artist gives list of all titles for that artist
			#maybe use same algorithm to search this list for the song title
		#if (list_contains(tit_contents,Base_Tit)):
		#	print(found_artist)
			
		#print(DBase['Artist'],DBase['Title'])
		#	tit_index = DBase.index[DBase['Title'] == file_tit].tolist()
		#	art_index = DBase.index[DBase['Artist'] == file_art].tolist()
		#	found_song_ind = list(set(tit_index).intersection(art_index))
		#	print(found_song_ind)
		
		#	base_title = DBase[DBase['Title']==file_tit]
		#	print(base_title)
		##	full_dict_title = full_values.to_dict()
		#	episode_DB = pd.concat([episode_DB,full_values], axis=0,ignore_index=True)
			#print(episode_DB)
	

	print('')
#print('')
#print('final created database row number:')
#print("\t"+str(episode_DB.shape[0]))
#print(episode_DB)
episode_DB.drop_duplicates(keep=False,inplace=True)
episode_DB.to_csv('Sep11_22.csv',sep=';',index=False)

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