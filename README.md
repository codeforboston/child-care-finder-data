child-care-finder-data
======================

Data/scripts powering the EEC MA Child Care Finder

How to use
----------

* export your data (using Excel or Numbers) to `data.csv`
* run `python3 convert.py` which creates/updates `data.geojson`
* `git add ProgramlistforChildCareSearch.xlsx data.csv data.geojson`
* `git commit -m 'updated data!'
* `git push`
* copy `data.geojson` to [child-care-finder](https://github.com/codeforboston/child-care-finder) and check it in there
