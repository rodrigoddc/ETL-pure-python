"""
As 'the goal is to create a single python2/3 file that uses only standard libraries',
that's my best solution according to the deadline
"""
import csv
import sys
from collections import defaultdict
from copy import deepcopy
from datetime import datetime
from io import BytesIO, TextIOWrapper
from itertools import groupby
from operator import itemgetter
from pprint import pprint
from urllib import request
from zipfile import ZipFile


# Constants corresponding full names in JODI Database CSV

ENERGY_PRODUCT = {'NATGAS': 'Natural Gas',
                  'LNG': 'Natural Gas (in form of LNG) in 1000 metric tons'}

FLOW_BREAKDOWN = {'INSDPROD': 'Production ', 'OSOURCES': 'Receipts from Other Sources',
                  'TOTIMPSB': 'Imports', 'IMPLNG': 'LNG (import)', 'IMPPIP': 'Pipeline (import)',
                  'TOTEXPSB': 'Exports', 'EXPLNG': 'LNG (export)', 'EXPPIP': 'Pipeline (export)',
                  'STOCKCH': 'Stock Change', 'TOTDEMC': 'Gross Inland Deliveries (Calculated)',
                  'STATDIFF': 'Statistical Difference', 'TOTDEMO': 'Gross Inland Deliveries (Observed)',
                  'MAINTOT': 'of which: Electricity and Heat Generation', 'CLOSTLV': 'Closing Stocks',
                  'CONVER': 'Conversion factor (m3/tonne)'}

REF_AREA = ' - Country code based on ISO 3166-1 alpha-2 standard'

UNIT_MEASURE = {'M3': 'Natural Gas in Million m3 (at 15oC, 760 mm hg)',
                'TJ': 'Natural Gas in Terajoules',
                'KT': 'LNG in 1000 tonnes'}

ASSESSMENT_CODE = {'1': 'Results of the assessment show reasonable levels of comparability',
                '2': 'Consult metadata/Use with caution',
                '3': 'Data has not been assessed'}

def shooju_senior():
    """
    Main function who call unacouple services to divide
    responsibilities and facilitate maintenance and readability
    :return: None
    """
    url = 'https://www.jodidata.org/_resources/files/downloads/gas-data/jodi_gas_csv_beta.zip'

    dt_downloaded = service_download_data(url)
    dt_extracted = service_extract_data(dt_downloaded)
    data_grouped = service_grouped_data(dt_extracted)
    dt_manipulated_to_json_series = service_data_as_list_of_series(data_grouped)
    service_write_to_stdout(dt_manipulated_to_json_series)


def service_download_data(url: str):
    """
    Receive a url, try to make a request and download its content, after that the content of the request is returned
    :param url:
    :return: resquest content data
    """
    data_requested = request.urlopen(url)

    return data_requested.read()


def service_extract_data(data_received: bytes) -> list:
    """
    Service to extract zipped data from bytes that have been downloaded
    :return: unzip data as list of csv.DictReader
    """
    ziped_bytes = BytesIO(data_received)

    with ZipFile(ziped_bytes) as ziped_files:
        for item in ziped_files.infolist():
            with ziped_files.open(item.filename) as export:
                # assuming that has just one item, cause this is the source case
                reader = list(csv.DictReader(TextIOWrapper(export, 'utf-8')))

    return reader


def service_grouped_data(data_extracted: list) -> dict:
    """

    :param data_extracted:
    :return:
    """

    data_xt = deepcopy(sorted(data_extracted, key=itemgetter('REF_AREA')))

    data_tmp = defaultdict(list)
    for key, group in groupby(data_xt, key=itemgetter('REF_AREA', 'ENERGY_PRODUCT', 'FLOW_BREAKDOWN',
                                                      'UNIT_MEASURE', 'ASSESSMENT_CODE')):
        data_tmp[key].append(list(group))

    return data_tmp


def service_data_as_list_of_series(data_grouped: dict) -> list:
    data_series_list = []
    for key, value in data_grouped.items():

        series_dict = {}
        points_agg = []
        for item in value:
            for v in item:
                points_agg.append([v.get('TIME_PERIOD'), v.get('OBS_VALUE')])
                series_dict = {'series_id': key,
                           'fields': {'REF_AREA': v.get('REF_AREA'),
                                      'ENERGY_PRODUCT': v.get('ENERGY_PRODUCT'),
                                      'FLOW_BREAKDOWN': v.get('FLOW_BREAKDOWN'),
                                      'UNIT_MEASURE': v.get('UNIT_MEASURE'),
                                      'ASSESSMENT_CODE': v.get('ASSESSMENT_CODE')
                                      }
                           }

        series_dict['points'] = points_agg
        data_series_list.append(series_dict)
    return data_series_list

def service_write_to_stdout(data_manipulated: list) -> None:

    # for item in data_manipulated:
        # pprint(item, indent=4)

        # if a json like obj is really desired to be printed:
        # import json
        # print(json.dumps(item, indent=4))

    # if desired data.json as result:
    import json
    with open('MARCO.json', 'w') as f:
        json.dump(data_manipulated, f, indent=2)


if __name__ == '__main__':
    shooju_senior()
    print('_'*10)
    sys.stdout.write(str(bytes.fromhex('62792068747470733a2f2f6769746875622e636f6d2f726f647269676f6464632f').decode('utf-8')))
