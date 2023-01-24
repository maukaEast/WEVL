''''
scripts to update audacity tags with data from scrape
https://methodmatters.github.io/editing-id3-tags-mp3-meta-data-in-python/
https://stackoverflow.com/questions/50575802/convert-dataframe-row-to-dict
'''
import os
import pandas as pd
import numpy as np
import eyed3

tag_file = "tags"
label_file = "labels"
mp3_list =[]
show_DB = pd.DataFrame()

DBase = pd.read_csv('offthe_recent.csv',sep=';',index_col=False)
DBase.drop(DBase.columns[0], axis=1, inplace=True)

all_files = os.listdir()
for x in all_files:
	if x.endswith('.mp3'):
		mp3_list.append(x[:-4])

#get label list text file from audacity and tag list file
for x in os.listdir():
	if x.endswith("_labels.txt"):
		print("label file found")
		label_file = x
	elif x.endswith("_tags.txt"):
		print("tag file found")
		tag_file = x

print(label_file+" "+tag_file)

for file in mp3_list:
	print (file)
	if DBase['Artist'].str.contains(file).any():
		#print("file found in DBase")
		the_values = DBase[(DBase['Artist']==file) & (DBase['show_date']=="Oct 23. 2022")]
		data_dict = the_values.to_dict()
		show_DB = show_DB.append(the_values, ignore_index=True)
		final_table = pd.concat([show_DB,the_values], axis=0)
		print(the_values) 	
	else:
		print("no details found for file: "+file)
print('final created database:')
print(final_table)
final_table.to_csv('Oct23_22.csv',sep=';',index=False)
