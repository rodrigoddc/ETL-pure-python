"""
As 'the goal is to create a single python2/3 file that uses only standard libraries',
that's my best solution according to the deadline
"""
import csv
import sys
from collections import defaultdict
from datetime import datetime
from io import BytesIO, TextIOWrapper
from itertools import groupby
from operator import itemgetter
from pprint import pprint
from urllib import request
from zipfile import ZipFile


# CONSTANTS corresponding full names in JODI Database CSV

# IMPORTANT
# I would create CONSTANTS to explain FLOW_BREAKDOWN and UNIT_MEASURE but at
# source https://www.jodidata.org/_resources/files/downloads/gas-data/jodi-gas-wdb-short--long-names-ver2018.pdf
# are missing some values who exists in csv
# source in https://www.jodidata.org/_resources/files/downloads/gas-data/jodi_gas_csv_beta.zip

# Just 2 keys: values becaus NATGAS is explained by UNIT_MEASURE
ENERGY_PRODUCT = {'NATGAS': 'Natural Gas',
                  'LNG': 'Natural Gas (in form of LNG) in 1000 metric tons'}

# I've considered creating a CONSTANT with all country codes, but as explained on
# source https://www.jodidata.org/_resources/files/downloads/gas-data/jodi-gas-wdb-short--long-names-ver2018.pdf
# there are 249 country codes at this source http://www.iso.org/iso/home/store/publication_item.htm?pid=PUB500001%3aen
# So this CONSTANT is just to make REF_AREA meaningful
REF_AREA = 'Country code based on ISO 3166-1 alpha-2 standard'

ASSESSMENT_CODE = {'1': 'Results of the assessment show reasonable levels of comparability',
                   '2': 'Consult metadata/Use with caution',
                   '3': 'Data has not been assessed'}


def main_service():
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
    Receives a url, try to make a request and download its content, after that the content of the request is returned
    :param url: string representation of source
    :return: resquest content data
    """
    data_requested = request.urlopen(url)

    return data_requested.read()


def service_extract_data(data_received: bytes) -> list:
    """
    Service to extract zipped data from bytes that have been downloaded
    :param data_received: data received as bytes from external source
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
    Receives a list of dicts from source csv and group its data according to desireble fields
    :param data_extracted: list of dict read from csv
    :return: dict of grouped series dict
    """

    data_xt = sorted(data_extracted, key=itemgetter('REF_AREA'))

    data_tmp = defaultdict(list)

    # for this time series, as i couldn't inquire which specific field is intended to be analyzed,
    # i've assumed that all fields could be a case of analysis, so the data were grouped by all fields
    # cause OBS_VALUE problally is the observated value for his previous columns grouped case on csv
    for key, group in groupby(data_xt, key=itemgetter('REF_AREA', 'ENERGY_PRODUCT', 'FLOW_BREAKDOWN',
                                                      'UNIT_MEASURE', 'ASSESSMENT_CODE')):
        data_tmp[key].append(list(group))

    return data_tmp


def service_data_as_list_of_series(data_grouped: dict) -> list:
    """
    Receives a dict of grouped data and manipulate over it to return list of series data
    :param data_grouped: list of grouped data
    :return: list of series
    """

    data_series_list = []
    for key, value in data_grouped.items():

        series_dict = {}
        points_agg = []

        for item in value:
            for v in item:

                # TIME_PERIOD forced formatted as datetime on ISO 8601, as tasks asks, provided by native isoformat
                points_agg.append([datetime.strptime(v.get('TIME_PERIOD'), '%Y-%m').isoformat(), float(v.get('OBS_VALUE'))])

                series_dict = {'series_id': '\\'.join(map(str, key)),
                               # REF_AREA concat just to be meaningful, it could over info
                               'fields': {'REF_AREA': ', '.join([v.get('REF_AREA'), REF_AREA]),
                                          'ENERGY_PRODUCT': ', '.join([v.get('ENERGY_PRODUCT'),
                                                                       ENERGY_PRODUCT[v.get('ENERGY_PRODUCT')]]),
                                          'FLOW_BREAKDOWN': v.get('FLOW_BREAKDOWN'),
                                          'UNIT_MEASURE': v.get('UNIT_MEASURE'),
                                          'ASSESSMENT_CODE': ', '.join([v.get('ASSESSMENT_CODE'),
                                                                        ASSESSMENT_CODE[v.get('ASSESSMENT_CODE')]])}}

        series_dict['points'] = points_agg

        data_series_list.append(series_dict)

    return data_series_list


def service_write_to_stdout(data_manipulated: list) -> None:
    """
    Helpfull function to writes received data param to stdout
    :param data_manipulated: list of series rpr
    :return: None
    """
    for item in data_manipulated:

        # pprint(item, indent=4)

        # if a real json obj is desired to be printed:
        # whitou indent cause is asked one series per line
        import json
        print(json.dumps(item))

    # if desired a file data.json as result:
    #     import json
    #     with open('data.json', 'a') as f:
    #         json.dump(item, f, indent="\t")


if __name__ == '__main__':
    main_service()
    print('_'*10)
    sys.stdout.write(str(bytes.fromhex('62792068747470733a2f2f6769746875622e636f6d2f726f647269676f6464632f')
                         .decode('utf-8')))
