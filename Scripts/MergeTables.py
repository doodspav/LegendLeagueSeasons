import MySQLdb

database = "database"
oldtable_main = "table1"
oldtable_extra = "table2"
new_table = "table3"

db = MySQLdb.connect(host="localhost", user="root", passwd="", db=database, charset="utf8mb4")
db.autocommit(True)
cur = db.cursor()

all_info = {}
tags = []

cur.execute("SELECT * FROM `%s`" % oldtable_main)
for row in cur.fetchall():
    #rank, trophies, tag, name, expLevel, attackWins, defenseWins, clanTag, clanName, clanBadgeURL
    all_info[row[2]] = [row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]]
    tags.append(row[2])

cur.execute("SELECT * FROM `%s`" % oldtable_extra)
for row in cur.fetchall():
    #tag, townHallLevel, bkLevel, aqLevel, gwLevel
    all_info[row[0]] += [row[1],row[2],row[3],row[4]]

queries = []
tuples = []

for tag in tags:
    query = "INSERT INTO `%s` (`rank`,`trophies`,`tag`,`name`,`expLevel`,`attackWins`,`defenseWins`,`clanTag`,`clanName`,`clanBadgeURL`,`townHallLevel`,`barbarianKingLevel`,`archerQueenLevel`,`grandWardenLevel`) " % new_table
    query += "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    info = all_info[tag]
    tup = tuple(info)
    queries.append(query)
    tuples.append(tup)

for i in range(len(queries)):
    if i%5000 == 0:
        print(i)
    query, tup = queries[i], tuples[i]
    cur.execute(query, tup)
print("Fully done.")
