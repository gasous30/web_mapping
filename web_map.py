import folium
import pandas as pd
import os

DATA_PATH = os.path.join('asset')

volcanoes = pd.read_csv(os.path.join(DATA_PATH, 'Volcanoes.txt'))

lat = list(volcanoes['LAT'])
lon = list(volcanoes['LON'])
elev = list(volcanoes['ELEV'])
name = list(volcanoes['NAME'])

center_coord = [volcanoes.iloc(0)[0][-2], volcanoes.iloc(0)[0][-1]]

map = folium.Map(location=center_coord, zoom_start=6, tiles='Stamen Terrain')

fg_volcano = folium.FeatureGroup(name='Show Volcanoes')

html = """
Volcano Name: %s
Height: %s m
"""

def color_marker(el):
    if (0 <= el <= 2000):
        return 'green'
    elif (2000 < el <= 3000):
        return 'orange'
    else:
        return 'red'

for lt, ln, nm, el in zip(lat, lon, name, elev):
    iframe = folium.IFrame(html=html % (nm, el), width=200, height=75)
    marker = folium.CircleMarker(location=[lt, ln], popup=folium.Popup(iframe), radius=6, fill=True, fill_color=color_marker(el), color='black', fill_opacity=0.6)
    fg_volcano.add_child(marker)

fg_pop = folium.FeatureGroup(name='Show Population 2005')

geojson = folium.GeoJson(data=open(os.path.join(DATA_PATH,'world.json'), 'r', encoding='utf-8-sig').read(), style_function=lambda x: {'fillColor': 'green' if x['properties']['POP2005'] < 10000000 else 'yellow' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red' })
fg_pop.add_child(geojson)

map.add_child(fg_pop)
map.add_child(fg_volcano)
map.add_child(folium.LayerControl())

map.save('volcanoes_map.html')