from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

import pandas as pd
df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
                   dtype={"fips": str})

import plotly.express as px

fig = px.choropleth_map(df, geojson=counties, locations='fips', color='unemp',
                           color_continuous_scale="Rainbow",
                           range_color=(0, 12),
                           map_style='satellite-streets',
                           opacity=0.3,
                           labels={'unemp':'unemployment rate'},
                           center={"lat": 37.0902, "lon": -95.7129} # Initial map center (approx. center of USA)
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()