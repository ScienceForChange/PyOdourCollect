# PyOdourCollect usage
This file explains how to use the Python module and the CLI as well as the intended use cases for them.
## Intended uses
Basically, PyOdourCollect is a tool for advanced Citizen Scientists and/or data analysts 
that want to obtain useful information regarding odour pollution episodes in a given area of interest. 
Nothing precludes any user from downloading all the observations to date in OdourCollect platform, 
but the most insightful analysis can only be performed when data is conveniently filtered by criteria like 
odour type and distance from a suspicious, previously identified point of interest.

If you previously want to know if the citizens have provided odour observations in a given area of your interest,
the best way to know is visiting [OdourCollect.eu](https://odourcollect.eu) directly and taking a look at the map. 
OdourCollect shares all the collected data for free, the same way the Citizen Scientists worldwide provide it.

## CLI Vs Module
The command line interface (CLI) tool provided simplifies downloading data from OdourCollect in CSV or XLSX formats.
and is the to-go choice if you plan to analyze the data:
- Manually
- With Microsoft's Excel or PowerBI
- With other data analysis tools that can import CSV or XLSX files. For example, [Orange data mining](https://orangedatamining.com/) (which we strongly recommend!)

On the other hand, the bare Python module is a more suitable choice if you are a more advanced scientist planning to:
- Put OdourCollect's data in a [Pandas DataFrame](https://pandas.pydata.org/docs/user_guide/dsintro.html#dataframe) to analyse and visualise it using your own code for that purpose. 
- Integrate OdourCollect's data into a Python program of yours. 
In that cases, PyOdourCollect will provide you with the data you need in the simpliest way: a [Pandas DataFrame](https://pandas.pydata.org/docs/user_guide/dsintro.html#dataframe).

## Data structure 

Wether you use the CLI to download OdourCollect's data in CSV/XLSX format, or you use the Python module directly to obtain a Pandas DataFrame, the structure of the data is the same:

| field           	| description 	|
|----------------	|------	|
| user              | OdourCollect's user ID of the citizen that registered the observation.      |
| date           	| Observation date in yyyy-mm-dd format.     	|
| time           	| Observation time in HH:mm (24h) format, UTC timezone.     	|
| week_day       	| Observation day of week. This field is extra data calculated by PyOdourCollect to help the analyst in finding patterns. Please bear in mind that this calculation is based on UTC, not local time, so it could be misleading in some edge cases.|
| category       	| First tier of odour classification. In OdourCollect webapp, this is called "type". It provides complementary classification nuances that can be safely ignored for basic analysis. See the full table below for better understanding.  	|
| type           	| Second tier of odour classification. In OdourCollect webapp, this is called "subtype". It provides the richest odour classification criteria. See the full table below for better understanding.     	|
| hedonic_tone_n 	| Hedonic tone of odour observation (numeric representation). Hedonic tone is the subjective measurement of how annoyant an odour is, from -4 (`Extremely unpleasant`) to +4 (`Extremely pleasant`). Zero is used to report nor annoyance nor pleasure. This scale is based on the `VDI 3940:2006` standard for odour impact assessement.       	|
| hedonic_tone_t 	| Text description version of the former metric.     	|
| intensity_n    	| Intensity of odour observation (numeric representation). Intensity is the measurement of how intense and noticeable an odour is, from 1 (`Very weak`) to 6 (`Extremely strong`). Zero (`Not perceptible`) is also used, but only to report absence of odour in observations. This scale is based on the `VDI 3940:2006` standard for odour impact assessement.    	|
| intensity_t    	| Text description version of the former metric.     	|
| duration       	| Metric informing for how much time an odour has been perceived by reporter. Categorical text data with following self-explanatory options: `(No odour)`,`Punctual`,`Continuous in the last hour` and `Continuous throughout the day`       	|
| latitude       	| GPS coordinates of observation. Latitude.      	|
| longitude      	| GPS coordinates of observation. Longitude.     	|
| distance       	| Distance in Kms (with an accuracy of 0.01 Kms.) between the point of observation and a configurable Point of Interest (POI). This extra data is calculated by PyOdourCollect when the data analyst provides a set of coordinates for a given suspicious activity that motivates his/her analysis. In case that no POI coordinates are provided, this field is missing.      	|

# What data is NOT provided by PyOdourCollect?
OdourCollect.eu provides some additional data regarding odour observations. However, this data is not available without performing one query to OdourCollect API per each observation. That would become much less practical and could put OdourCollect.eu server in jeopardy, so it will not be implemented.
The OdourCollect data that is not going to be provided by PyOdourCollect is:
- Written comments made by the citizen regarding the odour itself or hypothesis about its possible origin at the time of observation. 
- Full address that was inferred at the time of observation (it can be inferred from GPS coordinates anyway).

# Installing the module and the CLI


# Using the CLI
I