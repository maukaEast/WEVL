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
global Fullzig
global Indiezig

def compare_monkey():
	global Fullzig
	global Indiezig
	new_df = pd.DataFrame()
	
	Fullzig = pd.read_csv("fullziggy.csv")
	Fullzig = (Fullzig.replace(',','.', regex=True))
	Fullzig = Fullzig.drop(['Length','Genre','Rating','Bitrate','Path','Media'],axis=1)
	Fullzig.insert(0, 'show_date', '001100')
	Fullzig['show_date']=Fullzig['show_date'].astype(str)
	#Fullzig.drop(Fullzig.columns[0], axis=1, inplace=True)
	
	Indiezig = pd.read_csv("offthe_recent.csv",sep=';')
	Indiezig.drop(Indiezig.columns[0], axis=1, inplace=True)
	#format ziggy lists
		
	#Indiezig = Indiezig.drop(['Length','Genre','Rating','Bitrate','Path','Media'],axis=1)
	print(Indiezig.columns.tolist())
	print(Fullzig.columns.tolist())	
	#merage and compare both lists
	all_df = pd.merge(Fullzig, Indiezig, on=['show_date', 'Title','Artist','Album','Year'], how='left', indicator='exists')

#add column to show if each row in first DataFrame exists in second
	all_df['exists'] = np.where(all_df.exists == 'both', True, False)
	new_df = all_df[all_df['exists']==True]
	#drop assists columns
	#all_df = all_df.drop('exists', axis=1)
	print("comparing csvs")
	new_df.to_csv('comparison.csv',sep=';')
	
# MAIN FUNCTION
compare_monkey()