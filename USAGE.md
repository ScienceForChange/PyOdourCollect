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

If you find out that there is not odur observation data for the zone you wanted to analyse, 
you can always lead a local movement in your community and start recruiting neighbours, 
so they download the OdourCollect APP on their phones and start mapping odour observations!

<div style="text-align:center">
  <a href='https://play.google.com/store/apps/details?id=es.nobone.manchesterwebapp&pcampaignid=pcampaignidMKT-Other-global-all-co-prtnr-py-PartBadge-Mar2515-1'>
    <img alt='Get it on Google Play' width="200" src='https://play.google.com/intl/es-419/badges/static/images/badges/en_badge_web_generic.png'/>
  </a>
  <br/>
  <a href='https://apps.apple.com/es/app/odourcollect/id1457119732'>
    <img alt='Download on the App Store' width="175" src='https://developer.apple.com/app-store/marketing/guidelines/images/badge-example-preferred_2x.png'/>
  </a>
</div>

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
(soon)

# Using the CLI
This module includes a command line interface tool that is installed as `odourcollect` (GNU/Linux, MacOS) or `odourcollect.exe` (Windows).

This is the full help and usage output of the tool:
```
usage: OdourCollect [-h] [--startdate STARTDATE] [--enddate ENDDATE] [--category CATEGORY] [--odourtype ODOURTYPE]
                    [--hedonic [{pleasant,unpleasant,neutral,all}]] [--minintensity MININTENSITY] [--maxintensity MAXINTENSITY] [--gps lat long]
                    [--output path to output file] [--odourlist]

pyOdourCollect: A tool that obtains odour observations made by citizens at odourcollect.eu Citizen Obsevatory.

optional arguments:
  -h, --help            show this help message and exit

Observation filter options:
  --startdate STARTDATE, -s STARTDATE
                        Earliest date (yyyy-mm-dd).
  --enddate ENDDATE, -e ENDDATE
                        Latest date (yyyy-mm-dd).
  --category CATEGORY, -c CATEGORY
                        Category of odours (known as 'type' in OdourCollect) From 1 to 9. 0 means all.
  --odourtype ODOURTYPE, -t ODOURTYPE
                        Type of odour (known as 'subtype' in OdourCollect). From 1 to 89. 0 means all.
  --hedonic [{pleasant,unpleasant,neutral,all}]
                        Hedonic tones. "unpleasant" (from -1 to -4), "pleasant" (from +1 to +4), "neutral" (tone zero only) or "all" (get everything,
                        default
  --minintensity MININTENSITY
                        Minimum intensity of odour, from 0 to 6.
  --maxintensity MAXINTENSITY
                        Maximum intensity of odour, from 0 to 6.

Analysis options:
  --gps lat long        If specified, observations will include the distance in Km. from the specified GPS coordinates. Useful to analize data against a
                        suspicious point of odour emission in a specific area of interest. Takes two arguments in the form of decimal numbers for lat/long
                        gps coordenates i.e.: --gps 41.409032 2.222619

Output options:
  --output path to output file
                        Dump the results in xlsx/csv format to the specified file If not specified, defaults to "odourcollect.csv". File format is
                        autodetected based on extension.

List of odour categories and types:
  --odourlist           Prints the full list of odour categories and types used in OdourCollect.eu web and OdourCollect App

Run this program with --odourlist parameter for a full list of odour categories and types.
```
More detail on CLI params:

`--startdate` and `--enddate`: download only data comprised between start and end dates. 
When start date is not specified, it uses 2019-01-01 (OdourCollect launched on 2019). 
When end date is not specified, it uses current date, so it virtually means no end date.
Format of dates must be in `yyyy-mm-dd` format.

`--category` and `--type`: download only odour observations of certain odours based on a two tier classification system provided by OdourCollect.
Please note that "category" and "type" in PyOdourCollect are known as "type" and "subtype" in OdourCollect respectively.
While the first tier of classification provides only 8 options and provides a general idea for preliminary analysis, the second tier provides almost 90 classificators and is the most precise information that citizens can provide in the odour observation.
`--category` accepts numbers from 0 to 9. `--type` accepts numbers from 0 to 89. In both cases, 0 means "all" and is the default if not specified, so you can safely ignore these parameters if you prefer to download full data.
The full list of odour categories and odour types can be explored below.

`--hedonic`: The hedonic tone provides an observation filter based on the subjective pleasantness perception that the Citizen had when he/she reported. 
Internally, OdourCollect allows up to 9 degrees of pleasantness from -4 (most annoyant) to +4 (most pleasant), being 0 neutral. 
In order to simplify CLI usage and avoid managing ranges of negative numbers (which could be counterintuitive), 
we decided to provide just shorthand keywords: `pleasant` (from +1 to +4), `unpleasant` (from -1 to -4), 
`neutral` (observations with tone zero only), and `all` (which is the default, so you can safely omit the parameter if you plan to download full data).

`--minintensity` and `--maxintensity`: Filter observations by a minimum/maximum level of intensity reported by citizen at the time of observation. 
Values range from 0 (no odour) to 6 (extremely strong). Defaults are 0 for minimum and 6 for maximum, so you can safely omit these parameters if you plan to download full data.

`--gps`: This parameter expects two numbers in the form GPS coordinates for a given point (for example `--gps 41.409032 2.222619`). 
When specified, the downloaded data will include an extra column called `distance` at the end. 
This column will provide the distance (with an accuracy of 0.01 Kms.) between the point where the observation was made and the point specified with `--gps`.
This is extremely useful when you are analyzing a specific area of interest around a suspicious point from which odour emissions allegedly come.
You can then start your analysis removing or filtering out all the observations that are beyond a given distance (say, 10kms) to perform an analysis of a local area
(which is the most useful and logical use case). In future versions we plan to provide an option to filter out the observations that are past a given distance, 
so you have not to filter by yourself at a later stage. For the time being, please manually filter observations that are at 999 Kms from your area of interest :wink:.   


 

