import json
import os
import pandas as pd
from datetime import date
import haversine as hs
import pathlib
import pyodourcollect.ocmodels as ocmodels

OC_ENDPOINT = 'https://odourcollect.eu/api/odor/list'

TYPE_LIST = {1: 'Waste|Fresh waste',
             2: 'Waste|Decomposed waste',
             3: 'Waste|Leachate',
             4: 'Waste|Biogas',
             5: 'Waste|Biofilter',
             6: 'Waste|Ammonia',
             7: 'Waste|Amines',
             8: 'Waste|Other',
             9: 'Waste|I don\'t know',
             10: 'Waste Water|Waste water',
             11: 'Waste Water|Rotten eggs',
             12: 'Waste Water|Sludge',
             13: 'Waste Water|Chlorine',
             14: 'Waste Water|Other',
             15: 'Waste Water|I don\'t know',
             16: 'Agriculture / Livestock|Dead animal',
             17: 'Agriculture / Livestock|Cooked meat',
             18: 'Agriculture / Livestock|Organic fertilizers (manure/slurry)',
             19: 'Agriculture / Livestock|Animal feed',
             20: 'Agriculture / Livestock|Cabbage soup',
             21: 'Agriculture / Livestock|Rotten eggs',
             22: 'Agriculture / Livestock|Ammonia',
             23: 'Agriculture / Livestock|Amines',
             24: 'Agriculture / Livestock|Other',
             25: 'Agriculture / Livestock|I don\'t know',
             26: 'Food Industries|Fat / Oil',
             27: 'Food Industries|Coffee',
             28: 'Food Industries|Cocoa',
             29: 'Food Industries|Milk / Dairy',
             30: 'Food Industries|Animal food',
             31: 'Food Industries|Ammonia',
             32: 'Food Industries|Malt / Hop',
             33: 'Food Industries|Fish',
             34: 'Food Industries|Bakeries',
             35: 'Food Industries|Raw meat',
             36: 'Food Industries|Ammines',
             37: 'Food Industries|Cabbage soup',
             38: 'Food Industries|Rotten eggs',
             39: 'Food Industries|Bread / Cookies',
             40: 'Food Industries|Alcohol',
             41: 'Food Industries|Aroma / Flavour',
             42: 'Food Industries|Other',
             43: 'Food Industries|I don\'t know',
             44: 'Industrial|Cabbage soup',
             45: 'Industrial|Oil / Petrochemical',
             46: 'Industrial|Gas',
             47: 'Industrial|Asphalt / Rubber',
             48: 'Industrial|Chemical',
             49: 'Industrial|Ammonia',
             50: 'Industrial|Leather',
             51: 'Industrial|Metal',
             52: 'Industrial|Plastic',
             53: 'Industrial|Sulphur',
             54: 'Industrial|Alcohol',
             55: 'Industrial|Ketone / Ester / Acetate / Ether',
             56: 'Industrial|Amines',
             57: 'Industrial|Glue / Adhesive',
             58: 'Urban|Urine',
             59: 'Urban|Traffic',
             60: 'Urban|Sewage',
             61: 'Urban|Waste bin',
             62: 'Urban|Waste truck',
             63: 'Urban|Sweat',
             64: 'Urban|<not used>',  # it seems odour number 64 was accidentaly ommited in original design
             65: 'Urban|Fresh grass',
             66: 'Urban|Humidity / Wet soil',
             67: 'Urban|Flowers',
             68: 'Urban|Food',
             69: 'Urban|Chimney (burnt wood)',
             70: 'Urban|Paint',
             71: 'Urban|Fuel',
             72: 'Urban|Other',
             73: 'Urban|I don\'t know',
             74: 'Nice|Flowers',
             75: 'Nice|Food',
             76: 'Nice|Bread / Cookies',
             77: 'Nice|Fruit',
             78: 'Nice|Fresh grass',
             79: 'Nice|Forest / Trees / Nature',
             80: 'Nice|Mint / Rosemary / Lavander',
             81: 'Nice|Sea',
             82: 'Nice|Perfume',
             83: 'Nice|Chimney (burnt wood)',
             84: 'Nice|Wood',
             85: 'Nice|New book',
             86: 'Nice|Other',
             87: 'Nice|I don\'t know',
             88: 'No Odour|No Odour',
             89: 'Other|NA'}

