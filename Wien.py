import plotly.express as px
import pandas as pd
import json
import webbrowser
import os
from pyproj import Transformer
import geopandas as gpd
from shapely.geometry import shape
wiener_bezirke_gehaelter = {
    "Innere Stadt": 56600,
    "Hietzing": 41700,
    "Döbling": 41200,
    "Währing": 38500,
    "Wieden": 37800,
    "Neubau": 36900,
    "Josefstadt": 36700,
    "Mariahilf": 35600,
    "Alsergrund": 34800,
    "Penzing": 34200,
    "Landstraße": 33900,
    "Donaustadt": 33500,
    "Floridsdorf": 32800,
    "Hernals": 31900,
    "Meidling": 31600,
    "Ottakring": 31200,
    "Leopoldstadt": 30900,
    "Margareten": 30600,
    "Simmering": 30300,
    "Favoriten": 29800,
    "Brigittenau": 29500,
    "Rudolfsheim-Fünfhaus": 27900,
    "Liesing": 35000,
}



auslaenderanteil_wien = {
    "Innere Stadt": 32.1,
    "Leopoldstadt": 37.9,
    "Landstraße": 37.5,
    "Wieden": 36.2,
    "Margareten": 42.6,
    "Mariahilf": 34.6,
    "Neubau": 33.1,
    "Josefstadt": 33.4,
    "Alsergrund": 36.1,
    "Favoriten": 43.7,
    "Simmering": 36.5,
    "Meidling": 40.2,
    "Hietzing": 24.5,
    "Penzing": 30.3,
    "Rudolfsheim-Fünfhaus": 45.7,
    "Ottakring": 40.6,
    "Hernals": 37.3,
    "Währing": 30.7,
    "Döbling": 30.1,
    "Brigittenau": 44.0,
    "Floridsdorf": 31.3,
    "Donaustadt": 27.9,
    "Liesing": 26.0
}


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

# Create 'gehalt' column in DataFrame by mapping district names
df['Gehalt'] = df['NAMEK'].map(wiener_bezirke_gehaelter)
df['Ausländer'] = df['NAMEK'].map(auslaenderanteil_wien)
# Convert GeoJSON features to a GeoDataFrame to access geometric functions

# Convert the GeoJSON features to geometries
df['geometry'] = [shape(feature['geometry']) for feature in geojson_data['features']]
# Calculate centroids
df['centroid'] = df['geometry'].apply(lambda x: x.centroid)
df['Gehalt'] = (df['Gehalt'].astype(float)/14).astype(int)
print(df.head())
print (df.columns)

# Mapbox-Token (erforderlich für die Verwendung von choropleth_mapbox)
# Ersetze 'YOUR_MAPBOX_TOKEN' mit deinem eigenen Token.
# Ein Token kannst du kostenlos auf mapbox.com erstellen.

# Choropleth-Map erstellen
fig = px.choropleth_map(df,
                           geojson=geojson_data,
                           locations='NAMEK',  # Spalte mit den Bezirksnamen
                           featureidkey="properties.NAMEK",
                           color='Ausländer',
                           color_continuous_scale="Turbo",
                           map_style="satellite-streets", # Changed to OpenStreetMap style
                           zoom=10,
                           center={"lat": 48.21, "lon": 16.37},
                           opacity=0.5,
                           labels={'Ausländer': 'Ausländeranteil (%)', 'NAMEK': 'Bezirk'},
                           title='Ausländeranteil in den Wiener Bezirken',
                           hover_name='NAMEK',hover_data=['Gehalt','Ausländer'],
                          )

# Add text labels for each district
for idx, row in df.iterrows():
    print(row['geometry'].centroid.x, row['geometry'].centroid.y)
    fig.add_annotation(
        x=row['geometry'].centroid.x,
        y=row['geometry'].centroid.y,
        text="LABEL",
        showarrow=False,
        font=dict(size=8)
    )

fig.update_layout(
    margin={"r":0,"t":0,"l":0,"b":0},

)
# HTML-Datei speichern
file_path = os.path.abspath("wien_bezirke_choropleth.html")
fig.write_html(file_path)


# HTML-Datei im Browser öffnen
webbrowser.open("file://" + file_path)


print(f"Die Karte wurde in {file_path} gespeichert und im Browser geöffnet.")