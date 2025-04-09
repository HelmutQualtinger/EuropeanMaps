import plotly.express as px
import pandas as pd
import webbrowser
# No need to import 'json' if Plotly handles the file loading

# --- 1. Sample Data ---
# IMPORTANT: The 'locations' column must match the identifier in the GeoJSON.
# This GeoJSON uses state names (e.g., "Alabama") found in properties.name.

data = {
    'state': [
        'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado',
        'Connecticut', 'Delaware', 'District of Columbia', 'Florida', 'Georgia',
        'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky',
        'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan',
        'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
        'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina',
        'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania',
        'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas',
        'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin',
        'Wyoming'
    ],
    'unemployment': [
        3.0, 4.5, 3.6, 3.5, 5.3, 3.7,  # AL, AK, AZ, AR, CA, CO
        4.4, 4.1, 5.2, 3.3, 3.1,  # CT, DE, DC, FL, GA
        2.8, 3.3, 4.8, 3.6, 2.9, 2.8, 4.1,  # HI, ID, IL, IN, IA, KS, KY
        4.3, 3.3, 2.6, 2.9, 3.9,  # LA, ME, MD, MA, MI
        2.7, 3.8, 3.4, 3.0, 2.5, 5.2,  # MN, MS, MO, MT, NE, NV
        2.7, 4.7, 3.7, 4.2, 3.5,  # NH, NJ, NM, NY, NC
        2.0, 4.0, 3.4, 4.2, 3.4,  # ND, OH, OK, OR, PA
        3.4, 3.0, 2.0, 3.1, 4.0,  # RI, SC, SD, TN, TX
        2.8, 2.2, 3.0, 4.8, 4.2, 2.9,  # UT, VT, VA, WA, WV, WI
        2.8  # WY
    ]
}

# Daten basierend auf U.S. Census Bureau, American Community Survey (ACS)
# Stand: 2022 (1-Year Estimates), inflationsbereinigte Dollar
# Metrik: Median Household Income
# Beinhaltet den District of Columbia

median_income_data_us_states = {
    'state': [
        'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado',
        'Connecticut', 'Delaware', 'District of Columbia', 'Florida', 'Georgia',
        'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky',
        'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan',
        'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
        'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina',
        'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania',
        'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas',
        'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin',
        'Wyoming'
    ],
    'median_household_income': [
        59609, 86370, 72581, 56335, 91905, 87598,  # AL, AK, AZ, AR, CA, CO
        90213, 81856, 101722, 67917, 71355,  # CT, DE, DC, FL, GA
        92616, 76913, 78433, 70145, 72483, 71129, 61091,  # HI, ID, IL, IN, IA, KS, KY
        57200, 71798, 94488, 96555, 70849,  # LA, ME, MD, MA, MI
        84313, 52985, 68071, 68301, 72431, 72423,  # MN, MS, MO, MT, NE, NV
        90845, 99643, 58486, 78967, 71570,  # NH, NJ, NM, NY, NC
        73959, 69720, 66450, 80625, 74963,  # ND, OH, OK, OR, PA
        81369, 66574, 70612, 67243, 73035,  # RI, SC, SD, TN, TX
        89168, 74014, 87249, 90325, 55217, 72458,  # UT, VT, VA, WA, WV, WI
        69017  # WY
    ]
}

data = {
    'state': [
        'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado',
        'Connecticut', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois',
        'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine',
        'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi',
        'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey',
        'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio',
        'Oklahoma', 'Oregon', 'Pennsylvania', 'South Carolina', 'South Dakota',
        'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
        'West Virginia', 'Wisconsin', 'Wyoming'
    ],
    'wealth': [
        45000, 160000, 105000, 35000, 230000, 170000,  # AL, AK, AZ, AR, CA, CO
        200000, 130000, 115000, 250000, 38000, 155000,  # CT, FL, GA, HI, ID, IL
        90000, 75000, 65000, 50000, 40000, 27000,       # IN, IA, KS, KY, LA, ME
        195000, 220000, 100000, 165000, 18000, 85000,   # MD, MA, MI, MN, MS, MO
        33000, 70000, 135000, 175000, 210000, 20000,    # MT, NE, NV, NH, NJ, NM
        190000, 110000, 30000, 95000, 55000, 150000,    # NY, NC, ND, OH, OK, OR
        125000, 60000, 32000, 80000, 145000, 140000,    # PA, SC, SD, TN, TX, UT
        25000, 180000, 185000, 23000, 120000, 28000     # VT, VA, WA, WV, WI, WY
    ]
}
# Quelle: U.S. Census Bureau, 2022 American Community Survey 1-Year Estimates, Table B19013

# Beispiel zur Überprüfung (optional)
# print(len(median_income_data_us_states['state']))
# print(len(median_income_data_us_states['median_household_income']))
# print(median_income_data_us_states)

df = pd.DataFrame(data)

# --- 2. GeoJSON Source ---
# To use a local downloaded GeoJSON file, load it as a Python dictionary.
import json
with open("/Users/haraldbeker/EuropeanMaps/us-states.geojson", "r") as f:
    geojson_data = json.load(f)

# --- Optional: Set Mapbox Token (needed for certain map styles like 'satellite', 'streets') ---
# Get a free token from account.mapbox.com
# px.set_mapbox_access_token("YOUR_MAPBOX_ACCESS_TOKEN")

# --- 3. Create the Choropleth Mapbox plot ---
fig = px.choropleth_map(
    data_frame=df,                     # Your data
    geojson=geojson_data,               # URL or path to the GeoJSON file
    locations='state',                 # Column in data_frame with IDs matching GeoJSON features
    featureidkey="properties.name",    # Specifies how to find the ID within each GeoJSON feature
                                       # For this file, the state name is under the 'properties' object with the key 'name'
    color='wealth',              # Column determining the color
    color_continuous_scale="Hot",  # Color scale for continuous data
    # range_color=(3.0, 8.0),          # Optional: Set the range of the color scale
    map_style="satellite-streets",     # Basemap style (this one doesn't require a token)
    zoom=3,                            # Initial map zoom level
    center={"lat": 37.0902, "lon": -95.7129}, # Initial map center (approx. center of USA)
    opacity=0.3,                       # Opacity of the colored regions (0=transparent, 1=opaque)
    hover_name='state',                # Display state name prominently on hover
    hover_data={'wealth': ':.4f%'}, # Show unemployment formatted to 1 decimal place, add '%'
    labels={'wealth': 'wealth'}, # Label for the color legend and hover
    title="US States median wealth (Mapbox Example)"
)
fig.update_layout(
    title='Unemployment Rate by State',
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

# --- 5. Show the Plot ---
fig.write_html("/Users/haraldbeker/EuropeanMaps/USA.html")
webbrowser.open("file:///Users/haraldbeker/EuropeanMaps/USA.html")