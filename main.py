import requests

url = "https://api.fda.gov/drug/event.json?limit=2"

# url = 'https://api.fda.gov/drug/event.json?search=reactionmeddrapt:"headache"&limit=5'

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

level_of_serious_deathness = response.json()["results"][0]["seriousnessdeath"]

if level_of_serious_deathness == 1:
    print("ay dios mio")
else:
    print("you're chilling")



# http://localhost:5000/api/drug-checker