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

<p align="center">
  <a href='https://play.google.com/store/apps/details?id=es.nobone.manchesterwebapp&pcampaignid=pcampaignidMKT-Other-global-all-co-prtnr-py-PartBadge-Mar2515-1'>
    <img alt='Get it on Google Play' width="200" src='https://play.google.com/intl/es-419/badges/static/images/badges/en_badge_web_generic.png'/>
  </a>
  <br/>
  <a href='https://apps.apple.com/es/app/odourcollect/id1457119732'>
    <img alt='Download on the App Store' width="175" src='https://developer.apple.com/app-store/marketing/guidelines/images/badge-example-preferred_2x.png'/>
  </a>
</p>

## Installing the module and the CLI
You can get pyodourcollect from PyPi:
```
pip install pyodourcollect
```

## CLI Vs Module
The command line interface (CLI) tool provided simplifies downloading data from OdourCollect in CSV or XLSX formats
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
| hedonic_tone_n 	| Hedonic tone of odour observation (numeric representation). Hedonic tone is the subjective measurement of how annoyant an odour is, from -4 (`Extremely unpleasant`) to +4 (`Extremely pleasant`). Zero is used to report nor annoyance nor pleasure. This scale is based on the `VDI3882-1` and `VDI3882-2` standards for odour impact assessement.       	|
| hedonic_tone_t 	| Text description version of the former metric.     	|
| intensity_n    	| Intensity of odour observation (numeric representation). Intensity is the measurement of how intense and noticeable an odour is, from 1 (`Very weak`) to 6 (`Extremely strong`). Zero (`Not perceptible`) is also used, but only to report absence of odour in observations. This scale is based on the `VDI 3940:2006` standard for odour impact assessement.    	|
| intensity_t    	| Text description version of the former metric.     	|
| duration       	| Metric informing for how much time an odour has been perceived by reporter. Categorical text data with following self-explanatory options: `(No odour)`,`Punctual`,`Continuous in the last hour` and `Continuous throughout the day`       	|
| latitude       	| GPS coordinates of observation. Latitude.      	|
| longitude      	| GPS coordinates of observation. Longitude.     	|
| distance       	| Distance in Kms (with an accuracy of 0.01 Kms.) between the point of observation and a configurable Point of Interest (POI). This extra data is calculated by PyOdourCollect when the data analyst provides a set of coordinates for a given suspicious activity that motivates his/her analysis. In case that no POI coordinates are provided, this field is missing.      	|

## What data is NOT provided by PyOdourCollect?
OdourCollect.eu provides some additional data regarding odour observations. However, this data is not available without performing one query to OdourCollect API per each observation. That would become much less practical and could put OdourCollect.eu server in jeopardy, so it will not be implemented.
The OdourCollect data that is not going to be provided by PyOdourCollect is:
- Written comments made by the citizen regarding the odour itself or hypothesis about its possible origin at the time of observation. 
- Full address that was inferred at the time of observation (it can be inferred from GPS coordinates anyway).

## Using the CLI
This module includes a command line interface tool that is installed as `odourcollect` (GNU/Linux, MacOS) or `odourcollect.exe` (Windows).
### Stratightforward way: just run the CLI
You can simply run the CLI with no parameters. It will automatically download all data from OdourCollect into a `odourcollect.csv`.
Now you are ready to start analysing the data with you tool of choice.
However, if you prefer to prefilter data or enrich it with some additional fields not provided by OdourCollect, keep reading.
### CLI Arguments
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

`--output`: Dumps the results obtained from OdourCollect directly to the specified file.
The format is autodetected based on extension. `.csv` and `.xlsx` files are allowed. 
Default value is `odourcollect.csv`, which will write a csv file in the working folder.
Please note that we are very conservative here: 
Absolute and relative paths are allowed, but ensure that the destination folder exists (by default, current working folder) and the file does not exist already.
Otherwise, CLI tool will complain and will stop with exit code 2.

`--odourlist`: Dumps the full list of odour categories and types to use with `--category` and `--type`. 
See following section for more details. 

