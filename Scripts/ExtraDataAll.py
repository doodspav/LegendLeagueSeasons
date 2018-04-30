import MySQLdb, requests
from urllib import quote_plus
import threading
import time

database = "<put db name here>"
table = "<put table name here>" #table created using LegendsData.py
new_table = "<put table name here>"
sleep = 2 #raise this if thread count is getting too high or you get max files open erno 24 error
api_keys = [] #use more api keys if you get 429 errors

db = MySQLdb.connect(host="localhost", user="root", passwd="", db=database, charset="utf8mb4")
db.autocommit(True)
cur = db.cursor()

try:
    cur.execute("DROP TABLE `%s`" % new_table)
except:
    pass
start = "CREATE TABLE `%s` (" % new_table
end = ") CHARACTER SET utf8mb4"
i,v = "INT","VARCHAR"
fields1 = [("bestTrophies",i,5),
          ("bestVersusTrophies",i,5),
          ("tag",v,15),
          ("townHallLevel",i,2),
          ("builderHallLevel",i,2),
          ("versusBattleWins",i,8),
          ("warStars",i,5)]
fields2 = [("legendTrophies",i,5),
          ("bestSeasonID",v,7),
          ("bestSeasonRank",i,10),
          ("bestSeasonTrophies",i,5),
          ("previousSeasonID",v,7),
          ("previousSeasonRank",i,10),
          ("previousSeasonTrophies",i,5),
          ("bestVersusSeasonID",v,7),
          ("bestVersusSeasonRank",i,10),
          ("bestVersusSeasonTrophies",i,5),
          ("previousVersusSeasonID",v,7),
          ("previousVersusSeasonRank",i,10),
          ("previousVersusSeasonTrophies",i,5),]
troops = ['Barbarian', 'Archer', 'Goblin', 'Giant', 'Wall Breaker', 'Balloon', 'Wizard', 'Healer', 'Dragon', 'P.E.K.K.A', 'Minion', 'Hog Rider', 'Valkyrie', 'Golem', 'Witch', 'Lava Hound', 'Bowler', 'Baby Dragon Day', 'Miner', 'Raged Barbarian', 'Sneaky Archer', 'Beta Minion', 'Boxer Giant', 'Bomber', 'Super P.E.K.K.A', 'Cannon Cart', 'Drop Ship', 'Baby Dragon Night', 'Night Witch']
spells = ['Lightning Spell', 'Healing Spell', 'Rage Spell', 'Jump Spell', 'Freeze Spell', 'Poison Spell', 'Earthquake Spell', 'Haste Spell', 'Clone Spell', 'Skeleton Spell']
heroes = ['Barbarian King', 'Archer Queen', 'Grand Warden', 'Battle Machine']
achievements = [('Bigger Coffers', 2), ('Get those Goblins!', 3), ('Bigger & Better', 2), ('Nice and Tidy', 5), ('Release the Beasts', 1), ('Gold Grab', 10), ('Elixir Escapade', 10), ('Sweet Victory!', 5), ('Empire Builder', 1), ('Wall Buster', 7), ('Humiliator', 7), ('Union Buster', 7), ('Conqueror', 7), ('Unbreakable', 6), ('Friend in Need', 10), ('Mortar Mauler', 7), ('Heroic Heist', 10), ('League All-Star', 2), ('X-Bow Exterminator', 7), ('Firefighter', 7), ('War Hero', 5), ('Treasurer', 12), ('Anti-Artillery', 7), ('Sharing is caring', 10), ('Keep your village safe', 1), ('Master Engineering', 2), ('Next Generation Model', 1), ('Un-Build It', 7), ('Champion Builder', 5), ('High Gear', 1), ('Hidden Treasures', 1), ('Games Champion', 10)]

def camelCase(string):
    string = string.replace("&","and").replace("-"," ").replace(".","").replace("!","")
    words = string.split()
    words = [w.title() for w in words]
    words[0] = words[0].lower()
    if len(words[0]) == 1:
        words[1] = words[1].lower()
    string = "".join(words)
    return string

fields = fields1+fields2+troops+spells+heroes+achievements
for i in range(len(fields)):
    f = fields[i]
    if type(f) == str:
        fields[i] = (camelCase(f),"INT",2)
    elif len(f) == 2:
        fields[i] = (camelCase(f[0]),"INT",f[1])

for f in fields:
    start += "%s %s(%s)," % f
start = start[:-1]
query = start+end
cur.execute(query)

headers = []
for key in api_keys:
    header = {"Accept":"application/json","authorization":"Bearer "+key}
    headers.append(header)
lenheaders = len(headers)
tags = []

cur.execute("SELECT `tag` FROM `%s`" % table)
for row in cur.fetchall():
    tags.append(row[0])

print("Number of tags: %s" % len(tags))

extras = {}

