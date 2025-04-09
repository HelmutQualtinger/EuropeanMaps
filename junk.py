# 1. Import Libraries
import plotly.graph_objects as go
import pandas as pd
import requests

# 2. Prepare Data
# Dictionary of US States and DC with their abbreviations
states_data = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California',
    'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'DC': 'District of Columbia',
    'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois',
    'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana',
    'ME': 'Maine', 'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan',
    'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana',
    'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey',
    'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota',
    'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania',
    'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee',
    'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington',
    'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'
}

# Create lists for DataFrame
state_codes = list(states_data.keys())
state_names = list(states_data.values())

# Generate dummy data for coloring (e.g., sequential numbers)
# Using a simple range from 1 to number of states + DC
dummy_values = list(range(1, len(state_codes) + 1))

# Create Pandas DataFrame
df = pd.DataFrame({
    'state_code': state_codes,
    'state_name': state_names,
    'value': dummy_values  # Replace with your actual data if available
})

# Lade ein gültiges GeoJSON-Objekt für US-Bundesstaaten
geojson_url = "https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json"
us_states_geo = requests.get(geojson_url).json()

# 3. Create Figure
fig = go.Figure()

# 4. Add Choropleth Trace (for state coloring)
fig.add_trace(go.Choropleth(
    locations=df['state_code'],      # State abbreviations for location identification
    z=df['value'],                   # Data to be color-coded
    locationmode='USA-states',       # Set to know these are US states
    colorscale='Plasma',            # Choose a colorscale (e.g., 'Viridis', 'Blues', 'Reds')
    colorbar_title="Dummy Value",    # Title for the color bar
    geojson=us_states_geo,         # Provide the GeoJSON data for Mapbox
    featureidkey="properties.name",  # Match GeoJSON property for state identification,  # Use OpenStreetMap as base map
    marker_opacity=0.8,              # Adjust marker opacity
    marker_line_width=0 ,             # Remove borders around states
    marker=dict(opacity=0.8),      # Adjust marker opacity for better visualization
    hoverinfo='location+z+text',     # Show state code, value, and full name on hover
    text=df['state_name']            # Text displayed on hover (full state names)
))

# 5. Add Scattergeo Trace (for displaying text labels on states)
# Note: Plotly places text at calculated centroids. Placement might not be perfect for all states (e.g., Michigan, Florida).
# Using abbreviations ('state_code') as text because full names ('state_name') are usually too long.
fig.add_trace(go.Scattergeo(
    locations=df['state_code'],
    locationmode='USA-states',
    text=df['state_name'],          # Display full state names on the map
    mode='text',
    textfont=dict(                  # Optional: Customize text appearance
        size=14,
        color='black'               # Choose a color that contrasts with the colorscale
    ),
    showlegend=False,               # Hide this trace from the legend
    hoverinfo='none'                # Don't show hover info for the text itself
))


# 6. Update Layout
fig.update_layout(
    title_text='US States Choropleth Map with State Abbreviations', # Map title
    geo_scope='usa', # Limit map scope to USA
    # Optional: Adjust map projection or center
    # geo=dict(
    #     scope='usa',
    #     projection=go.layout.geo.Projection(type='albers usa'),
    #     lakecolor='rgb(255, 255, 255)' # color of lakes
    # ),
)

# 7. Show Figure
fig.show()

print("Plotly map generated. Check the output window or browser.")