### Full list of odour category and details 
If you run the CLI tool with the parameter `--odourlist`, it will provide the following list:
```
Odour categories (to use in --category parameter:
  Code  Category
------  ----------------------------------------------------------------------------
     1  Waste related odours
     2  Waste water related odours
     3  Agriculture and livestock related odours
     4  Food Industries related odours
     5  Industry related odours
     6  Urban odours
     7  Nice odours
     8  Other odours not fitting elsewhere
     9  No odour observations (for testing, for reporting the end of an odour, etc.)

Odour types (to use in --type parameter:
  Code  Category                 Odour Type
------  -----------------------  -----------------------------------
     1  Waste                    Fresh waste
     2  Waste                    Decomposed waste
     3  Waste                    Leachate
     4  Waste                    Biogas
     5  Waste                    Biofilter
     6  Waste                    Ammonia
     7  Waste                    Amines
     8  Waste                    Other
     9  Waste                    I don't know
    10  Waste Water              Waste water
    11  Waste Water              Rotten eggs
    12  Waste Water              Sludge
    13  Waste Water              Chlorine
    14  Waste Water              Other
    15  Waste Water              I don't know
    16  Agriculture / Livestock  Dead animal
    17  Agriculture / Livestock  Cooked meat
    18  Agriculture / Livestock  Organic fertilizers (manure/slurry)
    19  Agriculture / Livestock  Animal feed
    20  Agriculture / Livestock  Cabbage soup
    21  Agriculture / Livestock  Rotten eggs
    22  Agriculture / Livestock  Ammonia
    23  Agriculture / Livestock  Amines
    24  Agriculture / Livestock  Other
    25  Agriculture / Livestock  I don't know
    26  Food Industries          Fat / Oil
    27  Food Industries          Coffee
    28  Food Industries          Cocoa
    29  Food Industries          Milk / Dairy
    30  Food Industries          Animal food
    31  Food Industries          Ammonia
    32  Food Industries          Malt / Hop
    33  Food Industries          Fish
    34  Food Industries          Bakeries
    35  Food Industries          Raw meat
    36  Food Industries          Ammines
    37  Food Industries          Cabbage soup
    38  Food Industries          Rotten eggs
    39  Food Industries          Bread / Cookies
    40  Food Industries          Alcohol
    41  Food Industries          Aroma / Flavour
    42  Food Industries          Other
    43  Food Industries          I don't know
    44  Industrial               Cabbage soup
    45  Industrial               Oil / Petrochemical
    46  Industrial               Gas
    47  Industrial               Asphalt / Rubber
    48  Industrial               Chemical
    49  Industrial               Ammonia
    50  Industrial               Leather
    51  Industrial               Metal
    52  Industrial               Plastic
    53  Industrial               Sulphur
    54  Industrial               Alcohol
    55  Industrial               Ketone / Ester / Acetate / Ether
    56  Industrial               Amines
    57  Industrial               Glue / Adhesive
    58  Urban                    Urine
    59  Urban                    Traffic
    60  Urban                    Sewage
    61  Urban                    Waste bin
    62  Urban                    Waste truck
    63  Urban                    Sweat
    64  Urban                    <not used>
    65  Urban                    Fresh grass
    66  Urban                    Humidity / Wet soil
    67  Urban                    Flowers
    68  Urban                    Food
    69  Urban                    Chimney (burnt wood)
    70  Urban                    Paint
    71  Urban                    Fuel
    72  Urban                    Other
    73  Urban                    I don't know
    74  Nice                     Flowers
    75  Nice                     Food
    76  Nice                     Bread / Cookies
    77  Nice                     Fruit
    78  Nice                     Fresh grass
    79  Nice                     Forest / Trees / Nature
    80  Nice                     Mint / Rosemary / Lavander
    81  Nice                     Sea
    82  Nice                     Perfume
    83  Nice                     Chimney (burnt wood)
    84  Nice                     Wood
    85  Nice                     New book
    86  Nice                     Other
    87  Nice                     I don't know
    88  No Odour                 No Odour
    89  Other                    NA
```
Please note that each odour type code actually represents a combination of category + type.
Some odour types appear more than once because they are associated to more than one category.
This can be confusing sometimes, but it enables the analyst to obtain more nuances based on the category, 
and have a better understanding of what the perception of the citizen was. 
That is why we suggest you two ways in which you can filter the odour observation by type, the easiest 
and the more detailed.

