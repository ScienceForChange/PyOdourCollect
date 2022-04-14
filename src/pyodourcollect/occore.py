from ochelpers import *
import requests


def get_oc_data(query_params, outputfile, gpscoords):
    payload = build_ocrequest(query_params)
    r = requests.post(OC_ENDPOINT, json=payload, verify=True)
    if r.status_code != 200:
        print(f'Unexpected HTTP code received: {r.status_code}')
        exit(1)
    df = build_df(r.text)
    if gpscoords is not None:
        add_distance_from_poi(df, gpscoords.lat, gpscoords.long)
    # print(tabulate(df, headers='keys', tablefmt='fancy_grid'))
    return df
    #  -s 2021-01-01 -e 2021-12-31 --hedonic=unpleasant
