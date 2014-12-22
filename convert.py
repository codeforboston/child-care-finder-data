#!/usr/bin/env python3

import csv
import json
import re

output = {
    "type": "FeatureCollection",
    "features": []
}

def phone(number):
    return '-'.join((number[:3], number[3:6], number[6:]))

def split(value):
    return [v for v in value.split('; ') if v and v != "NULL"]

def yes_no(value):
    if value:
        return "Yes"
    else:
        return "No"

def all_sessions(line, value):
    return (split(line["Session1" + value]) +
            split(line["Session2" + value]) +
            split(line["Session3" + value]))

def strip_null(value):
    if not value or value == 'NULL':
        return ''
    return value

def titlecase(s):
    return re.sub(r"[A-Za-z]+('[A-Za-z]+)?",
        lambda mo: mo.group(0)[0:1].upper() +
                   mo.group(0)[1:].lower(),
    s)



def line_to_feature(line):
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [
                float(line["Longitude"]),
                float(line["Latitude"])]
        },
        "properties": {
            "name": line["ProgramName"],
            "address": titlecase(
                '\n'.join([l for l in [line["Address1"],
                                       line["Address2"]]
                           if l])),
            "city": titlecase(line["City"]),
            "zip": line["Zip"],
            "email": strip_null(line["eMailAddress"]),
            "url": "http://www.eec.state.ma.us/childcaresearch/ProvDetail.aspx?providerid=" + line["ProviderSiteID"],
            "phone": phone(line["Provider Phone"]),
            "capacity": int(line["Capacity"]),
            "type": line["Program Type"],
            "transport": split(line["Transportation"]),
            "food": yes_no(split(line["Meals"])),
            "help": yes_no(split(line["Financial Assistance"])),
            "special": yes_no(split(line["Special Needs"])),
            "duration": all_sessions(line, "Duration"),
            "dropin": all_sessions(line, "Drop_IN"),
            "before": all_sessions(line, "Bef_School"),
            "after": all_sessions(line, "After_School"),
            "holidays": all_sessions(line, "Open_Holidays"),
            "accept": [b for a in all_sessions(line, "Accepts_Children")
                       for b in a.split(" and ")]

        }
    }

with open('data.csv') as f:
    reader = csv.DictReader(f)
    for i, line in enumerate(reader):
        try:
            output["features"].append(line_to_feature(line))
        except:
            import traceback
            print("error parsing line {}", i)
            traceback.print_exc()

with open('data.geojson', 'w') as w:
    json.dump(output, w, separators=(',', ':'))
