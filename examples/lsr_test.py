
from datetime import datetime
from noaa_dat.spc_lsr import LSR


start_time = datetime(2025,4,4,12)
end_time = datetime(2025,4,6,12)
lsr = LSR(start_date=start_time, end_date=end_time)
df = LSR.get_lsr(lsr)
print(df)
df.to_csv('data/lsr_test.csv', index=False)