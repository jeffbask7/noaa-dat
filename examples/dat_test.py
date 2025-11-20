from noaa_dat.core import Dat
from datetime import datetime, timedelta, timezone
from pathlib import Path
import os

export_directory = 'data'
os.makedirs(export_directory, exist_ok=True)

start_time = datetime(2025,4,3,0)
end_time = datetime(2025,4,3,12)

start_time_str = start_time.strftime('%Y-%m-%d-%h')
end_time_str = end_time.strftime('%Y-%m-%d-%h')

lon_min = -95
lon_max = -85
lat_min = 25
lat_max = 40

export_filename = f'dat-{start_time_str}-to-{end_time_str}_{lon_min}-{lon_max}_{lat_min}-{lat_max}.csv'
print(f'{export_directory}/{export_filename}')




dat = Dat( start_time=start_time, end_time=end_time,
            lat_min=lat_min, lat_max=lat_max, lon_min=lon_min, lon_max=lon_max)

print('getting damage points')
df = dat.to_dataframe()
print('download complete')
print(df)


#export_filename = f'dat-{start_time_str}-{end_time_str}_{lon_min}-{lon_max}_{lat_min}-{lat_max}.csv'
#exp_path = Path(export_directory, export_filename)
df.to_csv(f'{export_directory}/{export_filename}', index=False)


