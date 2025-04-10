import geopandas as gpd
import plotly.express as px
import json
import os
import webbrowser
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

life_expectancy_ch = {
    "ZH": 84.3,  # Zürich
    "BE": 83.1,  # Bern
    "LU": 84.1,  # Luzern
    "UR": 83.8,  # Uri
    "SZ": 84.2,  # Schwyz
    "OW": 84.0,  # Obwalden
    "NW": 84.1,  # Nidwalden
    "GL": 83.5,  # Glarus
    "ZG": 84.8,  # Zug
    "FR": 83.8,  # Freiburg
    "SO": 83.4,  # Solothurn
    "BS": 82.3,  # Basel-Stadt
    "BL": 84.0,  # Basel-Landschaft
    "SH": 83.6,  # Schaffhausen
    "AR": 83.7,  # Appenzell Ausserrhoden
    "AI": 83.9,  # Appenzell Innerrhoden
    "SG": 83.7,  # St. Gallen
    "GR": 83.4,  # Graubünden
    "AG": 83.8,  # Aargau
    "TG": 83.9,  # Thurgau
    "TI": 83.1,  # Tessin
    "VD": 83.2,  # Waadt
    "VS": 83.3,  # Wallis
    "NE": 82.7,  # Neuenburg
    "GE": 82.5,  # Genf
    "JU": 82.9   # Jura
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
    cantons_geo['life_expectancy'] = [life_expectancy_ch [canton] for canton in cantons_geo['id']]
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
fig = px.choropleth_map(
    cantons_geo,
    geojson=cantons_json,
    featureidkey="properties.id",  # Adjust this if your GeoJSON uses a different key for canton IDs
    locations='id',
    color='life_expectancy',
    color_continuous_scale='rainbow_r',  # Similar to 'hot' in matplotlib
    map_style="satellite-streets",  # Changed from "carto-positron" to show more geographical details
    zoom=7.5,
    center={"lat": 46.8, "lon": 8.2},  # Center of Switzerland
    opacity=0.4,  # Reduced opacity to better see geographical features underneath
    labels={'life_expectancy': 'Lebenserwartung'},  # Label for the color legend
    # Added 'name' if availabe in your GeoJSON

)
# Update the figure to make borders thick and blue
fig.update_traces(
    marker_line_color='blue',
    marker_line_width=2.5,
)

# Additional layout updates to ensure borders are visible
fig.update_geos(
    showcoastlines=True,
    coastlinecolor="Blue",
    showland=True,
    showcountries=True,
    countrycolor="Blue",
    countrywidth=2,
    showsubunits=True,
    subunitcolor="Blue",
    subunitwidth=2
)



# Add annotations with canton IDs and life expectancy values
print("Adding canton annotations to map...")

# Calculate centroids for each canton's geometry
cantons_geo['centroid'] = cantons_geo.geometry.centroid
cantons_geo['lon'] = cantons_geo.centroid.x
cantons_geo['lat'] = cantons_geo.centroid.y

# Add text annotations for each canton
annotations = []
for idx, row in cantons_geo.iterrows():
    print (row['lon'], row['lat'])
    print(f"{row['id']}: {row['life_expectancy']:.1f}" )
    annotations.append(dict(
        x=row['lon'],
        y=row['lat'],
        text=f"{row['id']}: {row['life_expectancy']:.1f}",
        showarrow=False,
        font=dict(
            family="Arial, sans-serif",
            size=10,
            color="black"
        ),
        bgcolor="white",
        bordercolor="black",
        borderwidth=5,
        borderpad=4,
        opacity=0.8
    ))

# Add annotations to the map
fig.update_layout(annotations=annotations)


# Save the map as an HTML file
html_file = "switzerland_income_map.html"
print(f"Saving map to {html_file}...")
fig.write_html(html_file)
# Open the HTML file in the default web browser
print(f"Opening {html_file} in web browser...")
file_url = f"file://{os.path.abspath(html_file)}"
webbrowser.open_new_tab(file_url)
