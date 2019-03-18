# Starcraft2Metrics

Functions:
1) Build Order Deviation (BOD)
  Determines the average deviation of the time when a unit and building was created by a player in a replay with the time when those units and buildings were made by a benchmark replay. This function will allow a user to see how much deviation occurred between their executed build in any given replay and the benchmark of that same replay.

  
To Do:
- Create a multi-replay graph of average workers active vs time and a specific game's workers active vs time. 
	- Another possibility is to creat a new metric: Worker Creation Rate Pre X Workers. This metric could compare the rate at which workers were created.
	- The Time To X Workers metric might be good enough for comparing, though Worker Creation Rate would account for # bases and when chrono boosts are used.
	
Notes:
- Class structure
	- Sc2MetricAnalyzer
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
			- sc : Time spent supply capped
			- aur : Average unspent resources (minerals + vespene)
			- aurmax : Average unspent resources before reaching actual max supply.
			- rcr : Average resource collection rate.
			- rcrmax : Average resource collection rate before reaching actual max supply.
	- Sc2MultiMetricAnalyzer
		- Takes multiple Sc2MetricAnalyzers and uses the metrics generated to develop trends.
	- Sc2ReplayParser
		- Parses SC2 replays in order to extract metric data from them. The replays can be filtered.
	- Sc2MetricVisualizer
		- Generates graphs of metric trends.

- Outputs
	- Raw replay metric data from each replay
	- Multi-replay metric trend data
	- Graphs of the metric trends
