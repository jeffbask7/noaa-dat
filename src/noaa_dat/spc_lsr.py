from datetime import datetime, timedelta, timezone
from pathlib import Path
import pandas as pd
import geopandas as gpd
import os
import requests
from io import StringIO
import numpy as np

class LSR:
    def __init__(self, start_date=None, end_date=None):
        self.start_date=start_date
        self.end_date=end_date
        self.start_date_str = self.start_date.strftime('%Y-%m-%d-%h')
        self.end_date_str = self.end_date.strftime('%Y-%m-%d-%h')


    def lsr_download(date:datetime) -> pd.DataFrame:
        year_str = date.year - 2000
        month_str = (str(date.month)).zfill(2)
        day_str = (str(date.day)).zfill(2)
        url = f"https://www.spc.noaa.gov/climo/reports/{year_str}{month_str}{day_str}_rpts_filtered.csv"
        response = requests.get(url)
        contents = response.text
        df = pd.read_csv(StringIO(contents), header=None)
        #df['Datetime'] = np.where(df['Time'].astype(int) < 1200, date , date + timedelta(days=1))
        return df
    
    def normalize_magnitude(df):
        cols = list(df.columns)
        match cols[1]:
            case 'F_Scale':
                df['Event_Type'] = 'TOR'
                df['Magnitude'] = df['F_Scale']
                df = df.drop('F_Scale', axis=1)
            case 'Speed':
                df['Event_Type'] = 'WIND'
                df['Magnitude'] = df['Speed']
                df = df.drop('Speed', axis=1)
            case 'Size':
                df['Event_Type'] = 'HAIL'
                df['Magnitude'] = df['Size']
                df = df.drop('Size', axis=1)
        return df

    def get_lsr(self):
        df_raw_list = []
        date_range = pd.date_range(self.start_date, self.end_date)
        date_range = (list(date_range))
        for date in date_range:
            df = LSR.lsr_download(date)
            df_raw_list.append(df)
        df = df_raw_list[0]
        dataframes = []
        block = []
        header_list = ['F_Scale','Speed', 'Size']
        for df in df_raw_list:
            for _, row in df.iterrows():
                # A header is detected when row[0] is a string and block contains data
                if row[1] in header_list and block:
                    df0 = pd.DataFrame(block[1:], columns=block[0])
                    dataframes.append(df0)
                    block = []

                block.append(row.tolist())

            # Append the last block
            if block:
                df0 = pd.DataFrame(block[1:], columns=block[0])
                dataframes.append(df0)

            df1 = pd.DataFrame()
            for df in dataframes:
                df = LSR.normalize_magnitude(df)
                df1 = pd.concat([df1, df])

            df1['Datetime'] = np.where(df1['Time'].astype(int) < 1200, date , date + timedelta(days=1))
            hours = df1['Time'].str.slice(0, 2).astype(int)
            minutes = df1['Time'].str.slice(2, 4).astype(int)
            offset = pd.to_timedelta(hours, unit='h') + pd.to_timedelta(minutes, unit='m')
            df1['Datetime'] = df1['Datetime'].dt.normalize() + offset
            df1 = df1[['Datetime','Time','Event_Type','Magnitude', 'Location','County','State','Lat','Lon','Comments']]
            return df1
        
if __name__=="__main__":
    start_time = datetime(2025,4,4,12)
    end_time = datetime(2025,4,6,12)
    lsr = LSR(start_date=start_time, end_date=end_time)
    df = LSR.get_lsr(lsr)
    print(df)
    df.to_csv('lsr_test.csv', index=False)