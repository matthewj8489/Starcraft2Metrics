python sc2autosave.py 							\
	--source ~/My\ Documents/Starcraft\ II/Accounts/.../Multiplayer \
	--dest ~/My\ Documents/Starcraft2Replays/1v1Ladder		\
	--rename "{:date}({:length}) {:matchup} on {:map}: {:teams}"	\
	--player-format "{:name}({:play_race})"				\
	--date-format "YYYY-MM-DD"					\
	--filter-matchup 1v1						\

	
	