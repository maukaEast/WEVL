'''
Playlist scraper for WEVL's First Church of Rock

https://stackoverflow.com/questions/71545135/how-to-append-rows-with-concat-to-a-pandas-dataframe
https://datascientyst.com/compare-two-pandas-dataframes-get-differences/
https://stackoverflow.com/questions/20225110/comparing-two-dataframes-and-getting-the-differences
https://www.geeksforgeeks.org/how-to-compare-two-dataframes-with-pandas-compare/
https://www.statology.org/pandas-check-if-row-is-in-another-dataframe/
https://www.statology.org/pandas-select-rows-based-on-column-values/
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
'''
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

#- - setup variables and global uses
global Fulllist
global Heavylist

def compare_monkey():
	global Fulllist
	global Heavylist
	list_headings = ["artist","title","album","year","exists"]
	new_df = pd.DataFrame()
	
	Fulllist = pd.read_csv("test_list.csv",sep = ';')
	Heavylist = pd.read_csv("sm_list.csv",sep = ';')
	#merage and compare both lists
	all_df = pd.merge(Fulllist, Heavylist, on=["title","artist","year","album"], how='left', indicator='exists')
	all_df['exists'] = np.where(all_df.exists == 'both', True, False)
	#create list with just songs not on smaller list
	new_df= all_df.loc[all_df['exists'] == False]
	#remove comparison column and add placeholder for episode airdate
	new_df = new_df.drop(['exists'],axis=1)
	new_df.insert(0, 'play_date', '0_UNK_0')
	
	
	print("comparing csvs")
	new_df.to_csv('comparison.csv',sep=';')
	
	#with open('comparison.txt','w') as my_list_file:
	#	file_content = '\n'.join(all_df)
	#	my_list_file.write(file_content)
		
	print(new_df)
	
# MAIN FUNCTION
compare_monkey()

'''
'''