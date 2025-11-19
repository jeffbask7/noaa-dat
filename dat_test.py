from noaa_dat.core import Dat
from datetime import datetime, timedelta, timezone

start_time = datetime(2025,4,3,0)
end_time = datetime(2025,4,3,12)

lon_min = -95
lon_max = -85
lat_min = 25
lat_max = 40

apr25 = Dat( start_time=start_time, end_time=end_time,
            lat_min=lat_min, lat_max=lat_max, lon_min=lon_min, lon_max=lon_max)

contents_json = apr25.get_dat()
print('full json: ', contents_json)
features = contents_json['features']
for feature in features:
    print(feature)


