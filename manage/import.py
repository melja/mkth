from urllib.request import urlretrieve
import json
from flask import current_app
from datetime import datetime, timezone

url = (
    "http://unicode.org/Public/cldr/latest"
)
filename = "temp/cldr_latest.html"

def get_latest_cldr_version():
    urlretrieve(url, filename)

def retrieve_cldr(version):
    pass

def retrieve_cldr_zone_data():
    source_url = "https://github.com/unicode-org/cldr-json/raw/main/cldr-json/cldr-core/supplemental/metaZones.json"
    temp_filename = "temp/metaZones.json"
    output_filename = "manage/reference_data/timezones.json"
    urlretrieve(source_url, temp_filename)
    timezones = []
    inf = open(temp_filename, "r")
    try:
        tz_data = inf.read()
        tz_json = json.loads(tz_data)
        tz_version = tz_json["supplemental"]["version"]["_cldrVersion"]
        tz_cats = tz_json["supplemental"]["metaZones"]["metazoneInfo"]["timezone"]
        for category, cat_value in tz_cats.items():
            if isinstance(cat_value, dict):
                for tzone, metazones in cat_value.items():
                    for mz in metazones:
                        if "usesMetazone" in mz:
                            if "_to" not in mz["usesMetazone"]:
                                metazone = mz["usesMetazone"]["_mzone"]
                    #print(f"{category}/{timezone} { metazone }")
                    timezones.append([category, tzone, metazone])
    except Exception as e:
        print(e)
    finally:
        inf.close()

    ouf = open(output_filename, "w")
    file_out = {
            "data_format": 0,
            "schema_version": 1,
            "datasource": {
                "id": "CLDR_tz",
                "version": tz_version,
                "title": "Unicode Common Locale Data Repository (CLDR) Timezone Data",
                "retrieved": datetime.now(timezone.utc).isoformat(),
                "steward": "Unicode CLDR",
                "license": "https://www.unicode.org/copyright.html",
                "url": source_url
            },
            "table_data": [
                {
                    "tablename": "timezones",
                    "columns": [
                        "region",
                        "timezone",
                        "metazone"
                    ],
                    "key_columns": [
                        "region",
                        "timezone"
                    ],
                    "row_data": timezones
                }
            ]
        }
    try:
        ouf.write(json.dumps(file_out, indent=2))
    except Exception as e:
        print(e)
    finally:
        ouf.close()

    #return timezones


retrieve_cldr_zone_data()