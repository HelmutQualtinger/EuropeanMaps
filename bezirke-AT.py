import geopandas as gpd
import plotly.express as px
from   bezirk import *
import webbrowser
import os
import uuid

# Load the GeoJSON file containing Austria's districts
file_path = "österreich-bezirke.json"
districts = gpd.read_file(file_path)

# Add area, population, and population density to the GeoDataFrame
districts['area']       = districts['name'].map(lambda x: politische_bezirke_dict[x]['fläche'])
districts['population'] = districts['name'].map(lambda x: politische_bezirke_dict[x]["bevölkerung"])
districts['population_density'] = districts.apply(
    lambda row: round(row['population'] / row['area'], 1) if row['area'] else None, axis=1
)

fig = px.choropleth_map(
    districts,
    geojson=districts.geometry,
    locations=districts.index,
    color='population_density',  # You can specify a column for coloring
    hover_name="name", # Use the correct column name for hover data
    title=r"Bevölkerungsdiche Österreich mit Bezirken Einw/km^2",
    map_style="satellite-streets",
    center={"lat": 47.5162, "lon": 14.5501},
    hover_data={
        'name': True,  # Show district name on hover
        'population': True,  # Show population on hover
        'area': True,  # Show area on hover
        'population_density': True,  # Show population density on hover
    },
    opacity=0.4,
    zoom=6
)
fig.update_coloraxes( colorscale="rainbow", colorbar_title="Einw/km^2", colorbar=dict(tickmode="array", 
                        tickvals=[10, 50, 100, 400], ticktext=["10", "50", "100", "400"]), cmin=1, cmax=400, )
fig.update_traces(marker_line_color="gold", marker_line_width=4)

fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
# Save the figure as an HTML file using a relative path
html_file_path = f"/tmp/austria_districts_map_{uuid.uuid4().hex}.html"
fig.write_html(html_file_path)

# Open the HTML file in Microsoft Edge
webbrowser.get().open(f"file://{html_file_path}")
