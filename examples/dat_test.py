from noaa_dat.core import Dat
from datetime import datetime, timedelta, timezone
from pathlib import Path
import os

#DEFINE OUTPUT DIRECTORY
export_directory = 'data'
os.makedirs(export_directory, exist_ok=True)

#DEFINE START AND END TIMES AS DATETIME OBJECTS
start_time = datetime(2025,4,4,0)
end_time = datetime(2025,4,4,12)

#CREATE STRING VERSIONS OF START AND END TIMES FOR USE IN EXPORT FILENAME
start_time_str = start_time.strftime('%Y-%m-%d-%h')
end_time_str = end_time.strftime('%Y-%m-%d-%h')

#DEFINE LAT/LON BOUNDS
lon_min = -95
lon_max = -85
lat_min = 25
lat_max = 40

#DEFINE EXPORT FILE NAME
export_filename = f'dat-{start_time_str}-to-{end_time_str}_{lon_min}-{lon_max}_{lat_min}-{lat_max}.csv'
print(f'{export_directory}/{export_filename}')

#CREATE EXPORT PATH OBJECTS
export_path = Path(export_directory, export_filename)

#CREATE DAT OBJECT
dat = Dat( start_time=start_time, end_time=end_time,
            lat_min=lat_min, lat_max=lat_max, lon_min=lon_min, lon_max=lon_max)

#CALL TO_DATAFRAME ON DAT OBJECT TO RETURN RESULTS AS PANDAS DATAFRAME
print('getting damage points')
gdf = dat.to_geodataframe()
print('download complete')
print(gdf)

#SAVE RESULTS TO CSV
gdf.to_csv(export_path, index=False)
#SAVE RESULTS AS GEOPACKAGE
gdf.to_file(export_path, layer='damage_points', driver='GPKG')
#SAVE RESULTS AS SHAPE FILE
gdf.to_file(export_path)


