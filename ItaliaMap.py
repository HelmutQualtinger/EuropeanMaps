import geopandas as gpd
import plotly.express as px
import webbrowser
import os
import pandas as pd

average_provincial_income_2022 = {
    "Agrigento": 16940,
    "Alessandria": 23460,
    "Ancona": 24340,
    "Aosta": 24280,  # Valle d'Aosta is often treated as a single province unit in these stats
    "Arezzo": 23180,
    "Ascoli Piceno": 20960,
    "Asti": 23510,
    "Avellino": 19410,
    "Bari": 22080,
    "Barletta-Andria-Trani": 17790,
    "Belluno": 23500,
    "Benevento": 18770,
    "Bergamo": 26880,
    "Biella": 23180,
    "Bologna": 28110,
    "Bolzano/Bozen": 25690,
    "Brescia": 25890,
    "Brindisi": 18410,
    "Cagliari": 23580,
    "Caltanissetta": 17950,
    "Campobasso": 21030,
    "Caserta": 18430,
    "Catania": 20470,
    "Catanzaro": 20450,
    "Chieti": 21680,
    "Como": 27310,
    "Cosenza": 18520,
    "Cremona": 25490,
    "Crotone": 17780,
    "Cuneo": 24050,
    "Enna": 17180,
    "Fermo": 20790,
    "Ferrara": 24280,
    "Firenze": 26300,
    "Foggia": 17800,
    "Forlì-Cesena": 24520,
    "Frosinone": 19470,
    "Genova": 25960,
    "Gorizia": 23280,
    "Grosseto": 22110,
    "Imperia": 21910,
    "Isernia": 19630,
    "L'Aquila": 22040,
    "La Spezia": 23720,
    "Latina": 21190,
    "Lecce": 18880,
    "Lecco": 27710,
    "Livorno": 23500,
    "Lodi": 26970,
    "Lucca": 23890,
    "Macerata": 22190,
    "Mantova": 24930,
    "Massa-Carrara": 21510,
    "Matera": 19280,
    "Messina": 19840,
    "Milano": 35220,
    "Modena": 27400,
    "Monza e della Brianza": 27980,
    "Napoli": 22110,
    "Novara": 25100,
    "Nuoro": 19060,
    "Oristano": 19160,
    "Padova": 26440,
    "Palermo": 21050,
    "Parma": 28050,
    "Pavia": 26380,
    "Perugia": 22640,
    "Pesaro e Urbino": 22660,
    "Pescara": 23400,
    "Piacenza": 26770,
    "Pisa": 24680,
    "Pistoia": 22430,
    "Pordenone": 25140,
    "Potenza": 19120,
    "Prato": 23020,
    "Ragusa": 18340,
    "Ravenna": 25690,
    "Reggio Calabria": 18620, # Often referred to as Reggio di Calabria
    "Reggio Emilia": 27240, # Often referred to as Reggio nell'Emilia
    "Rieti": 20540,
    "Rimini": 23250,
    "Roma": 27960,
    "Rovigo": 22920,
    "Salerno": 20190,
    "Sassari": 21160, # Includes former Olbia-Tempio province area for these stats
    "Savona": 23480,
    "Siena": 24280,
    "Siracusa": 18860,
    "Sondrio": 24120,
    "Sud Sardegna": 18810, # New province, data aggregated from parts of former provinces
    "Taranto": 19080,
    "Teramo": 21630,
    "Terni": 20510,
    "Torino": 26400,
    "Trapani": 18340,
    "Trento": 24460,
    "Treviso": 25280,
    "Trieste": 25160,
    "Udine": 24500,
    "Varese": 27560,
    "Venezia": 25390,
    "Verbano-Cusio-Ossola": 23380,
    "Vercelli": 22870,
    "Verona": 25600,
    "Vibo Valentia": 17110,
    "Vicenza": 25960,
    "Viterbo": 20340,
}

# Optional: Print the dictionary to verify
# import json
# print(json.dumps(average_provincial_income_2022, indent=2, ensure_ascii=False))

# --- 1. Configuration ---
geojson_path = "limits_IT_provinces.geojson"
data_column = "population"  # Example: Use population data
location_column = "prov_name"  # Example: Use province name as location ID
title = "Population in Italian Provinces"

# --- 2. Load Data ---
try:
    # Load GeoJSON data into a GeoDataFrame
    gdf = gpd.read_file(geojson_path)
    # Drop the geometry column

    # Add the average_provincial_income_2022 column
    gdf['average_income'] = gdf['prov_name'].map(average_provincial_income_2022)
    
    # Check if any values are NaN
    if gdf['average_income'].isnull().any():
        print("Warning: Some provinces do not have income data.")
    
    print(gdf.head())
    
    # Format 'average_income' column with thousands separator
    gdf['average_income_formatted'] = gdf['average_income'].apply(lambda x: f"{x:,.0f}")


    df= pd.DataFrame(gdf)
    
except Exception as e:
    print(f"Error loading GeoJSON file: {e}")
    exit()
    
# --- 3. Create the Map with Plotly ---

fig = px.choropleth_map(
    df,
    geojson=gdf,
    locations='prov_name',  # Use the correct column name for locations
    featureidkey="properties.prov_name",
    color='average_income',
    color_continuous_scale="Rainbow_r",
    range_color=[16000, 30000],

    hover_name='prov_name',
    hover_data={'average_income_formatted': True, 'average_income': False},
    map_style="satellite-streets",
    
    opacity=0.5,
    labels={'average_income_formatted': 'Reddito medio (€)','average_income': 'Redditto medio (€)', 'prov_name': 'Provincia'},
    center={"lat": 41.9, "lon": 12.5},
    zoom=5,
    
    title="Average Income in Italian Provinces (2022)"
)
fig.update_layout(margin={"r": 0, "t": 10, "l": 0, "b": 0})
fig.update_traces(marker_line_color="darkgoldenrod", marker_line_width=2)
# Save the map as an HTML file
html_file = "italy_income_map.html"
print(f"Saving map to {html_file}...")
fig.write_html(html_file)
# Open the HTML file in the default web browser
print(f"Opening {html_file} in web browser...")
file_url = f"file://{os.path.abspath(html_file)}"
webbrowser.open_new_tab(file_url)
