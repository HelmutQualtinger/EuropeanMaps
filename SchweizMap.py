import geopandas as gpd
import plotly.express as px
import json
import os
import webbrowser
from SwissData import *
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
    cantons_geo['mean_income'] = [mean_income[canton] for canton in cantons_geo['id']]
    cantons_geo['mean_wealth'] = [mean_wealth[canton] for canton in cantons_geo['id']]
    print("Available columns:", cantons_geo.columns)
    print(cantons_geo.head())

except Exception as e:
    print(f"Error loading GeoJSON: {e}")
    print("Please ensure the path/URL is correct or download a local file.")
    exit()
    


# --- 3. Create the Map with Plotly ---
print("Generating map...")

# Create choropleth map
# Create choropleth map
fig = px.choropleth_map(
    cantons_geo,
    geojson=cantons_geo,
    featureidkey="properties.name",  # Adjust this if your GeoJSON uses a different key for canton IDs
    locations='name',  # This should match the 'id' or 'name' in your GeoJSON
    color='mean_wealth',  # Change to 'mean_income' if you want to visualize income instead
    color_continuous_scale='Rainbow',  # Similar to 'hot' in matplotlib
    map_style="open-street-map",  # <<< CHANGED to OpenStreetMap style
    zoom=7.5,
    center={"lat": 46.8, "lon": 8.2},  # Center of Switzerland
    opacity=0.3,
    range_color=(150000, 250000),
    labels={
        'life_expectancy': 'Lebenserwartung',
        'mean_income': 'Ø Einkommen (CHF)',
        'mean_wealth': 'Ø Vermögen (CHF)',
        'name': 'Kanton'  # Label for canton name
    },
    hover_data={
        'name': True,  # Show the full canton name
        'life_expectancy': ':.1f',  # Format life expectancy to 1 decimal place
        'mean_income': ':,d',  # Format mean income as an integer
        'mean_wealth': ':,d'  # Format mean wealth as an integer

    }
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
    countrycolor="White",
    countrywidth=4,
    showsubunits=True,
    subunitcolor="Red",
    subunitwidth=2
)


# Save the map as an HTML file
html_file = "switzerland_income_map.html"
print(f"Saving map to {html_file}...")
fig.write_html(html_file)
# Open the HTML file in the default web browser
print(f"Opening {html_file} in web browser...")
file_url = f"file://{os.path.abspath(html_file)}"
webbrowser.open_new_tab(file_url)
