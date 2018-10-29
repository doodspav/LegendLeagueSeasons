# LegendLeagueSeasons

### Information
All data from 2018-03 onwards is downloaded within 24h (and almost always within an hour) of the season ending, regardless of upload time (usually I download it and then get distracted and forget to format and upload it here). If there was a delay of more than a couple hours after season reset, it will say how long the delay was and the reason for it in the commit description. For seasons before this it doesn't matter since only the legends data has been downloaded, not all the data, and the legends data is saved by supercell at the end of every season.
##### MySQL
Each season has its own file. They contain the following information on every player that finished the season in legends league (i.e. had a legends badge and trophies higher than or equal to 4901):

- rank (int)
- trophies (int)
- tag (str)
- name (str)
- expLevel (int)
- attackWins (int)
- defenseWins (int)
- clanTag (str)
- clanName (str)
- clanBadgeURL (str)

clanBadgeURL is not the full url. The url is in the format "https://api-assets.clashofclans.com/badges/size/clanBadgeURL.png", where clanBadgeURL is the clanBadgeURL provided in the data, and size (not provided) is 70,200, or 512.

The following additional info is provided for season 2018-03:

- townHallLevel (int)
- barbarianKingLevel (int)
- archerQueenLevel (int)
- grandWardenLevel (int)

Seasons 2018-04 and later have all the info provided provided by the official api. Bear in mind that updates can mean that more information is provided.
##### CSV
Seasons 2018-03 and later have seperate csv files from th7-11 (th7 is only included if any got to legends that season), and all seasons have a file with all the information.

The files contain whatever information is available in the MySQL files.

### Gzip
Files larger than 24MB are compressed using gzip. For example `yyyy-mm.sql` would become `yyyy-mm.sql.gz`.

If the compressed file is more than 24MB it's split up into files of max size 24MB. For example `yyyy-mm.sql` would become `yyyy-mm.gza` and `yyyy-mm.gzb`.

In the scripts directory there are scripts to decompress all files and return them to their normal state.
