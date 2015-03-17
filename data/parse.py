import csv
import pandas as pd
import numpy as np

def computeStats(win_rec, lose_rec):
	win_rec_sum = win_rec.sum()
	lose_rec_sum = lose_rec.sum()

	total_games = float(len(win_rec) + len(lose_rec))

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

	pospg = pos / total_games

	efg = (fgm + 0.5*fgm3) / fga
	opp_efg = (opp_fgm + 0.5*opp_fgm3) / opp_fga

	ts = pts / (2*(fga + 0.475*fta))
	opp_ts = opp_pts / (2*(opp_fga + 0.475*opp_fta))

	a_rate = (win_rec_sum.wast + lose_rec_sum.las) / float(fgm)
	ft_rate = fta / float(fga)

	ppg = pts / total_games
	opp_ppg = opp_pts / total_games
	apg = (win_rec_sum.wast + lose_rec_sum.las) / total_games
	rpg = (orb + win_rec_sum.wdr + lose_rec_sum.ldr) / total_games
	orpg = orb / total_games
	bpg = (win_rec_sum.wblk + lose_rec_sum.lblk) / total_games
	spg = (win_rec_sum.wstl + lose_rec_sum.lstl) / total_games
	topg = (win_rec_sum.wto + lose_rec_sum.lto) / total_games
	pfpg = (win_rec_sum.wpf + lose_rec_sum.lpf) / total_games

	return [ortg, drtg, pospg, efg, opp_efg, ts, opp_ts, a_rate, ft_rate, ppg, opp_ppg, apg, rpg, orpg, bpg, spg, topg, pfpg]

def __main__(): 
	data = pd.read_csv('regular_season_detailed_results_2015.csv')
	teams = pd.read_csv('teams.csv', index_col = 1)
	ratings = pd.read_csv('massey_ordinals_2015.csv')

	# check = 'Duke'

	# print computeStats(data[data.wteam==teams.loc[check,'team_id']], data[data.lteam==teams.loc[check,'team_id']])
	# print len(data[data.wteam==teams.loc[check,'team_id']]), len(data[data.lteam==teams.loc[check,'team_id']])
	# print data[data.wteam==teams.loc[check,'team_id']].lteam.values
	# print ratings[ratings.team==teams.loc[check,'team_id']]

	for i in xrange(5200, 5250):#len(data)):
		#print teams.loc[data.loc[i, 'wteam'], 'team_name'], teams.loc[data.loc[i, 'lteam'], 'team_name']
		if i%100 == 0:
			print i

		game = data.loc[i]

		#team a
		a_win_rec = data[(data.wteam == game.wteam) & (data.daynum < game.daynum)]
		a_lose_rec = data[(data.lteam == game.wteam) & (data.daynum < game.daynum)]

		a_stats = computeStats(a_win_rec, a_lose_rec)

		a_ranking = ratings[(ratings.team == game.wteam) & (ratings.rating_day_num < game.daynum) & (ratings.rating_day_num >= (game.daynum-7))].mean().orank

		a_opp_teams = np.append(a_win_rec.lteam.values, a_lose_rec.lteam.values)
		a_opp_rankings = ratings[(ratings.team.isin(a_opp_teams)) & (ratings.rating_day_num < game.daynum) & (ratings.rating_day_num >= (game.daynum-7))].mean().orank

		#team b
		b_win_rec = data[(data.wteam == game.lteam) & (data.daynum < game.daynum)]
		b_lose_rec = data[(data.lteam == game.lteam) & (data.daynum < game.daynum)]

		b_stats = computeStats(b_win_rec, b_lose_rec)

		b_ranking = ratings[(ratings.team == game.wteam) & (ratings.rating_day_num < game.daynum) & (ratings.rating_day_num >= (game.daynum-7))].mean().orank

		b_opp_teams = np.append(b_win_rec.lteam.values, b_lose_rec.lteam.values)
		b_opp_rankings = ratings[(ratings.team.isin(b_opp_teams)) & (ratings.rating_day_num < game.daynum) & (ratings.rating_day_num >= (game.daynum-7))].mean().orank


if __name__ == '__main__':
	__main__()