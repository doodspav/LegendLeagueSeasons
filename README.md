# LegendLeagueSeasons

Information Contained:
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

The following info is provided for seasons 2018-03 and later:

- townHallLevel (int)
- barbarianKingLevel (int)
- archerQueenLevel (int)
- grandWardenLevel (int)
