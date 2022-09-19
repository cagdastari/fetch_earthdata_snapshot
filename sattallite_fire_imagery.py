import numpy as np
import wget




url='''https://worldview.earthdata.nasa.gov/?v=150.92489600284233,-30.835367201702034,154.38592951943735,-29.0886268487955
&l=VIIRS_SNPP_Thermal_Anomalies_375m_Day,VIIRS_SNPP_Thermal_Anomalies_375m_Night(hidden),Reference_Labels_15m(hidden),
Reference_Features_15m(hidden),Coastlines_15m,VIIRS_SNPP_CorrectedReflectance_TrueColor,MODIS_Aqua_CorrectedReflectance_TrueColor
(hidden),MODIS_Terra_CorrectedReflectance_TrueColor(hidden)&lg=false&t=2019-09-07-T15%3A25%3A24Z'''  

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

lat=-30.17596
lon=152.27618

if lat<0:
    lat_small= lat + dif_lat
    lat_big= lat - dif_lat
else:
    lat_small= lat - dif_lat
    lat_big= lat + dif_lat

if lon<0:
    lon_small= lon + dif_lon
    lon_big= lon - dif_lon
else:
    lon_small= lon - dif_lon
    lon_big= lon + dif_lon



url=f'''https://wvs.earthdata.nasa.gov/api/v1/snapshot?REQUEST=GetSnapshot&TIME=2019-09-07T00:00:00Z&BBOX={lat_big},{lon_small},{lat_small},{lon_big}
&CRS=EPSG:4326&LAYERS=VIIRS_SNPP_CorrectedReflectance_TrueColor,Coastlines_15m&WRAP=day,x&FORMAT=image/jpeg&WIDTH=612&HEIGHT=332&ts=1663590759376'''

img=wget.download(url)




