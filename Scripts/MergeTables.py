import MySQLdb

database = "<put db name here>"
table_main = "<put table name here>"
table_extra = "<put table name here>"
table_new = "<put table name here>"
common_field = "<put shared column name here>"

db = MySQLdb.connect(host="localhost", user="root", passwd="", db=database, charset="utf8mb4")
db.autocommit(True)
cur = db.cursor()

main_fields = []
cur.execute("DESCRIBE `%s`" % table_main)
for row in cur.fetchall():
	main_fields.append((row[0],row[1]))
extra_fields = []
cur.execute("DESCRIBE `%s`" % table_extra)
for row in cur.fetchall():
	extra_fields.append((row[0],row[1]))
print("Fetched column names of both tables.")

try:
	cur.execute("DROP TABLE `%s`" % table_new)
except:
	pass

start = "CREATE TABLE `%s` (" % table_new
end = ") CHARACTER SET utf8mb4"
#common field indexes
cfi_main = int([main_fields.index(t) for t in main_fields if t[0] == common_field][0])
cfi_extra = int([extra_fields.index(t) for t in extra_fields if t[0] == common_field][0])
del extra_fields[cfi_extra]
fields = main_fields+extra_fields
for f in fields:
	start += "%s %s," % (f[0],f[1])
start = start[:-1]
query = start+end
cur.execute(query)
print("Created new table.")

all_info = {}
cf_values = [] #common field values

cur.execute("SELECT * FROM `%s`" % table_main)
for row in cur.fetchall():
	all_info[row[cfi_main]] = [row[i] for i in range(len(row))]
	cf_values.append(row[cfi_main])
print("Fetched all data from main table.")

cur.execute("SELECT * FROM `%s`" % table_extra)
for row in cur.fetchall():
	all_info[row[cfi_extra]] += [row[i] for i in range(len(row)) if i != cfi_extra]
print("Fetched all data from extra table.")

queries = []
tuples = []

for cfv in cf_values:
	query = "INSERT INTO `%s` VALUES (" % table_new
	for i in range(len(fields)):
		query += "%s,"
	query = query[:-1]
	query += ")"
	info = all_info[cfv]
	tup = tuple(info)
	queries.append(query)
	tuples.append(tup)
print("Generated all queries and tuples.")

for i in range(len(queries)):
	if i%5000 == 0:
		print(i)
	query, tup = queries[i], tuples[i]
	cur.execute(query, tup)
print("Inserted all rows to new table.")
print("Fully done.")
