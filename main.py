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


def shooju_senior():
    """
    Main function who call unacouple services to divide
    responsibilities and facilitate maintenance and readability
    :return: None
    """
    url = 'https://www.jodidata.org/_resources/files/downloads/gas-data/jodi_gas_csv_beta.zip'

    dt_downloaded = service_download_data(url)
    dt_extracted = service_extract_data(dt_downloaded)
    dt_manipulated_to_json_series = service_manipulate_data(dt_extracted)
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


def service_manipulate_data(data_extracted: list) -> dict:
    """

    :param data_extracted:
    :return:
    """

    data = defaultdict(list)

    data_xt = deepcopy(sorted(data_extracted, key=itemgetter('REF_AREA')))
    x = defaultdict(list)
    for key, group in groupby(data_xt, key=itemgetter('REF_AREA', 'ENERGY_PRODUCT', 'FLOW_BREAKDOWN',
                                                      'UNIT_MEASURE', 'ASSESSMENT_CODE')):
        data[key].append(list(group))

    return data


def service_write_to_stdout(data_manipulated: dict) -> None:
    for item in data_manipulated.items():
        pprint(item, indent=4)
        # if a json like obj is really desired to be printed:
        # import json
        # print(json.dumps(item, indent=4))

    # if desired data.json as result:
    # import json
    # with open('data.json', 'w') as f:
    #     json.dump(data_manipulated, f, indent=4)


if __name__ == '__main__':
    shooju_senior()
    print('_'*10)
    sys.stdout.write(str(bytes.fromhex('62792068747470733a2f2f6769746875622e636f6d2f726f647269676f6464632f').decode('utf-8')))
