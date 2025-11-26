import requests
from datetime import datetime, timedelta, timezone
from noaa_dat._constants import BASE_URL, OUT_FIELDS, OUT_SR
import pandas as pd
import geopandas as gpd

class Dat:
    def __init__(self, start_time=None, end_time=None, lat_min=None, lat_max=None, lon_min=None, lon_max=None, format_out='geojson'):
        self.start_time = start_time
        self.end_time = end_time
        self.lat_min = lat_min
        self.lat_max = lat_max
        self.lon_min = lon_min
        self.lon_max = lon_max
        self.f = format_out

        start_year = self.start_time.year
        start_month = (str(self.start_time.month)).zfill(2)
        start_day = (str(self.start_time.day)).zfill(2)
        start_hour = (str(self.start_time.hour)).zfill(2)

        end_year = self.end_time.year
        end_month = (str(self.end_time.month)).zfill(2)
        end_day = (str(self.end_time.day)).zfill(2)
        end_hour = (str(self.end_time.hour)).zfill(2)

        #self.where = f"""stormdate+BETWEEN+TIMESTAMP+%272025-04-03+00%3A00%3A00%27+AND+TIMESTAMP+%272025-04-03+06%3A00%3A00%27+"""
        self.where = f"""stormdate+BETWEEN+TIMESTAMP+%27{start_year}-{start_month}-{start_day}+{start_hour}%3A00%3A00%27+AND+TIMESTAMP+%27{end_year}-{end_month}-{end_day}+{end_hour}%3A00%3A00%27+"""
        self.geometry = (str({"xmin":self.lon_min,
                         "ymin":self.lat_min,
                         "xmax":self.lon_max,
                         "ymax":self.lat_max,
                         "spatialReference":{"wkid":4326}})).replace("'", '"')
        
    def build_url(self) -> str:
        params = {
            "where":f"{self.where}",
            "text":"",
            "objectIds":"",
            "time":"",
            "timeRelation":"esriTimeRelationOverlaps",
            "geometry":f"{self.geometry}",
            "geometryType":"esriGeometryEnvelope",
            "inSR":"",
            "spatialRel":"esriSpatialRelIntersects",
            "distance":"",
            "units":"esriSRUnit_Foot",
            "relationParam":"",
            "outFields":OUT_FIELDS,
            "returnGeometry":"true",
            "returnTrueCurves":"false",
            "maxAllowableOffset":"",
            "geomteryPrecision":"",
            "outSR": OUT_SR,
            "havingClause":"",
            "returnIdsOnly":"false",
            "returnCountOnly":"false",
            "orderByFields":"",
            "groupByFieldsForStatistics":"",
            "outStatistics":"",
            "returnZ":"false",
            "returnM":"false",
            "gdbVersion":"",
            "historicMoment":"",
            "returnDistinctValues":"false",
            "resultOffset":"",
            "resultRecordCount":"",
            "returnExtentOnly":"false",
            "sqlFormat":"none",
            "datumTransformation":"",
            "parameterValues":"",
            "rangeValues":"",
            "quantizationParameters":"",
            "featureEncoding":"esriDefault",
            "f":f"{self.f}"
            }
        
        url_str = BASE_URL
        for key, value in params.items():
            param = f"{key}={value}"
            #print(param)
            if url_str == BASE_URL:
                url_str = url_str + param
            else:
                url_str = url_str + "&" + param
        return url_str
    
    def get_dat(self) -> dict:
        url_str = Dat.build_url(self)
        print(url_str)
        result = requests.get(url_str)
        contents_json = result.json()
        return contents_json
    
    def to_dataframe(self) -> pd.DataFrame:
        contents_json = Dat.get_dat(self)
        df = pd.json_normalize(contents_json, record_path='features')
        df = df.drop('type', axis=1)
        cols = list(df.columns)
        newcols = [x.split('.')[1] for x in cols if len(x.split('.')) > 1]
        cols_rename = dict(zip(cols[1:],newcols))
        df = df.rename(columns=cols_rename)
        df['stormdate'] = pd.to_datetime(df['stormdate']*1000000)
        df['surveydate'] = pd.to_datetime(df['surveydate']*1000000)
        return df
    
    def to_geodataframe(self) -> gpd.Geodataframe:
        df = Dat.to_dataframe(self)
        gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(x=df['lon'], y=df['lat']), crs='EPSG:4326')
        return gdf
