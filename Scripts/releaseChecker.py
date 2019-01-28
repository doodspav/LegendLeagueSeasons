import requests
import time
import sys

api_key = "<put key here>"
headers = {"Accept":"application/json","authorization":"Bearer "+api_key}
season_id = "yyyy-mm"
league_id = "29000022" #legends league
base_url = "https://api.clashofclans.com/v1/leagues/%s/seasons/%s" % (league_id,season_id)
limit = 10
base_url += "?limit=%s" % limit

time_waited = 0

print("Checking...")

while True:
	r = requests.get(base_url, headers=headers)
	info_dict = r.json()
	if len(info_dict["items"]) != 0:
		break
	else:
		time.sleep(30)
		time_waited += 1
		print("Still waiting... (%s)" % (30*time_waited))

print("\n\n RESULTS ARE OUT!!!")
sys.exit(99)  # this is just so i have a unique code to be picked up by bash script
