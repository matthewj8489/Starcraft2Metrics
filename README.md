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
		Analyzes a replay and gives access to metrics from the replay at given points.
	- Sc2MultiMetricAnalyzer
		Takes multiple Sc2MetricAnalyzers and uses the metrics generated to develop trends.
	- Sc2ReplayParser
		Parses SC2 replays in order to extract metric data from them. The replays can be filtered.
	- Sc2MetricVisualizer
		Generates graphs of metric trends.

- Outputs
	- Raw replay metric data from each replay
	- Multi-replay metric trend data
	- Graphs of the metric trends
