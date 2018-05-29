import glob, subprocess

database = "<put db name here>"

files = [f for f in glob.glob("*.sql")]
for f in files:
    try:
        command = "mysql %s < %s" % (database,f)
        stdout = subprocess.check_output(command,shell=True)
    except Exception:
        print("Database (%s) not found." % database)
        break

print("Finished.")
