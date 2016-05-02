import json
champs = {}
with open('champion.dat') as jsonfile:
	for item in jsonfile:
		data = json.loads(item)["data"]
		for champ in data:
			champs[data[champ]["key"]] = champ
with open('simple_champions.dat', 'w') as output:
	json.dump(champs, output)
