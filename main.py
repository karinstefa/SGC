
#%%Libreries 
import pandas as pd
import numpy as np 
from read_api import readAPI

#%% read URL
url = "https://archive.sgc.gov.co/feed/v1.0/notifications/notifications.json"
json_data =readAPI(url)
# %%
notifications_list = json_data['notifications']
#%%
import folium

## Datos 
#volcanes = [
#    {
#        'name': 'Volcán Nevado del Huila',
#        'lat': 2.924,
#        'lon': -76.029,
#        'popup': "<strong>Volcán Nevado del Huila</strong><br>ID: 1<br>Latitud: 2.924<br>Longitud: -76.029",
#    },
#    {
#        'name': 'Volcán Puracé',
#        'lat': 2.313,
#        'lon': -76.395,
#        'popup': "<strong>Volcán Puracé</strong><br>ID: 2<br>Latitud: 2.313<br>Longitud: -76.395",
#    }
#]

volcanes =notifications_list[1]["properties"]
#%%
# Crear el mapa
mapa = folium.Map(location=[notifications_list[1]["properties"]["latitude"], notifications_list[1]["properties"]["longitude"]], zoom_start=8)

activityDict = { 1:['red', 'Rojo'], 2:['orange','Naranja'], 3:['yellow','Amarillo'], 4:['green', 'verde'] }

#%%
# Añadir marcadores de los volcanes
for volcan in notifications_list:
    if volcan['type'] == 'volcano':
        volcan = volcan["properties"]
        folium.Marker(
            [volcan['latitude'], volcan['longitude']],
            popup=f"<h5>{volcan['VolcanoName']}</h5><br><b>Nivel:</b>{activityDict[volcan['activityLevel']][1]}<br><b>Nivel2: </b>{volcan['activityLevel']}<br><a target='_blank' href='{volcan['bulletins'][0]['file']}'>Boletin</a>",
            icon=folium.Icon(color=activityDict[volcan['activityLevel']][0], icon='info-sign')
        ).add_to(mapa)
    elif volcan['type'] == 'earthquake':
        volcan['latitude'] = volcan['geometry']['coordinates'][0]
        volcan['longitude'] = volcan['geometry']['coordinates'][1]
        folium.Marker(
            [volcan['latitude'], volcan['longitude']],
            popup=f"<h5>{volcan['properties']['place']}</h5><br><b>{volcan['properties']['mag']}</b>",
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(mapa)
        
    
# Guardar el mapa como un archivo HTML
mapa.save('mapa_volcanes.html')


# %%
