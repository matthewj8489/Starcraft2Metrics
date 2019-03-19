# Starcraft2Metrics

Functions:
1) Build Order Deviation (BOD)
  Determines the average deviation of the time when a unit and building was created by a player in a replay with the time when those units and buildings were made by a benchmark replay. This function will allow a user to see how much deviation occurred between their executed build in any given replay and the benchmark of that same replay.

  
To Do:
- Create a multi-replay graph of average workers active vs time and a specific game's workers active vs time. 
	- Another possibility is to creat a new metric: Worker Creation Rate Pre X Workers. This metric could compare the rate at which workers were created.
	- The Time To X Workers metric might be good enough for comparing, though Worker Creation Rate would account for # bases and when chrono boosts are used.
	
Notes: **_ToDo_**
- Class structure
	- **_Sc2MetricAnalyzer_**
		- Analyzes a replay and gives access to metrics from the replay at given points.
		- Metrics:
			- ttm : Time to (theoretical) Max.
			- ttw66 : Time to a worker count of 66
			- ttw75 : Time to a worker count of 75
			- ttb3 : Time to a base count of 3
			- ttb4 : Time to a base count of 4
			- sq : Average Spending Quotient
			- sqmax : Average Spending Quotient before reaching actual max supply.
			- apm : Average actions per minute
			- **_sc : Time spent supply capped_**
			- aur : Average unspent resources (minerals + vespene)
			- aurmax : Average unspent resources before reaching actual max supply.
			- rcr : Average resource collection rate.
			- rcrmax : Average resource collection rate before reaching actual max supply.
	- **_Sc2MultiMetricAnalyzer_**
		- **_Takes multiple Sc2MetricAnalyzers and uses the metrics generated to develop trends._**
	- **_Sc2ReplayParser_**
		- Parses SC2 replays in order to extract metric data from them. The replays can be filtered.
		- Options:
			- Recursion into a folder **_(to a specified depth)_**
			- **_Automatically monitors a folder for replays, parses new replays, adds their data to the output files_**
			- Overwrite. If set to true, the outputs will be overwritten. If false, any matching replays in the output files will not be parsed again, but their data will still be used in the trends.
			- filters:
				- game-type : 1v1, 2v2, 3v3, or 4v4
				- ladder-only : filters out all non-ladder replays
			- outputs:
				- raw .csv file with metric data from each replay along with replay info:
					- replay name
					- date
					- result
					- map
					- race matchup
					- game length
					- game type
					- is ladder?
				- **_metric trend data:_**
					- **_best_**
					- **_average last 30 games_**
				- **_data visualization graphs of each metric trend_**
	- **_Sc2MetricVisualizer_**
		- **_Generates graphs of metric trends._**

- Outputs
	- Raw replay metric data from each replay
	- **_Multi-replay metric trend data_**
	- **_Graphs of the metric trends_**
