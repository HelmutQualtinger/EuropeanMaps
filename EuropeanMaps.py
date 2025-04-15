# The above code is creating choropleth maps to visualize life expectancy data in Europe by gender. It
# defines dictionaries containing life expectancy values for various European countries for both
# total, male, and female populations. The code then converts these dictionaries into DataFrames and
# uses Plotly Express to create choropleth maps for total life expectancy, male life expectancy, and
# female life expectancy separately.
import pandas as pd
from plotly.subplots import make_subplots
import webbrowser
import os

import plotly.express as px

# Load data (if needed, though not directly used for the provided dictionaries)
# df = px.data.gapminder()
# latest_year = df['year'].max()
# df_europe_latest = df[(df['continent'] == 'Europe') & (df['year'] == latest_year)]

from life_expectancy import *
# Convert dictionaries to DataFrames
life_expectancy_df = pd.DataFrame(list(life_expectancy.items()), columns=['country', 'lifeExp'])
male_life_expectancy_df = pd.DataFrame(list(male_life_expectancy_europe.items()), columns=['country', 'maleLifeExp'])
female_life_expectancy_df = pd.DataFrame(list(female_life_expectancy_europe.items()), columns=['country', 'femaleLifeExp'])

# Create choropleth maps
fig_total = px.choropleth(
    life_expectancy_df,
    locations="country",
    locationmode="country names",
    color="lifeExp",
    hover_name="country",
    hover_data={"lifeExp": True, "country": True},
    color_continuous_scale=px.colors.sequential.Viridis,
    title="Total Life Expectancy in Europe",
    template="plotly_white"
)
fig_total.update_layout(margin=dict(l=0, r=0, t=50, b=0))

fig_male = px.choropleth(
    male_life_expectancy_df,
    locations="country",
    locationmode="country names",
    color="maleLifeExp",
    hover_name="country",
    hover_data={"maleLifeExp": True, "country": True},
    color_continuous_scale=px.colors.sequential.Viridis,
    title="Male Life Expectancy in Europe"
)

fig_female = px.choropleth(
    female_life_expectancy_df,
    locations="country",
    locationmode="country names",
    color="femaleLifeExp",
    hover_name="country",
    hover_data={"femaleLifeExp": True, "country": True},
    color_continuous_scale=px.colors.sequential.Viridis,
    title="Female Life Expectancy in Europe"
)

# Update geos for all figures
for fig in [fig_total, fig_male, fig_female]:
    fig.update_geos(
        visible=False,  # Hide the default geos
        projection_type="natural earth",  # Use natural earth projection
        center=dict(lat=54, lon=15),  # Center the map on Europe
        projection_scale=4,  # Adjust scale for better visibility
        showlakes=True,
        lakecolor="darkblue",
        showocean=True,
        oceancolor="darkblue",
        showcountries=True,
        countrycolor="Black"
    )
    # Adjust layout
    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            coastlinecolor="Black",
            showland=True,
            landcolor="lightgray",
            showcountries=True,
            countrycolor="Black",
            showlakes=True,
        )
    )

# Combine figures into subplots
fig = make_subplots(
    rows=2, 
    cols=2, 
    subplot_titles=("Total Life Expectancy"," " , "Female Life Expectancy", "Male Life Expectancy"), 
    specs=[[{'type': 'choropleth'}, {'type': 'choropleth'}], [{'type': 'choropleth'}, {'type': 'choropleth'}]],
    vertical_spacing=0.05,  # Reduziert den vertikalen Abstand (Standard ist 0.3)
    horizontal_spacing=0.05,  # Reduziert den horizontalen Abstand (Standard ist 0.2)
)

fig.add_trace(fig_total.data[0], row=1, col=1)
fig.add_trace(fig_male.data[0], row=2, col=2)
fig.add_trace(fig_female.data[0], row=2, col=1)
# Update layout for the combined figure
fig.update_layout(margin=dict(l=0, r=0, t=20, b=0),  # Adjust margins as needed
    width=1400,
    height=1000,
    title_text="Life Expectancy in Europe ",
    title=dict(
            text="Life Expectancy in Europe by Gender",
            x=0.5,  # Center the title horizontally (0.5 is the center)
            font=dict(
                size=24  # Adjust the size as needed
            )
        ),
    title_xanchor="center",  # Center the title

    geo=dict(
        showframe=False,
        projection_scale=4,
        center=dict(lat=54, lon=15),
        showlakes=True,
        showocean=True,
        oceancolor="lightblue", lakecolor="darkblue",
        showcountries=True,  # Ensure countries are shown
        countrycolor="Black"   # Set the color for country borders
    ),
    geo2=dict(
        showframe=False,
        projection_scale=4,
        center=dict(lat=54, lon=15),
        showlakes=True,
        showocean=True,
        oceancolor="lightblue",
        lakecolor="darkblue",
        showcountries=True,  # Ensure countries are shown
        countrycolor="Black"   # Set the color for country borders
    ),
    geo3=dict(
        showframe=False,
        projection_scale=5,
        center=dict(lat=54, lon=15),
        showlakes=True,
        showocean=True,
        oceancolor="lightblue",
        lakecolor="darkblue",
        showcountries=True,  # Ensure countries are shown
        countrycolor="Black"   # Set the color for country borders
    ),
    geo4=dict(
        showframe=False,
        projection_scale=5,
        center=dict(lat=54, lon=15),
        showlakes=True,
        showocean=True,
        lakecolor="darkblue",
        oceancolor="lightblue",
        showcountries=True,  # Ensure countries are shown
        countrycolor="Black"   # Set the color for country borders
    ),
)
fig.update_layout(
    margin=dict(l=0, r=0, t=50, b=0),
    # Adjust vertical spacing between rows
    height=800,  # Adjust the height as needed
    )
file_path = os.path.abspath("european_life_expectancy.html")
fig.write_html(file_path)
webbrowser.open("file://" + file_path)
