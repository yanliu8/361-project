import numpy as np 
import json
stats = ["winner","champLevel","kills","doubleKills","tripleKills","quadraKills","pentaKills","unrealKills","largestKillingSpree","deaths","assists","totalDamageDealt","totalDamageDealtToChampions","totalDamageTaken","largestCriticalStrike","totalHeal","minionsKilled","neutralMinionsKilled","neutralMinionsKilledTeamJungle","neutralMinionsKilledEnemyJungle","goldEarned","goldSpent","magicDamageDealtToChampions","physicalDamageDealtToChampions","trueDamageDealtToChampions","visionWardsBoughtInGame","sightWardsBoughtInGame","magicDamageDealt","physicalDamageDealt","trueDamageDealt","magicDamageTaken","physicalDamageTaken","trueDamageTaken","firstBloodKill","firstBloodAssist","firstTowerKill","firstTowerAssist","firstInhibitorKill","firstInhibitorAssist","inhibitorKills","towerKills","wardsPlaced","wardsKilled","largestMultiKill","killingSprees","totalUnitsHealed","totalTimeCrowdControlDealt"]
permin = ["creepsPerMinDeltas", "xpPerMinDeltas", "goldPerMinDeltas", "csDiffPerMinDeltas", "xpPerMinDeltas", "damageTakenPerMinDeltas", "damageTakenDiffPerMinDeltas"]
time = ["zeroToTen", "tenToTwenty", "twentyToThirty", "thirtyToEnd"]
def load_champion_id():
	championId = {}
	with open('simple_champions.dat') as jsonfile:
		for row in jsonfile:
			championId = json.loads(row)
	return championId
def rank_time_line(rankItem, championId):
	champs = {}
	if rankItem not in permin:
		print("The input is not in time line")
		return
	for t in time:
		champs[t] = {}
	for i in range(1,11):
		filename = 'matches/matches'+str(i)+'.json'
		matches = open(filename, encoding="ISO-8859-1")
		totalmatches = json.load(matches)
		totalmatches = totalmatches["matches"]
		for match in totalmatches:
			for player in match["participants"]:
				champ = player["championId"]
				timeline = player["timeline"]
				if rankItem in timeline:
					for t in time:
						if t in timeline[rankItem]:
							if champ not in champs[t]:
								champs[t][champ] = []
							champs[t][champ].append(float(timeline[rankItem][t]))
		matches.close()
	total = {}
	final_rank_list = []
	for t in time:
		for champ in champs[t]:
			champs[t][champ] = sum(champs[t][champ])/len(champs[t][champ])
			if champ not in total:
				total[champ] = []
			total[champ].append(champs[t][champ])
		final_rank = sorted(champs[t], key=champs[t].__getitem__, reverse = True)
		final_rank_list.append(final_rank)
		print("The top 5 champions in " + rankItem + " in time period " + t + " are")
		for i in range(5):
			print(championId[str(final_rank[i])] + " : " + str(champs[t][final_rank[i]]))
	for champ in total:
		total[champ] = sum(total[champ])/len(total[champ])
	print("The top 5 champions in " + rankItem + " in total are")
	final_total_rank = sorted(total, key=total.__getitem__, reverse = True)
	for i in range(5):
		print(championId[str(final_total_rank[i])] + " : " + str(total[final_total_rank[i]]))
	final_rank_list.append(final_total_rank)
	return final_rank_list





def rank_stats(rankItem, championId):
	
	if rankItem not in stats:
		print("the input is not in stats")
		return
	champs = {}
	for i in range(1,11):
		filename = 'matches/matches'+str(i)+'.json'
		matches = open(filename, encoding="ISO-8859-1")
		totalmatches = json.load(matches)
		totalmatches = totalmatches["matches"]
		for match in totalmatches:
			for player in match["participants"]:
				champ = player["championId"]
				playerstats = player["stats"]
				if champ not in champs:
					champs[champ] = []
				
				champs[champ].append(float(playerstats[rankItem]))
		matches.close()
	for champ in champs:
		champs[champ] = sum(champs[champ])/len(champs[champ])
	ranked_stats = sorted(champs, key=champs.__getitem__, reverse = True)
	for i in range(5):
		print(championId[str(ranked_stats[i])] + " : " + str(champs[ranked_stats[i]]))

	return ranked_stats


