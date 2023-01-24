''''
scripts to update audacity tags with data from scrape
https://methodmatters.github.io/editing-id3-tags-mp3-meta-data-in-python/
https://stackoverflow.com/questions/50575802/convert-dataframe-row-to-dict
'''
import os
import pandas as pd
import numpy as np
import eyed3

mp3_list =[]
show_DB = pd.DataFrame()

DBase = pd.read_csv('../offthe_recent.csv',sep=';',index_col=False)
DBase.drop(DBase.columns[0], axis=1, inplace=True)

all_files = os.listdir()
for x in all_files:
	if x.endswith('.mp3'):
		mp3_list.append(x[:-4])

for file in mp3_list:
	print (file)
	if DBase['Artist'].str.contains(file).any():
		the_values = DBase[(DBase['Artist']==file) & (DBase['show_date']=="Oct 23. 2022")]
		data_dict = the_values.to_dict()
		show_DB = pd.concat([show_DB,the_values], axis=0,ignore_index=True)
		#print(the_values) 	
	else:
		print("no details found for file: "+file)
print('')
#print('final created database:')
#print(show_DB)
show_DB.to_csv('Oct23_22.csv',sep=';',index=False)

#checking for index of given row
for i in range(0,show_DB.shape[0]):
	to_tag_name = str(mp3_list[i])
	to_tag_file = to_tag_name+'.mp3'
	#print("File data for "+to_tag_file)
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
		print ("Tag data at index "+str(i)+" extracted for file "+new_name)