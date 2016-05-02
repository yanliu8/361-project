import numpy as np 
import json
from sklearn.ensemble import RandomForestClassifier
def verify(filenumber):
	tier = ["UNRANKED", "BRONZE", "SILVER", "GOLD", "PLATINUM", "DIAMOND", "CHALLENGER", "MASTER"]
	data = []
	Class = []
	testdata = []
	testClass = []
	for i in range(1,11):
		filename = 'matches/matches'+str(i)+'.json'
		matches = open(filename, encoding="ISO-8859-1")
		totalmatches = json.load(matches)
		totalmatches = totalmatches["matches"]
		for match in totalmatches:
			if match["queueType"] != "RANKED_SOLO_5x5":
				continue
			duration = match["matchDuration"]
			for player in match["participants"]:
				new_data = []
				new_data.append(duration)
				new_data.append(player["spell1Id"])
				new_data.append(player["spell2Id"])
				if i == filenumber:
					testClass.append(player["championId"])
				else:
					Class.append(player["championId"])
				#new_data.append(player["championId"])
				#if i == 10:
				# 	testClass.append(tier.index(player["highestAchievedSeasonTier"]))
				#else:
				# 	Class.append(tier.index(player["highestAchievedSeasonTier"]))
				timeline = player["timeline"]
				permin = ["creepsPerMinDeltas", "xpPerMinDeltas", "goldPerMinDeltas", "csDiffPerMinDeltas", "xpPerMinDeltas", "damageTakenPerMinDeltas", "damageTakenDiffPerMinDeltas"]
				for item in permin:
					if item not in timeline:
						new_data += [0,0,0,0]
						continue
					new_data.append(timeline[item].get("zeroToTen", 0))
					new_data.append(timeline[item].get("tenToTwenty", 0))
					new_data.append(timeline[item].get("twentyToThirty", 0))
					new_data.append(timeline[item].get("thirtyToEnd", 0))
				role = ["NONE", "SOLO", "DUO_CARRY","DUO_SUPPORT", "DUO"]
				new_data.append(role.index(timeline["role"]))
				#if i == 10:
				#	testClass.append(role.index(timeline["role"]))
				#else:
				#	Class.append(role.index(timeline["role"]))
				lane = ["TOP", "JUNGLE", "BOTTOM", "MIDDLE"]
				new_data.append(lane.index(timeline["lane"]))
				stats = player["stats"]
				for stat in stats:
					new_data.append(stats[stat])
				if i == filenumber:
					testdata.append(new_data)
	
				else:
					data.append(new_data)
		matches.close()
	data = np.array(data)
	Class = np.array(Class)
	print('done loading data')
	print(data.shape)
	print("The accuracy of crossvalidation "+str(filenumber)+" is")
	randomForest = RandomForestClassifier(n_estimators = 500, min_samples_leaf = 10)
	randomForest.fit(data, Class)
	print(randomForest.score(testdata, testClass))
	
if __name__ == "__main__":
	for i in range(1,11):
		verify(i)
	
