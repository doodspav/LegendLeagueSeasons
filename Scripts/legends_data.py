import argparse
import MySQLdb
import requests

# used if no arguments passed in command line
api_key = "<api key>"
database = "<db name>"
table = "<table name>"
season_id = "<yyyy-mm>"

# create arg parser
parser = argparse.ArgumentParser()
parser.add_argument("-k", "--key")
parser.add_argument("-d", "--database")
parser.add_argument("-t", "--table")
parser.add_argument("-s", "--season")
args = parser.parse_args()

# check command line arguments
if args.database:
    database = args.database
if args.table:
    table = args.table
if args.season:
    season_id = args.season
if args.key:
    api_key = args.key.strip()

# create database connection
db = MySQLdb.connect(host="localhost", user="root", passwd="", db=database, charset="utf8mb4")
db.autocommit(True)
cur = db.cursor()

# create/replace table
query = f"DROP TABLE IF EXISTS `{table}`"
cur.execute(query)
query = f"CREATE TABLE `{table}` (rank INT(10),trophies INT(5),tag VARCHAR(15),name VARCHAR(30),expLevel INT(4),attackWins INT(8),defenseWins INT(8),clanTag VARCHAR(15),clanName VARCHAR(30),clanBadgeURL VARCHAR(60)) CHARACTER SET utf8mb4"
cur.execute(query)

# setup request parameters
headers = {"Accept": "application/json", "authorization": f"Bearer {api_key}"}
league_id = "29000022"  # legends league
base_url = f"https://api.clashofclans.com/v1/leagues/{league_id}/seasons/{season_id}"
info = []


def get_info(url, headers, limit=10000, cursor=None):
    global info

    # finish
    if cursor == "finished":
        print("Finished data collection.")
        return

    # make request
    new_url = f"{url}?limit={limit}"
    if cursor is not None:
        new_url += f"&after={cursor}"
    r = requests.get(new_url, headers=headers)

    # parse results
    info_dict = r.json()
    len_items = len(info_dict["items"])
    info += (info_dict["items"])
    if "after" in info_dict["paging"]["cursors"].keys():
        new_cursor = info_dict["paging"]["cursors"]["after"]
    else:
        new_cursor = "finished"

    # print update and recurse
    print(f"Done {len(info)}.")
    get_info(url, headers, cursor=new_cursor)


get_info(base_url, headers)
len_info = len(info)
print(f"Total: {len_info}.")

# parse info into table
for j in range(len_info):
    i = info[j]
    query = f"INSERT INTO `{table}` (`rank`,`trophies`,`tag`,`name`,`expLevel`,`attackWins`,`defenseWins`,`clanTag`,`clanName`,`clanBadgeURL`) "
    query += " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    tup_list = [i["rank"],i["trophies"],i["tag"],i["name"],i["expLevel"],i["attackWins"],i["defenseWins"]]
    if "clan" in i.keys():
        cbu = i["clan"]["badgeUrls"]["small"][46:-4]
        tup_list += [i["clan"]["tag"],i["clan"]["name"],cbu]
    else:
        tup_list += [None, None, None]
    tup = tuple(tup_list)

    # execute queries and print progress
    cur.execute(query, tup)
    if j % 10000 == 0:
        print(f"Done {j}.")

print(f"Done {len_info}.")
print("Fully finished.")
