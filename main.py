import numpy as np
import pandas as pd
import geopandas as gpd
import us
import os
import glob
import typer


def main(state_str: str, level: str = "block"):
    state = us.states.lookup(state_str)
    BASE = f"zip:///media/max/cabinet/census/ftp.census.gov/geo/tiger/TIGER2020PL/STATE/{state.fips}_{state.name.upper().replace(' ', '_')}/{state.fips}/"
    if level == "block":
        census_path = BASE + f"tl_2020_{state.fips}_tabblock20.zip"
        sumlev = 750
    elif level == "bg":
        census_path = BASE + f"tl_2020_{state.fips}_bg20.zip"
        sumlev = 150
    elif level == "vtd":
        census_path = BASE + f"tl_2020_{state.fips}_vtd20.zip"
        sumlev = 700
    elif level == "tract":
        census_path = BASE + f"tl_2020_{state.fips}_tract20.zip"
        sumlev = 140
    elif level == "county":
        census_path = BASE + f"tl_2020_{state.fips}_county20.zip"
        sumlev = 50
    elif level == "place":
        census_path = BASE + f"tl_2020_{state.fips}_place20.zip"
        sumlev = 160
    elif level == "cousub":
        census_path = BASE + f"tl_2020_{state.fips}_cousub20.zip"
        sumlev = 60
    elif level == "sldu":
        census_path = BASE + f"tl_2020_{state.fips}_sldu20.zip"
        sumlev = 610
    elif level == "sldl":
        census_path = BASE + f"tl_2020_{state.fips}_sldl20.zip"
        sumlev = 620
    elif level == "cd116":
        census_path = BASE + f"tl_2020_{state.fips}_cd116.zip"
        sumlev = 500
    else:
        raise ValueError

    census_shp = gpd.read_file(census_path)
    orig_len = len(census_shp) # debug
    filepaths = glob.glob(f"/media/max/cabinet/pl-94/{state.abbr.lower()}*/*.pl")

    f1path = ""
    f2path = ""
    geopath = ""
    for filename in filepaths:
        if filename.endswith("012020.pl"):
            f1path = filename
        elif filename.endswith("022020.pl"):
            f2path = filename
        elif "geo" in filename:
            geopath = filename

    assert f1path and f2path and geopath

    # read headers
    geoheaders = list(pd.read_excel('2020_PLSummaryFile_FieldNames.xlsx', sheet_name=2))
    f1headers = list(pd.read_excel('2020_PLSummaryFile_FieldNames.xlsx', sheet_name=4))
    f2headers = list(pd.read_excel('2020_PLSummaryFile_FieldNames.xlsx', sheet_name=6))
    f3headers = list(pd.read_excel('2020_PLSummaryFile_FieldNames.xlsx', sheet_name=8))

    # do not need the third file, read the others
    f1 = pd.read_csv(f1path, names = f1headers, delimiter = '|')
    f2 = pd.read_csv(f2path, names = f2headers, delimiter = '|')
    geo = pd.read_csv(geopath, names = geoheaders, delimiter = '|', low_memory=False)

    # join f1 to f2
    joined = f1.merge(f2, on='LOGRECNO')

    # get columns we want
    wanted_cols = pd.read_excel('col_map.xlsx')
    cols = list(wanted_cols['Census'])
    cols.append('LOGRECNO')

    # subset to what we want
    joined = joined[cols]

    # map census names to mggg names
    mapper = {
        c: "LOGRECNO" if c == "LOGRECNO" else wanted_cols[wanted_cols['Census'] == c].iloc[0]['MGGG'] for c in cols
    }
    joined = joined.rename(mapper = mapper, axis = 1)

    # add geographic info
    with_geo = joined.merge(geo[['LOGRECNO', 'GEOCODE', 'SUMLEV']], on = 'LOGRECNO')
    with_geo['GEOCODE'] = with_geo['GEOCODE'].apply(str)
    with_geo = with_geo[with_geo['SUMLEV'] == sumlev]
    print(with_geo)
    census_shp['GEOID20'] = census_shp['GEOID20'].apply(str)

    # add geometry
    if not os.path.isdir(f"final/{state.abbr.lower()}"):
        os.makedirs(f"final/{state.abbr.lower()}")

    final = census_shp.merge(with_geo, left_on='GEOID20', right_on='GEOCODE')
    final.to_file(f"final/{state.abbr.lower()}/{state.abbr.lower()}_{level}.shp")
    final_len = len(final)
    print(orig_len, final_len)

if __name__ == "__main__":
    typer.run(main)