def addExtra(tag,i):
    global extras
    try:
        ih = i%lenheaders
        header = headers[ih]
        url = "https://api.clashofclans.com/v1/players/" + quote_plus(tag)
        r = requests.get(url, headers=header)
        if r.status_code == 200:
            pass
        else:
            if r.status_code != 404:
                print(r.status_code)
            extras[tag] = None
            return
        p = r.json()
        tuplist = []
        for f in fields1:
            try:
                value = p[f[0]]
            except:
                continue
            try:
                value = int(value)
            except:
                pass
            tup = (f[0],value)
            tuplist.append(tup)
        if "legendStatistics" in p.keys():
            pls = p["legendStatistics"]
            if "legendTrophies" in pls.keys():
                tuplist.append(("legendTrophies",pls["legendTrophies"]))
            if "bestSeason" in pls.keys():
                plsbs = pls["bestSeason"]
                tuplist.append(("bestSeasonID",plsbs["id"]))
                tuplist.append(("bestSeasonRank",int(plsbs["rank"])))
                tuplist.append(("bestSeasonTrophies",int(plsbs["trophies"])))
            if "previousSeason" in pls.keys():
                plsbs = pls["previousSeason"]
                tuplist.append(("previousSeasonID",plsbs["id"]))
                tuplist.append(("previousSeasonRank",int(plsbs["rank"])))
                tuplist.append(("previousSeasonTrophies",int(plsbs["trophies"])))
            if "bestVersusSeason" in pls.keys():
                plsbs = pls["bestVersusSeason"]
                tuplist.append(("bestVersusSeasonID",plsbs["id"]))
                tuplist.append(("bestVersusSeasonRank",int(plsbs["rank"])))
                tuplist.append(("bestVersusSeasonTrophies",int(plsbs["trophies"])))
            if "previousVersusSeason" in pls.keys():
                plsbs = pls["previousVersusSeason"]
                tuplist.append(("previousVersusSeasonID",plsbs["id"]))
                tuplist.append(("previousVersusSeasonRank",int(plsbs["rank"])))
                tuplist.append(("previousVersusSeasonTrophies",int(plsbs["trophies"])))
        trp = p["troops"]
        trpd = {}
        for tr in trp:
            if tr["name"] == "Baby Dragon":
                if tr["village"] == "home":
                    tr["name"] = "Baby Dragon Day"
                else:
                    tr["name"] = "Baby Dragon Night"
            trpd[tr["name"]] = int(tr["level"])
        for t in troops:
            try:
                tuplist.append((camelCase(t),trpd[t]))
            except:
                pass
        if "spells" in p.keys():
            trp = p["spells"]
            trpd = {}
            for tr in trp:
                trpd[tr["name"]] = int(tr["level"])
            for t in spells:
                try:
                    tuplist.append((camelCase(t),trpd[t]))
                except:
                    pass
        if "heroes" in p.keys():
            trp = p["heroes"]
            trpd = {}
            for tr in trp:
                trpd[tr["name"]] = int(tr["level"])
            for t in heroes:
                try:
                    tuplist.append((camelCase(t),trpd[t]))
                except:
                    pass
        ach = p["achievements"]
        achd = {}
        for ac in ach:
            achd[ac["name"]] = int(ac["value"])
        for a in achievements:
            try:
                tuplist.append((camelCase(a[0]),achd[a[0]]))
            except:
                pass
        extras[tag] = tuplist
    except Exception as e:
        print(e)

threads = []
for i in range(len(tags)):
    tag = tags[i]
    t = threading.Thread(target=addExtra, args=(tag,i))
    threads.append(t)

start_time = time.time()
for i in range(len(threads)):
    if i%200 == 0:
        print("%s started." % i)
        ts = threading.enumerate()
        ts = len(list(ts))
        print("%s threads before sleep." % ts)
        time.sleep(sleep)
        ts = threading.enumerate()
        ts = len(list(ts))
        print("%s threads after sleep.\n" % ts)
        now = time.time()
        print("%f" % (now-start_time))
    threads[i].start()

time.sleep(10)
print("\n\n")
ts = threading.enumerate()
ts = len(list(ts))
print("%s threads." % ts)
print("Finished.")

queries = []
tuples = []
for tag in tags:
    try:
        info = extras[tag]
        if info == None:
            query = "INSERT INTO `%s` (`tag`) VALUES ('%s')" % (new_table,tag)
            queries.append(query)
            tuples.append(None)
        else:
            tuplist = []
            start = "INSERT INTO `%s` (" % new_table
            middle = ") VALUES ("
            for i in range(len(info)):
                info_tuple = info[i]
                start += "`%s`," % info_tuple[0]
                middle += "%s,"
                tuplist.append(info_tuple[1])
            start = start[:-1]
            middle = middle[:-1]
            query = start+middle+")"
            queries.append(query)
            tup = tuple(tuplist)
            tuples.append(tup)
    except Exception as e:
        print("%s: %s" % (e,tag))
print("Generated queries.\n")   

for i in range(len(queries)):
    if i%10000 == 0:
        print("Done %s." % i)
    query = queries[i]
    tup = tuples[i]
    if tup == None:
        cur.execute(query)
    else:
        cur.execute(query,tup)
print("Fully Done.")
