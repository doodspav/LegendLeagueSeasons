#!/usr/bin/env bash

# get command line arguments
if [ $# != 4 ]; then
	printf "You provided $# command line arguments; you need 4:"
	printf "database, folder, season, keyfile"
	exit 0
fi
database=$1
new_dir=$2
season=$3
readarray keys < "$4"
printf "\nBASH :: Got command line arguments\n"
sleep 2

# setup server
sudo apt-get update && sudo apt-get -y upgrade
sudo apt-get -y install python3-pip python3-dev libmysqlclient-dev
sudo pip3 install mysqlclient
printf "\nBASH :: Setup server\n"
sleep 2

# make and clear directories
mkdir "$new_dir"
cd "$new_dir" || exit 1
rm * -f
mkdir sql
cd sql || exit 1
rm * -f
cd ..
mkdir csv
cd csv || exit 1
rm * -f
cd ..
printf "\nBASH :: Made and cleared directories\n"
sleep 2

# get files
wget https://raw.githubusercontent.com/doodspav/LegendLeagueSeasons/master/Scripts/legends_data.py
wget https://raw.githubusercontent.com/doodspav/LegendLeagueSeasons/master/Scripts/extra_data.py
wget https://raw.githubusercontent.com/doodspav/LegendLeagueSeasons/master/Scripts/merge_tables.py
wget https://raw.githubusercontent.com/doodspav/LegendLeagueSeasons/master/Scripts/release_checker.py
printf "\nBASH :: Wgot files\n"
sleep 2

# run releaseChecker.py
python3 release_checker.py -s "$season" -r 30 -e 5 -k "${keys[0]}"
exit_code=$?
while [ $exit_code != 5 ]; do
	printf "Incorrect exit code. Was $?, should have been 5."
	sleep 5
	printf "Rerunning..."
	python3 releaseChecker.py -s "$season" -r 30 -e 5 -k "${keys[0]}"
	exit_code=$?
done
printf "\nBASH :: Ran release_checker.py\n"
sleep 2

# collect data
python3 legends_data.py -d "$database" -t LD -s "$season" -k "${keys[0]}"
sleep 2
command_string="python3 extra_data.py -d $database -t LD -n ED -s 2"
for key in "${keys[@]}"; do
	command_string="$command_string -k $key"
done
$command_string
sleep 2
python3 merge_tables.py -d "$database" -m LD -e ED -n "$season" -f tag
printf "\nBASH :: Collected data\n"
sleep 2

# create sql files
cd sql || exit 1
mysqldump "$database" "$season" > "$season.sql"
gzip -c "$season.sql" | split -b 24000000 - "$season.sql.gz"
cd ..
printf "\nBASH :: Created SQL files\n"
sleep 2

# create csv files
cd csv || exit 1
base_query="'SELECT * FROM \`$season\`"
th0="$base_query'"
mysql "$database" -e "$th0" -B | sed "s/'/\'/;s/\t/\",\"/g;s/^/\"/;s/$/\"/;s/\n//g" > "$season.csv"
for n in {7..12}; do
	thn="$base_query WHERE townHallLevel=$n'"
	mysql "$database" -e "$thn" -B | sed "s/'/\'/;s/\t/\",\"/g;s/^/\"/;s/$/\"/;s/\n//g" > "$season-th$thn.csv"
done
gzip -c "$season.csv" | split -b 24000000 - "$season.csv.gz"
gzip -c "$season-th12.csv" | split -b 24000000 - "$season.csv-th12.gz"
printf "\nBASH :: Created CSV files\n"
sleep 2

# finish
printf "th7 csv file may be empty."
