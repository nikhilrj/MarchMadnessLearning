import csv
import pandas as pd
import numpy as np

def computeRatings(win_rec, lose_rec):
	win_rec_sum = win_rec.sum()
	lose_rec_sum = lose_rec.sum()

	#team's FGA / FTA
	fga = win_rec_sum.wfga + lose_rec_sum.lfga
	fgm = win_rec_sum.wfgm + lose_rec_sum.lfgm
	fgm3 = win_rec_sum.wfgm3 + lose_rec_sum.lfgm3
	fta = win_rec_sum.wfta + lose_rec_sum.lfta

	#opponent's FGA / FTA
	opp_fga = win_rec_sum.lfga + lose_rec_sum.wfga
	opp_fgm = win_rec_sum.lfgm + lose_rec_sum.wfgm
	opp_fgm3 = win_rec_sum.lfgm3 + lose_rec_sum.wfgm3
	opp_fta = win_rec_sum.lfta + lose_rec_sum.wfta

	#team's or/ to/ pts
	orb = win_rec_sum.wor + lose_rec_sum.lor
	to = win_rec_sum.wto + lose_rec_sum.lto
	pts = win_rec_sum.wscore + lose_rec_sum.lscore

	#opponent's or/ to/ pts
	opp_orb = win_rec_sum.lor + lose_rec_sum.wor
	opp_to = win_rec_sum.lto + lose_rec_sum.wto
	opp_pts = win_rec_sum.lscore + lose_rec_sum.wscore


	pos = 0.5*(fga + 0.475*fta - orb + to) + 0.5*(opp_fga + 0.475*opp_fta - opp_orb + opp_to)

	ortg = 100*pts/pos
	drtg = 100*opp_pts/pos

	efg = (fgm + 0.5*fgm3) / fga
	opp_efg = (opp_fgm + 0.5*opp_fgm3) / opp_fga

	return [ortg, drtg, efg, opp_efg]

def __main__(): 
	data = pd.read_csv('regular_season_detailed_results_2015.csv')
	teams = pd.read_csv('teams.csv', index_col = 1)
	ratings = pd.read_csv('massey_ordinals_2015.csv')

	print ratings

	result = pd.DataFrame(columns=('result', 'ortg_spread', 'drtg_spread'))
	#print data[(data.wteam==1103) & (data.wloc=='H')]
	#print data.loc[(data.wteam==1103) & (data.daynum<20)].mean()
	#print data.loc[(data.wteam==1103) & (data.daynum<=20)]

	#check = 'Texas'

	#print computeRatings(data[data.wteam==teams.loc[check,'team_id']], data[data.lteam==teams.loc[check,'team_id']])
	#print len(data[data.wteam==teams.loc[check,'team_id']]), len(data[data.lteam==teams.loc[check,'team_id']])

	for i in xrange(1000, 1150):#len(data)):
		#print teams.loc[data.loc[i, 'wteam'], 'team_name'], teams.loc[data.loc[i, 'lteam'], 'team_name']
		if i%100 == 0:
			print i

		game = data.loc[i]

		a_win_rec = data[(data.wteam == game.wteam) & (data.daynum < game.daynum)]
		a_lose_rec = data[(data.lteam == game.wteam) & (data.daynum < game.daynum)]

		a_ratings = computeRatings(a_win_rec, a_lose_rec)


		#print rec

		b_win_rec = data[(data.wteam == game.lteam) & (data.daynum < game.daynum)]
		b_lose_rec = data[(data.lteam == game.lteam) & (data.daynum < game.daynum)]

		b_ratings = computeRatings(b_win_rec, b_lose_rec)

if __name__ == '__main__':
	__main__()