### How to filter odour observations by type (the easiest way)
This filter strategy is usually more than enough to perform interesting and relevant analysis.
It has the advantadge of not having to deal with numeric codes while being specific enough.
If you are getting started with OdourCollect data analysis, we suggest you to stick to the following:
1. Just donwload the data with no category/type filters
2. open it in your analysis tool (i.e. Microsoft Excel)
3. Ignore the column `category` and proceed directly to the column `type`, 
selecting the description of the odour you are interested in (i.e.: `ammonia`).

Technically, this traduces to the following odour codes:
   
| Category                	| Type    	| Type code 	|
|-------------------------	|---------	|:---------:	|
| Waste                   	| Ammonia 	|     6     	|
| Agriculture / Livestock 	| Ammonia 	|     22    	|
| Food industries         	| Ammonia 	|     31    	|
| Industrial              	| Ammonia 	|     49    	|

But you will treat them as the same. This way, you will get all the odour observations that have been reported as ammonia, no matter the nuances.

### How to filter odour observations by type (the more detailed way)
Let's imagine that you are still interested in ammonia, but you want to focus on the odour observations in which the citizen 
is suspicious about some agricultural/livestock activity nearby. So you are interested in knowing what category did the user select when he/she reported the odour, 
because this is a way of getting such nuances.

After typing in your command line `odurcollect.exe --odourlist` and checking the type codes table, 
you realise that the odour type you are interested in is `31`. So you type the following command:

`odourcollect.exe --type 31`

This command will save `odourcollect.csv` in your current directory.

The file will only contain observations of category `Agriculture / Livestock` and type `Ammonia`.

