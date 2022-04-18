import pyodourcollect.ochelpers as ochelpers
import requests


def get_oc_data(query_params, gpscoords):
    payload = ochelpers.build_ocrequest(query_params)
    r = requests.post(ochelpers.OC_ENDPOINT, json=payload, verify=True)
    if r.status_code != 200:
        print(f'Unexpected HTTP code received: {r.status_code}')
        exit(1)
    df = ochelpers.build_df(r.text)
    if gpscoords is not None:
        ochelpers.add_distance_from_poi(df, gpscoords.lat, gpscoords.long)
    # print(tabulate(df, headers='keys', tablefmt='fancy_grid'))
    return df
    #  -s 2021-01-01 -e 2021-12-31 --hedonic=unpleasant
