import numpy as np
import wget
import pandas as pd


url='''https://worldview.earthdata.nasa.gov/?v=150.92489600284233,-30.835367201702034,154.38592951943735,-29.0886268487955&l=VIIRS_SNPP_Thermal_Anomalies_375m_Day,VIIRS_SNPP_Thermal_Anomalies_375m_Night(hidden),Reference_Labels_15m(hidden),Reference_Features_15m(hidden),Coastlines_15m,VIIRS_SNPP_CorrectedReflectance_TrueColor,MODIS_Aqua_CorrectedReflectance_TrueColor(hidden),MODIS_Terra_CorrectedReflectance_TrueColor(hidden)&lg=false&t=2019-09-07-T15%3A25%3A24Z'''  

url=url.split("v=")
url= url[1].split("&l")
url=url[0].split(",")
# print(url)

lon1=float(url[0])
lon2=float(url[2])
lat1=float(url[1])
lat2=float(url[3])


dif_lat=np.abs(lat1-lat2)/2
dif_lon=np.abs(lon1-lon2)/2

data=pd.read_csv('./modis_2020_United_States.csv')

data_lon=data['longitude']
data_lat=data['latitude']
data_time=data['acq_date']



old_lat=0
old_lon=0
old_time=0
count=0

for lat,lon,time in zip(data_lat,data_lon,data_time):
    
    check=int(time.split('-')[1])
    if check<6:
        pass
    else:

        my_dict={
        'lat_small':[],
        'lat_big':[],
        'lon_small':[],
        'lon_big':[],
        'time':[],
        }

        count +=1
        print(count)
        if count>1500:
            break

        if old_time==time and lat-10<old_lat<lat+10 and lon-10<old_lon<lon+10:
            
            old_time=time
            old_lat=lat
            old_lon=lon
            print('GEÇTİM')
            pass

        else:
            lat_small= lat - dif_lat
            lat_big= lat + dif_lat
        
            lon_small= lon - dif_lon
            lon_big= lon + dif_lon
        
            
            my_dict['lat_small'].append(lat_small)
            my_dict['lat_big'].append(lat_big)
            my_dict['lon_small'].append(lon_small)
            my_dict['lon_big'].append(lon_big)
            my_dict['time'].append(time)


            print(my_dict)

            old_time=time
            old_lat=lat
            old_lon=lon

            import time
            for x in range(0,len(my_dict['time'])):
                
                url=f'''https://wvs.earthdata.nasa.gov/api/v1/snapshot?REQUEST=GetSnapshot&TIME={my_dict["time"][x]}T00:00:00Z&BBOX={my_dict["lat_small"][x]},{my_dict["lon_small"][x]},{my_dict["lat_big"][x]},{my_dict["lon_big"][x]}&CRS=EPSG:4326&LAYERS=MODIS_Terra_CorrectedReflectance_TrueColor&WRAP=day&FORMAT=image/jpeg&WIDTH=1657&HEIGHT=841&ts=1666297214625'''
                # url_2=f'https://wvs.earthdata.nasa.gov/api/v1/snapshot?REQUEST=GetSnapshot&TIME={my_dict["time"][x]}T00:00:00Z&BBOX={my_dict["lat_small"][x]},{my_dict["lon_big"][x]},{my_dict["lat_big"][x]},{my_dict["lon_small"][x]}&CRS=EPSG:4326&LAYERS=VIIRS_SNPP_CorrectedReflectance_TrueColor,Coastlines_15m,VIIRS_SNPP_Thermal_Anomalies_375m_Day&WRAP=day,x,none&FORMAT=image/jpeg&WIDTH=394&HEIGHT=394&ts=1663771937988'
                # https://wvs.earthdata.nasa.gov/api/v1/snapshot?REQUEST=GetSnapshot&TIME=2019-09-07T00:00:00Z&BBOX=-17.5422,144.5351,-15.8096,146.2678&CRS=EPSG:4326&LAYERS=VIIRS_SNPP_CorrectedReflectance_TrueColor,Coastlines_15m,VIIRS_SNPP_Thermal_Anomalies_375m_Day&WRAP=day,x,none&FORMAT=image/jpeg&WIDTH=394&HEIGHT=394&ts=1663771937988
                # https://wvs.earthdata.nasa.gov/api/v1/snapshot?REQUEST=GetSnapshot&TIME=2022-08-02T00:00:00Z&BBOX=-19.5477,-50.4551,-16.1429,-42.3216&CRS=EPSG:4326&LAYERS=VIIRS_NOAA20_CorrectedReflectance_TrueColor,Reference_Features_15m,Reference_Labels_15m&WRAP=day,x,x&FORMAT=image/jpeg&WIDTH=925&HEIGHT=387&ts=1666288083735
                time.sleep(2)
                print(url)

                try:
                    img=wget.download(url)
                except:
                    print('Görüntü yok')
                my_dict.clear()
                
