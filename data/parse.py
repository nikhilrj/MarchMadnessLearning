import csv
import pandas as pd

def __main__(): 
	data = pd.read_csv('regular_season_detailed_results_2015.csv')
	teams = pd.read_csv('teams.csv', index_col = 0)
	#print data[(data.wteam==1103) & (data.wloc=='H')]
	#print data.loc[(data.wteam==1103) & (data.daynum<20)].mean()
	print data.loc[(data.wteam==1103) & (data.daynum<=20)]


if __name__ == '__main__':
	__main__()