def champion_data(champion_name, rankItem, championId):
	champion_id = ''
	valid_champ = False
	for champ in championId:
		if championId[champ] == champion_name:
			champion_id = champ
			valid_champ = True
			break
	if not valid_champ:
		print("champion does not exist!")
		return
	if rankItem in permin:
		champs = {}
		for t in time:
			champs[t] = {}
		for i in range(1,11):
			filename = 'matches/matches'+str(i)+'.json'
			matches = open(filename, encoding="ISO-8859-1")
			totalmatches = json.load(matches)
			totalmatches = totalmatches["matches"]
			for match in totalmatches:
				for player in match["participants"]:
					champ = player["championId"]
					timeline = player["timeline"]
					if rankItem in timeline:
						for t in time:
							if t in timeline[rankItem]:
								if champ not in champs[t]:
									champs[t][champ] = []
								champs[t][champ].append(float(timeline[rankItem][t]))
			matches.close()
		total = {}
		final_rank_list = []
		for t in time:
			for champ in champs[t]:
				champs[t][champ] = sum(champs[t][champ])/len(champs[t][champ])
				if champ not in total:
					total[champ] = []
				total[champ].append(champs[t][champ])
			final_rank = sorted(champs[t], key=champs[t].__getitem__, reverse = True)
			if int(champion_id) not in final_rank:
				continue
			rank = final_rank.index(int(champion_id)) + 1
			print('during time ' + t + ' ' + champion_name+' is rank '+ str(rank)+ ': '+str(champs[t][int(champion_id)]))
	if rankItem in stats:
		duration = [{},{},{},{}, {}]
		for i in range(1,11):
			filename = 'matches/matches'+str(i)+'.json'
			matches = open(filename, encoding="ISO-8859-1")
			totalmatches = json.load(matches)
			totalmatches = totalmatches["matches"]

			for match in totalmatches:
				match_duration = match["matchDuration"]
				index = 0
				if match_duration > 1500:
					index = 1
				if match_duration > 1800:
					index = 2
				if match_duration > 2100:
					index = 3
				if match_duration > 2400:
					index = 4

				for player in match["participants"]:
					champ = player["championId"]
					playerstats = player["stats"]
					if champ not in duration[index]:
						duration[index][champ] = []
				
					duration[index][champ].append(float(playerstats[rankItem]))
		matches.close()
	temp = ["<25", "25-30", "30-35", "35-40",">40"]
	for i in range(5):
		for champ in duration[i]:
			if len(duration[i][champ]) == 0:
				duration[i][champ] = 0
				continue
			duration[i][champ] = sum(duration[i][champ])/len(duration[i][champ])
		rank = sorted(duration[i], key=duration[i].__getitem__, reverse = True).index((int(champion_id)))
		print("In games " + temp[i] + " " + champion_name + " is rank" + str(rank)+ ': ' + str(duration[i][int(champion_id)]))


if __name__ == "__main__":
	championId = load_champion_id()
	while 1:
		arg = input("Do you want rank of timeline data, rank of total stats or data of champion\n")
		if arg == "timeline":
			arg2 = input("please type in the detailed category\n")
			rank_time_line(arg2, championId)
		elif arg == "stats":
			arg2 = input("please type in the detailed category\n")
			rank_stats(arg2, championId)
		elif arg == "exit":
			break
		elif arg == "champion":
			arg2 = input("please type in the champion name\n")
			arg3 = input("please type in the detailed category\n")
			champion_data(arg2, arg3, championId)
		else:
			print("legal input: timeline, stats, exit\n")

