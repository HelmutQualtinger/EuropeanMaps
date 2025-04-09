import plotly.express as px
import pandas as pd
import json
import webbrowser
import os
from pyproj import Transformer

def transform_coordinates(geojson_data, source_crs=31256, target_crs=4326):
    # Create transformer from source CRS to target CRS
    transformer = Transformer.from_crs(source_crs, target_crs, always_xy=True)

    # Transform all coordinates in the GeoJSON
    for feature in geojson_data['features']:
        geometry = feature['geometry']
        if geometry['type'] == 'Polygon':
            for ring in geometry['coordinates']:
                for i, coord in enumerate(ring):
                    x, y = coord
                    lon, lat = transformer.transform(x, y)
                    ring[i] = [lon, lat]
        elif geometry['type'] == 'MultiPolygon':
            for polygon in geometry['coordinates']:
                for ring in polygon:
                    for i, coord in enumerate(ring):
                        x, y = coord
                        lon, lat = transformer.transform(x, y)
                        ring[i] = [lon, lat]
    return geojson_data

# Load GeoJSON data from file
with open('WienBezirke.json', 'r') as f:
    geojson_data = json.load(f)


    # Transform coordinates
    geojson_data = transform_coordinates(geojson_data)

    # DataFrame aus den Daten erstellen
df = pd.DataFrame([feature['properties'] for feature in geojson_data['features']])
print(df.head())

# Mapbox-Token (erforderlich für die Verwendung von choropleth_mapbox)
# Ersetze 'YOUR_MAPBOX_TOKEN' mit deinem eigenen Token.
# Ein Token kannst du kostenlos auf mapbox.com erstellen.

# Choropleth-Map erstellen
fig = px.choropleth_mapbox(df,
                           geojson=geojson_data,
                           locations='NAMEK',  # Spalte mit den Bezirksnamen
                           featureidkey="properties.NAMEK",
                           color='FLAECHE',
                           color_continuous_scale="Viridis",
                           mapbox_style="open-street-map", # Changed to OpenStreetMap style
                           zoom=10,
                           center={"lat": 48.21, "lon": 16.37},
                           opacity=0.5,
                           labels={'FLAECHE': 'Flaeche'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


# HTML-Datei speichern
file_path = os.path.abspath("wien_bezirke_choropleth.html")
fig.write_html(file_path)


# HTML-Datei im Browser öffnen
webbrowser.open("file://" + file_path)


print(f"Die Karte wurde in {file_path} gespeichert und im Browser geöffnet.")