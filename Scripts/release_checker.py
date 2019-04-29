import argparse
import requests
import sys
import time

# used if no arguments passed in command line
api_key = "<api key>"
season_id = "<yyyy-mm>"
poll_rate = 30
exit_code = 0

# create arg parser
parser = argparse.ArgumentParser()
parser.add_argument("-k", "--key")
parser.add_argument("-s", "--season")
parser.add_argument("-r", "--rate", type=int)
parser.add_argument("-e", "--exitcode", type=int)
args = parser.parse_args()

# check command line arguments
if args.key:
    api_key = args.key.strip()
if args.season:
    season_id = args.season
if args.rate:
    poll_rate = args.rate
if args.exitcode:
    exit_code = args.exitcode

# setup request parameters
headers = {"Accept": "application/json", "authorization": f"Bearer {api_key}"}
league_id = "29000022"  # legends league
base_url = f"https://api.clashofclans.com/v1/leagues/{league_id}/seasons/{season_id}?limit=1"
time_waited = 0
print("Checking...")


# poll
while True:
    r = requests.get(base_url, headers=headers)
    info_dict = r.json()
    print(info_dict)
    if len(info_dict["items"]) != 0:
        print("\n\nResults are out.")
        sys.exit(exit_code)
    else:
        t = poll_rate * (time_waited - 1)
        print(f"Still waiting... ({t})")
        time.sleep(poll_rate)
        time_waited += 1
