import glob, subprocess

database = "<put db name here>"

files = [f for f in glob.glob("*.sql")]
for f in files:
    command = "mysql `%s` < %s" % (database,f)
    stdout = subprocess.check_output(command,shell=True)
    print(stdout)

print("Finished.")