### Recommended tools to analyse the data downloaded with the CLI
You suggest you to use the following tools to process the data you download with PyOdourCollect's CLI.
They are in no particular order, and it's mostly a matter of choice.
Also, there are many more not listed here that can perfectly suit your needs (feel free to let us know, so we can add them here):
1. [Orange data mining](https://orangedatamining.com/). A free, python based, intutitive, graphic application designed to ease the process of data ingestion, transformation, analysis and visualisation. 
You can use the mouse and a few clicks without knowing anything about code. It can also plot maps based on gps coordinates. We recommend it!
2. Microsoft PowerBI. Microsoft's standard technology for data connectors and data analysis.
It features interactive dashboards with interactive graphics that can be extremely useful to illustrate and demonstrate what's happening in a community affected by odour pollution, 
including geographic maps, but it requieres more practice in comparison to other tools like Orange or Excel.  
3. Microsoft Excel. The good old option for hobbyists and amateur Citizen Scientists. Its features are more than enough to filter, order, obtain statistics, detect some basic patterns and plot explanatory graphics based on the data.

Want to see your favourite tool here? Let us know.

## Using PyOdourCollect module
Using PyOdourCollect is very easy. You only have to do four steps:
1. Load module and helpers.
2. Prepare a request.
3. (Optional) prepare GPS coordinates of a suspicious Point Of Interest, if you have any.
4. Send the request to OdourCollect, getting a DataFrame in exchange.

### 1. Load module and helpers
The examples here will assume that you loaded the pyodourcollect module and helpers this way:
```
import pyodourcollect.ochelpers as ochelpers
import pyodourcollect.occore as occore
import pyodourcollect.ocmodels as ocmodels
```

### 2. Prepare a request

Compared to PyOdourCollect's CLI, using PyOdourCollect module directly just requires a bit more knowledge about how OdourCollect.eu API works, 
and what parameters expect to receive. Things are self-explanatory and have similar counterparts in Command Line Interface tool.

We provide a Pydantic model through pyodourcollect.ocmodels, making the process easier:

```
requestparams = ocmodels.OCRequest(
                date_init=date_init,
                date_end=date_end,
                minAnnoy=min_annoy,
                maxAnnoy=max_annoy,
                minIntensity=min_intensity,
                maxIntensity=max_intensity,
                type=odour_type,
                subtype=odour_subtype)
```
Explanation of the aforementioned parameters (all of them are optional):

`date_init`: The equivalent of `--startdate` in CLI. Expects a date object.

`date_end`: The equivalent of `--enddate` in CLI. Expects a date object.

`minAnnoy`: Minimum degree of pleasantness/annoyance, from -4 (Extremely annoying) to 4 (Extremely pleasant).

`maxAnnoy`: Maximum degree of pleasantness/annoyance, from -4 (Extremely annoying) to 4 (Extremely pleasant).

> When using CLI, `minAnnoy` and `maxAnnoy` are not directly specified. Instead, you use the `--hedonic` parameter as a shorthand for pleasant (from 1 to 4), unpleasant (from -4 to -1) or neutral (just 0) odours. This was decided to avoid the hassle of handling negative numbers in command line arguments, which can be problematic.

> Please note that `minAnnoy` can't be greater than maxAnnoy, and that the ranges always have to be expressed starting from the smaller number: for a range from -4 to 0, -4 is minAnnoy and 0 is maxAnnoy.

`minIntensity`: Minimum degree of intensity, from 0 (not perceptible) to 6 (extremely strong). 

`maxIntensity`: Maximum degree of intensity, from 0 (not perceptible) to 6 (extremely strong).

> Again, please note that min values can't be greater that max values. Internal request validators will complain otherwise.

`type`: Tier 1 classification of odour observations (known as "Type" in OdourCollect, "Category" in PyOdourCollect).

`subtype`: Tier 2 classification of odour observations (known as "Subtype" in OdourCollect, "Type" in PyOdourCollect).

### 3. (Optional) prepare GPS coords of a POI
If you have the GPS coords of a suspicious Point Of Interest and you want to add them to the data, you can do it this way:

```
suspicious_coords = ocmodels.GPScoords(latitude, longitude)
```
where `latitude` and `longitude` are the gps coords of the facility, industry, farm, plant, etc. that you are investigating. 
The GPScoords helper provides instant validation of valid GPS coordinates.

### 4. Send the request to OdourCollect

```
my_ocdata = occore.get_oc_data(requestparams, suspicious_coords)
```

where `requestparams` and `suspicious_coords` are the OCRequest and GPScoords objects built in previous steps.
In case you don't want to add distances from a given point, you can omit the creation of a GPSCoords object, 
but you have to explicitly pass `None` as second parameter to `occore.get_oc_data`.

After that, `my_ocdata` will contain a Pandas DataFrame object with all the data ready to use.

So, a typical Python script to gather data from OdourCollect specifying all request parameters would be as follows:

```
import pyodourcollect.ochelpers as ochelpers
import pyodourcollect.occore as occore
import pyodourcollect.ocmodels as ocmodels
from datetime import datetime

date_init = datetime.strptime('31-01-2020', '%Y-%m-%d')  # just random example
date_end = datetime.strptime('30-02-2020', '%Y-%m-%d')  # just random example

requestparams = ocmodels.OCRequest(
                date_init=date_init,
                date_end=date_end,
                minAnnoy=-4,
                maxAnnoy=4,
                minIntensity=0,
                maxIntensity=6,
                type=0,
                subtype=0)
suspicious_coords = ocmodels.GPScoords(41.409032, 2.222619)  # Example. A waste water processing plant in Barcelona
my_ocdata = occore.get_oc_data(requestparams, suspicious_coords)
```

**BONUS TRACK**: One liner to get all data from OdourCollect quickly and easily:

```
my_ocdata = occore.get_oc_data(ocmodels.OCRequest(), None)  # Requests with no filter parameters cause OdourCollect to yield all data.
```

 

