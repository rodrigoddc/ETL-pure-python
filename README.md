# API single pure python script
## api-consume-and-normalize-data

Single Pure Python script, service oriented, to make a request to https://www.jodidata.org/_resources/files/downloads/gas-data/jodi_gas_csv_beta.zip download, unzip, extract, parse csv, normalize dataset and retrieve data

### Steps:
1.  Downloaded resource from the URL `https://www.jodidata.org/_resources/files/downloads/gas-data/jodi_gas_csv_beta.zip` as input;
2.  Unziped and parsed csv to list of csv.DictReader;
3.  Normalized data sorting and aggregating by zone as Key, time period formated to ISO 8061, and the others fields as dicts;
4.  Parsed as json;
4.  Resulting from this:
   
``` 
[{'REF_AREA': 'ZA', 'TIME_PERIOD': '2018-08', 'ENERGY_PRODUCT': 'NATGAS', 'FLOW_BREAKDOWN': 'TOTIMPSB', 'UNIT_MEASURE': 'M3', 'OBS_VALUE': '355', 'ASSESSMENT_CODE': '1'},
{'REF_AREA': 'ZA', 'TIME_PERIOD': '2018-08', 'ENERGY_PRODUCT': 'NATGAS', 'FLOW_BREAKDOWN': 'TOTIMPSB', 'UNIT_MEASURE': 'TJ', 'OBS_VALUE': '13878', 'ASSESSMENT_CODE': '1'},
{'REF_AREA': 'UY', 'TIME_PERIOD': '2017-10', 'ENERGY_PRODUCT': 'NATGAS', 'FLOW_BREAKDOWN': 'TOTDEMO', 'UNIT_MEASURE': 'M3', 'OBS_VALUE': '5', 'ASSESSMENT_CODE': '1'},
{'REF_AREA': 'UY', 'TIME_PERIOD': '2017-10', 'ENERGY_PRODUCT': 'NATGAS', 'FLOW_BREAKDOWN': 'TOTIMPSB', 'UNIT_MEASURE': 'M3', 'OBS_VALUE': '6', 'ASSESSMENT_CODE': '1'},
{'REF_AREA': 'VE', 'TIME_PERIOD': '2011-01', 'ENERGY_PRODUCT': 'LNG', 'FLOW_BREAKDOWN': 'EXPLNG', 'UNIT_MEASURE': 'KTONS', 'OBS_VALUE': '0', 'ASSESSMENT_CODE': '3'},
{'REF_AREA': 'VE', 'TIME_PERIOD': '2011-01', 'ENERGY_PRODUCT': 'LNG', 'FLOW_BREAKDOWN': 'EXPLNG', 'UNIT_MEASURE': 'M3', 'OBS_VALUE': '0', 'ASSESSMENT_CODE': '2'},
{'REF_AREA': 'VE', 'TIME_PERIOD': '2011-01', 'ENERGY_PRODUCT': 'LNG', 'FLOW_BREAKDOWN': 'IMPLNG', 'UNIT_MEASURE': 'KTONS', 'OBS_VALUE': '0', 'ASSESSMENT_CODE': '3'},
{'REF_AREA': 'VE', 'TIME_PERIOD': '2011-01', 'ENERGY_PRODUCT': 'LNG', 'FLOW_BREAKDOWN': 'IMPLNG', 'UNIT_MEASURE': 'M3', 'OBS_VALUE': '0', 'ASSESSMENT_CODE': '2'},
{'REF_AREA': 'US', 'TIME_PERIOD': '2014-09', 'ENERGY_PRODUCT': 'NATGAS', 'FLOW_BREAKDOWN': 'TOTIMPSB', 'UNIT_MEASURE': 'TJ', 'OBS_VALUE': '217004', 'ASSESSMENT_CODE': '1'},
{'REF_AREA': 'US', 'TIME_PERIOD': '2014-10', 'ENERGY_PRODUCT': 'NATGAS', 'FLOW_BREAKDOWN': 'CLOSTLV', 'UNIT_MEASURE': 'M3', 'OBS_VALUE': '101580', 'ASSESSMENT_CODE': '1'}] 
 ```

to this:

```
{'US': {'periods': ['2014-05-01T00:00:00', '2014-04-01T00:00:00'],
        'fields': [{'ENERGY_PRODUCT': 'LNG', 'FLOW_BREAKDOWN': 'EXPLNG', 'UNIT_MEASURE': 'KTONS', 'OBS_VALUE': '0', 'ASSESSMENT_CODE': '3'},
                   {'ENERGY_PRODUCT': 'NATGAS', 'FLOW_BREAKDOWN': 'EXPLNG', 'UNIT_MEASURE': 'KTONS', 'OBS_VALUE': '0', 'ASSESSMENT_CODE': '3'}]}
        }
}
```
5.  Wrote to stdout as JSON