CATEGORY_LIST = {1: 'Waste related odours',
                 2: 'Waste water related odours',
                 3: 'Agriculture and livestock related odours',
                 4: 'Food Industries related odours',
                 5: 'Industry related odours',
                 6: 'Urban odours',
                 7: 'Nice odours',
                 8: 'Other odours not fitting elsewhere',
                 9: 'No odour observations (for testing, for reporting the end of an odour, etc.)'}

ANNOY_ID_TO_REAL_NUMBER = {1: -4,
                           2: -3,
                           3: -2,
                           4: -1,
                           5: 0,
                           6: 1,
                           7: 2,
                           8: 3,
                           9: 4}

ANNOY_ID_TO_DESCRIPTION = {1: 'Extremely unpleasant',
                           2: 'Very unpleasant',
                           3: 'Unpleasant',
                           4: 'Slightly unpleasant',
                           5: 'Neutral',
                           6: 'Slightly pleasant',
                           7: 'Pleasant',
                           8: 'Very pleasant',
                           9: 'Extremely pleasant'}

INTENSITY_ID_TO_REAL_NUMBER = {1: 0,
                               2: 1,
                               3: 2,
                               4: 3,
                               5: 4,
                               6: 5,
                               7: 6}

INTENSITY_ID_TO_DESCRIPTION = {1: 'Not perceptible',
                               2: 'Very weak',
                               3: 'Weak',
                               4: 'Noticeable',
                               5: 'Strong',
                               6: 'Very strong',
                               7: 'Extremely strong'}

DURATION_LIST = {0: '(No odour)',
                 1: 'Punctual',
                 2: 'Continuous in the last hour',
                 3: 'Continuous throughout the day'}


def build_ocrequest(params):
    # Receives OCRequest
    # constructs payload for POST request
    payload = {}
    for param in params:
        key = param[0]
        if type(param[1]) == date:
            value = param[1].strftime('%Y-%m-%d')
        else:
            value = param[1]
        payload.update({key: value})
    return payload


def day_of_week(whatdate: date) -> str:
    weekdays = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
    dow = whatdate.weekday()
    return weekdays[dow]


def build_df(json_response) -> pd.DataFrame:
    observationslist = []
    try:
        observationslist = json.loads(json_response)['content']
    except KeyError:
        print('Received JSON data does not have a "content" key:')
        print(json_response)
        exit(2)
    if len(observationslist) == 0:
        print('No data for criteria specified')
        exit(1)
    df = pd.DataFrame(observationslist)

    # DATA TRANSFORMS
    # USERS: adds the character "u" as a prefix for the user ID number so they clearly become categoric, not numeric
    df['id_user'] = df['id_user'].apply(str)
    df['id_user'] = df['id_user'].apply(lambda s: 'u' + s)
    df.rename(columns={'id_user': 'user'}, inplace=True)

    # ODOUR TYPES: build a "category" column copying values from "id_odor_type"
    df['category'] = df['id_odor_type']
    # we perform substitutions. Numeric values become text: "category of odour|type of odour"
    df.replace(inplace=True, to_replace={'category': TYPE_LIST})
    # then we split the BBBB part of "AAAA|BBBB" into a new, separate column called "type"
    # We end up having "id_odor_type" as numeric type, "category" as text description of odour,
    # and type as text description of type. The columns go hand in hand, always matching values.
    df[['category', 'type']] = df['category'].str.split('|', n=1, expand=True)
    # we can remove id_odor_type now
    df.drop('id_odor_type', inplace=True, axis=1)

    # DURATION: we replace numeric, non explanatory values by categoric text values on the spot
    df.replace(inplace=True, to_replace={'id_odor_duration': DURATION_LIST})
    # and change the column name to just "duration"
    df.rename(columns={'id_odor_duration': 'duration'}, inplace=True)

    # HEDONIC TONE: we rely on id_odor_annoy to add real numbers of hedonic tones from -4 to 4 according to VDI3882 standard
    df['hedonic_tone_n'] = df['id_odor_annoy']
    df.replace(inplace=True, to_replace={'hedonic_tone_n': ANNOY_ID_TO_REAL_NUMBER})
    # Now, we add text descriptions from VDI3882 that go in sync with the hedonic tone grades. They can be used interchangeably
    df['hedonic_tone_t'] = df['id_odor_annoy']
    df.replace(inplace=True, to_replace={'hedonic_tone_t': ANNOY_ID_TO_DESCRIPTION})
    # we can drop id_odor_annoy now
    df.drop('id_odor_annoy', inplace=True, axis=1)

    # INTENSITY: we rely on id_odor_intensity to add real numbers of intensity grades from 0 to 6 according to VDI3882 standard
    df['intensity_n'] = df['id_odor_intensity']
    df.replace(inplace=True, to_replace={'intensity_n': INTENSITY_ID_TO_REAL_NUMBER})
    # Now we add the text version of the same thing. As in hedonic tone, they can be used interchangeably
    df['intensity_t'] = df['id_odor_intensity']
    df.replace(inplace=True, to_replace={'intensity_t': INTENSITY_ID_TO_DESCRIPTION})

    # DATE AND TIME: We split date and time because it's useful for pattern detection
    df['date'] = pd.to_datetime(df['published_at']).dt.date
    df['time'] = pd.to_datetime(df['published_at']).dt.time
    # We add "week_day" column. OdourCollect does not provide it but it's useful for pattern detection
    df['week_day'] = df['date'].apply(day_of_week)
    # We can safely drop published_at column now
    df.drop('published_at', inplace=True, axis=1)

    # Finally, drop other spureous data like odourcollect's internal observation id or map colour
    df.drop('color', inplace=True, axis=1)
    df.drop('id', inplace=True, axis=1)

    # And reorder fields
    df = df[['user', 'date', 'time', 'week_day', 'category', 'type', 'hedonic_tone_n', 'hedonic_tone_t', 'intensity_n',
             'intensity_t', 'duration', 'latitude', 'longitude']]

    return df


