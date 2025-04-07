import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go
import json
import os

# Dictionary of mean income by canton (two-letter abbreviation)
# Values are in CHF (Swiss Francs)
mean_income = {
    'ZH': 60900,  # Zurich
    'BE': 52800,  # Bern
    'LU': 55200,  # Lucerne
    'UR': 53500,  # Uri
    'SZ': 63600,  # Schwyz
    'OW': 59800,  # Obwalden
    'NW': 61200,  # Nidwalden
    'GL': 53100,  # Glarus
    'ZG': 71500,  # Zug (Often highest)
    'FR': 50800,  # Fribourg
    'SO': 54100,  # Solothurn
    'BS': 53700,  # Basel-Stadt
    'BL': 58300,  # Basel-Landschaft
    'SH': 56500,  # Schaffhausen
    'AR': 54900,  # Appenzell Ausserrhoden
    'AI': 55100,  # Appenzell Innerrhoden
    'SG': 53400,  # St. Gallen
    'GR': 52100,  # Graubünden / Grisons
    'AG': 58500,  # Aargau
    'TG': 55800,  # Thurgau
    'TI': 44700,  # Ticino (Often lowest)
    'VD': 51900,  # Vaud
    'VS': 48200,  # Valais / Wallis
    'NE': 46500,  # Neuchâtel
    'GE': 52500,  # Geneva
    'JU': 49100   # Jura
}


# --- 1. Configuration ---

# Path or URL to the GeoJSON file with Swiss canton boundaries
# Using a common online source. Download your own if this URL breaks or for reliability.
# Check the properties of your file to find a canton identifier if needed later (e.g., 'id', 'name')
geojson_path_or_url = "cantons.geojson"
# Example if using a local file:
# geojson_path_or_url = "path/to/your/swiss_cantons.geojson"

# --- 2. Load Geospatial Data ---
print(f"Loading canton shapes from: {geojson_path_or_url}")
try:
    cantons_geo = gpd.read_file(geojson_path_or_url)
    print("GeoDataFrame loaded successfully.")
    # Optional: Print columns to see available properties like 'id', 'name'
    print("Available columns:", cantons_geo.columns)
    # Add income data to the GeoDataFrame
    cantons_geo['income_per_capita'] = [mean_income[canton] for canton in cantons_geo['id']]
    print("Available columns:", cantons_geo.columns)
    print(cantons_geo.head())

except Exception as e:
    print(f"Error loading GeoJSON: {e}")
    print("Please ensure the path/URL is correct or download a local file.")
    exit()

# --- 3. Create the Map with Plotly ---
print("Generating map...")

# Convert GeoDataFrame to GeoJSON for Plotly
cantons_json = json.loads(cantons_geo.to_json())

# Create choropleth map
fig = px.choropleth_mapbox(
    cantons_geo,
    geojson=cantons_json,
    locations=cantons_geo.index,
    color='income_per_capita',
    color_continuous_scale='rainbow_r',  # Similar to 'hot' in matplotlib
    mapbox_style="carto-positron",  # Changed from "carto-positron" to show more geographical details
    zoom=5.5,
    center={"lat": 46.8, "lon": 8.2},  # Center of Switzerland
    opacity=0.6,  # Reduced opacity to better see geographical features underneath
    labels={'income_per_capita': 'Per Capita Income (CHF)'},
    # Added 'name' if available in your GeoJSON
)


# Customize layout
fig.update_layout(
    title='Cantons of Switzerland',
    title_font_size=10,
    font=dict(
        family="Arial",
        size=16,
        color="Black"
    ),
    margin={"r": 0, "t": 30, "l": 0, "b": 0},  # Increased top margin for title
    height=800,
    width=1200,
    mapbox=dict(
        style="open-street-map",  # Ensuring consistent style setting
        layers=[
            {
                "below": 'traces',
                "sourcetype": "raster",
                "sourceattribution": "© OpenStreetMap contributors",
                "source": [
                    "https://tile.openstreetmap.org/{z}/{x}/{y}.png"
                ]
            }
        ]
    )
)

# Add canton labels
for idx, row in cantons_geo.iterrows():
    centroid = row.geometry.centroid
    fig.add_trace(go.Scattermapbox(
        lat=[centroid.y],
        lon=[centroid.x],
        mode='text',
        text=[f"{row['name']}<br>{row['income_per_capita']}"],
        textfont=dict(color='black', size=15),
        showlegend=False
    ))

# Save the map as an HTML file
html_file = "switzerland_income_map.html"
print(f"Saving map to {html_file}...")
fig.write_html(html_file)
import webbrowser
# Open the HTML file in the default web browser
print(f"Opening {html_file} in web browser...")
file_url = f"file://{os.path.abspath(html_file)}"



# Open the HTML file in the default web browser
print(f"Opening {html_file} in web browser...")
file_url = f"file://{os.path.abspath(html_file)}"
webbrowser.open_new_tab(file_url)
