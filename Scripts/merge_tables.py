import argparse
import MySQLdb

# used if no arguments passed in command line
database = "<database name>"
table_main = "<table name>"
table_extra = "<table name>"
table_new = "<table name>"
common_field = "<field name>"

# create arg parser
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--database")
parser.add_argument("-m", "--main")
parser.add_argument("-e", "--extra")
parser.add_argument("-f", "--field")
parser.add_argument("-n", "--new")
args = parser.parse_args()

# check command line arguments
if args.database:
    database = args.database
if args.main:
    table_main = args.main
if args.extra:
    table_extra = args.extra
if args.new:
    table_new = args.new
if args.field:
    common_field = args.field

# create database connection
db = MySQLdb.connect(host="localhost", user="root", passwd="", db=database, charset="utf8mb4")
db.autocommit(True)
cur = db.cursor()

# get fields (column names) from both tables
main_fields, extra_fields = [], []
query = f"DESCRIBE `{table_main}`"
cur.execute(query)
for row in cur.fetchall():
    main_fields.append((row[0], row[1]))
query = f"DESCRIBE `{table_extra}`"
cur.execute(query)
for row in cur.fetchall():
    extra_fields.append((row[0], row[1]))
print("Fetched column names from both tables.")

# create/replace new table (cfi == common field indexes)
query = f"DROP TABLE IF EXISTS `{table_new}`"
cur.execute(query)
start = f"CREATE TABLE `{table_new}` ("
end = ") CHARACTER SET utf8mb4"
cfi_main = int([main_fields.index(t) for t in main_fields if t[0] == common_field][0])
cfi_extra = int([extra_fields.index(t) for t in extra_fields if t[0] == common_field][0])
del extra_fields[cfi_extra]
fields = main_fields + extra_fields
for f in fields:
    start += f"{f[0]} {f[1]},"
start = start[:-1]
query = start + end
cur.execute(query)
print("Created new table.")

# get all info from both tables
all_info = {}
cf_values = []  # common field values
query = f"SELECT * FROM `{table_main}`"
cur.execute(query)
for row in cur.fetchall():
    all_info[row[cfi_main]] = [row[i] for i in range(len(row))]
    cf_values.append(row[cfi_main])
print("Fetched all data from main table.")
query = f"SELECT * FROM `{table_extra}`"
cur.execute(query)
for row in cur.fetchall():
    all_info[row[cfi_extra]] += [row[i] for i in range(len(row)) if i != cfi_extra]
print("Fetched all data from extra table.")

# generate queries
queries, tuples = [], []
for cfv in cf_values:
    query = f"INSERT INTO `{table_new}` VALUES ("
    for i in range(len(fields)):
        query += "%s,"
    query = query[:-1]
    query += ')'
    info = all_info[cfv]
    tup = tuple(info)
    queries.append(query)
    tuples.append(tup)
print("Generated all queries and tuples.")

# execute queries
for i, (query, tup) in enumerate(zip(queries, tuples)):
    if i % 10000 == 0:
        print(i)
    cur.execute(query, tup)
print(len(queries))
print("Inserted all rows into new table.")
print("Fully done.")
