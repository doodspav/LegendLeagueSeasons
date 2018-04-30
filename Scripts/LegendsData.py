import MySQLdb, requests

database = "<put db name here>"
#table name will just be the season_id

db = MySQLdb.connect(host="localhost", user="root", passwd="", db=database, charset="utf8mb4")
db.autocommit(True)
cur = db.cursor()

api_key = "<put key here>"
headers = {"Accept":"application/json","authorization":"Bearer "+api_key}
season_id = "yyyy-mm"
league_id = "29000022" #legends league
base_url = "https://api.clashofclans.com/v1/leagues/%s/seasons/%s" % (league_id,season_id)
info = []

query = "DROP TABLE `%s`" % season_id
try:
    cur.execute(query)
except:
    pass
query = "CREATE TABLE `%s` (rank INT(10),trophies INT(5),tag VARCHAR(15),name VARCHAR(30),expLevel INT(4),attackWins INT(8),defenseWins INT(8),clanTag VARCHAR(15),clanName VARCHAR(30),clanBadgeURL VARCHAR(60)) CHARACTER SET utf8mb4" % season_id
cur.execute(query)

def getInfo(url, headers, limit=10000, cursor=None):
    #DONT SET THE LIMIT TO ALL OF THEM (ie no limit)
    global info
    if cursor == "finished":
        return
        print("Finished data collection.")
    new_url = url + "?limit=%s" % limit
    if cursor != None:
        new_url += "&after=%s" % cursor
    r = requests.get(new_url, headers=headers)
    info_dict = r.json()
    lid = len(info_dict["items"])
    info += (info_dict["items"])
    if "after" in info_dict["paging"]["cursors"].keys():
        new_cursor = info_dict["paging"]["cursors"]["after"]
    else:
        new_cursor = "finished"
    print("Done %s." % len(info))
    if lid != limit and new_cursor != "finished":
        print("Limit: %s     Results: %s" % (limit,lid))
    getInfo(url,headers,cursor=new_cursor)

getInfo(base_url,headers)
print(len(info))
leninfo = len(info)

for j in range(leninfo):
    i = info[j]
    query = "INSERT INTO `%s` (`rank`,`trophies`,`tag`,`name`,`expLevel`,`attackWins`,`defenseWins`,`clanTag`,`clanName`,`clanBadgeURL`) " % season_id
    query += " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    tuplist = [i["rank"],i["trophies"],i["tag"],i["name"],i["expLevel"],i["attackWins"],i["defenseWins"]]
    if "clan" in i.keys():
        cbu = i["clan"]["badgeUrls"]["small"][46:-4]
        tuplist += [i["clan"]["tag"],i["clan"]["name"],cbu]
    else:
        tuplist += [None,None,None]
    tup = tuple(tuplist)
    cur.execute(query,tup)
    if j%10000 == 0:
        print("Done %s." % j)

print("Fully finished.")