def calculate_distance(point1lat, point1long, point2lat, point2long):
    # calculates distance in Km between two sets of gps coordinates.
    sanep1 = ocmodels.GPScoords(lat=float(point1lat), long=float(point1long))
    sanep2 = ocmodels.GPScoords(lat=float(point2lat), long=float(point2long))
    # distance calculation with haversine (we don't need higher precision when we measure distances of a few kms!)
    return round(hs.haversine((sanep1.lat, sanep1.long), (sanep2.lat, sanep2.long)), 2)


def add_distance_from_poi(df: pd.DataFrame, poilat, poilong) -> pd.DataFrame:
    # calculates distance ob observations (in KM) from a point of interest (POI)
    # we assume that a Pandas Dataframe made with build_df() is passed here
    df['distance'] = df.apply(lambda x: calculate_distance(x.latitude, x.longitude, poilat, poilong), axis=1)
    # df.style.format({'distance': '{:,.2f}'.format})
    return df

def check_path(filename):
    absolutepath = os.path.abspath(filename)
    if os.path.isdir(absolutepath):
        print('The intended output path for csv/xlsx file is a folder: {}'.format(absolutepath))
        print('Please, specify a different path using --output argument or delete/rename the existent folder')
        exit(2)
    if os.path.isfile(absolutepath):
        print('csv/xlsx file already exists: {}'.format(absolutepath))
        print('Please, specify a different path using --output argument or delete/rename the existent file')
        exit(2)
    fileformat = pathlib.Path(filename).suffix
    if fileformat not in ['.xlsx', '.csv']:
        print('Output file specified wit --output argument must have either ".csv" or ".xlsx" extension.')
        exit(2)
    return absolutepath


def df_to_file(df: pd.DataFrame, filename):
    from csv import QUOTE_NONNUMERIC
    # TODO: this can be greatly enhanced. It writes files with very few checks
    fileformat = pathlib.Path(filename).suffix
    finalpath = check_path(filename)
    if fileformat not in ['.xlsx', '.csv']:
        print('Output file path must have either ".csv" or ".xlsx" extension.')
        exit(2)
    elif fileformat == '.csv':
        print('Writing csv file: {}'.format(finalpath))
        df.to_csv(finalpath, quoting=QUOTE_NONNUMERIC, index=False)
    elif fileformat == '.xlsx':
        print('Writing xlsx file: {}'.format(finalpath))
        df.to_excel(finalpath, index=False)
