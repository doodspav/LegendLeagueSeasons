import glob, os

full_files = [f for f in glob.glob("*.gz")]
split_files = [f for f in glob.glob("*.gz??")]
unique_split_files = []

for sf in split_files:
    name = sf[:-2]
    if name not in unique_split_files:
        unique_split_files.append(name)

for ff in full_files:
    cmd = "gunzip %s" % ff
    os.system(cmd)

for usf in unique_split_files:
    new_name = usf[:-3]
    cmd = "cat %s* | zcat > %s" % (usf,new_name)
    os.system(cmd)

for sf in split_files:
    os.remove(sf)

print("Done.")
