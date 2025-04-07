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

european_life_expectancy = {
    "Monaco": 87.0,          # Often highest, data varies (Source: UN/Wikipedia ~2023)
    "Switzerland": 84.0,     # (Source: World Bank ~2021/2022)
    "Spain": 83.9,           # (Source: World Bank ~2021/2022)
    "Italy": 83.8,           # (Source: World Bank ~2021/2022)
    "Liechtenstein": 83.7,   # (Source: Wikipedia/UN ~2021) - Data can be sparse
    "Norway": 83.6,          # (Source: World Bank ~2021/2022)
    "Iceland": 83.5,         # (Source: World Bank ~2021/2022)
    "Sweden": 83.4,          # (Source: World Bank ~2021/2022)
    "France": 83.1,          # (Source: World Bank ~2021/2022) - Includes overseas departments
    "Malta": 83.0,           # (Source: World Bank ~2021/2022)
    "Luxembourg": 82.8,      # (Source: World Bank ~2021/2022)
    "Ireland": 82.8,         # (Source: World Bank ~2021/2022)
    "Finland": 82.6,         # (Source: World Bank ~2021/2022)
    "Netherlands": 82.5,     # (Source: World Bank ~2021/2022)
    "Portugal": 82.3,        # (Source: World Bank ~2021/2022)
    "Austria": 82.1,         # (Source: World Bank ~2021/2022)
    "Belgium": 82.0,         # (Source: World Bank ~2021/2022)
    "United Kingdom": 81.8,  # (Source: World Bank ~2021/2022)
    "Slovenia": 81.6,        # (Source: World Bank ~2021/2022)
    "Germany": 81.6,         # (Source: World Bank ~2021/2022)
    "Greece": 81.5,          # (Source: World Bank ~2021/2022)
    "Denmark": 81.4,         # (Source: World Bank ~2021/2022)
    "Cyprus": 81.3,          # (Source: World Bank ~2021/2022)
    "San Marino": 81.1,      # (Source: Wikipedia/WHO ~2019/2020) - Data can be sparse
    "Czech Republic": 79.7,  # (Source: World Bank ~2021/2022)
    "Estonia": 79.3,         # (Source: World Bank ~2021/2022)
    "Croatia": 79.0,         # (Source: World Bank ~2021/2022)
    "Poland": 78.6,          # (Source: World Bank ~2021/2022)
    "Slovakia": 77.8,        # (Source: World Bank ~2021/2022)
    "Turkey": 77.7,          # (Source: World Bank ~2021/2022) - Transcontinental
    "Albania": 77.6,         # (Source: World Bank ~2021/2022)
    "Montenegro": 77.1,      # (Source: World Bank ~2021/2022)
    "Hungary": 76.9,         # (Source: World Bank ~2021/2022)
    "Lithuania": 76.5,       # (Source: World Bank ~2021/2022)
    "Latvia": 75.9,          # (Source: World Bank ~2021/2022)
    "Romania": 75.6,         # (Source: World Bank ~2021/2022)
    "Serbia": 75.5,          # (Source: World Bank ~2021/2022)
    "Bulgaria": 75.1,        # (Source: World Bank ~2021/2022)
    "Belarus": 74.8,         # (Source: World Bank ~2021/2022)
    "Bosnia and Herzegovina": 74.6, # (Source: World Bank ~2021/2022)
    "North Macedonia": 74.5, # (Source: World Bank ~2021/2022)
    "Russia": 72.7,          # (Source: World Bank ~2021/2022) - Transcontinental
    "Moldova": 71.9,         # (Source: World Bank ~2021/2022)
    "Ukraine": 71.6,         # (Source: World Bank ~2021/2022) - Pre-invasion figures likely affected now
    # -- Countries often included, data may vary or be less available --
    "Andorra": 81.8,       # (Example, check recent sources like WHO/Wikipedia)
    # "Vatican City": N/A    # Usually not listed due to unique demographics
    "Kosovo": 79.1,        # (Example, check recent sources - UN/World Bank might list separately)
}

male_life_expectancy_europe = {
    "Albania": 75.0,
    "Andorra": None, # Data often unavailable in standard datasets
    "Armenia": 70.0, # Geographically complex, often included
    "Austria": 78.8,
    "Azerbaijan": 68.3, # Geographically complex, often included
    "Belarus": 69.3, # Data might be less reliable or older depending on source
    "Belgium": 79.1,
    "Bosnia and Herzegovina": 73.4,
    "Bulgaria": 70.0,
    "Croatia": 74.7,
    "Cyprus": 78.8, # Geographically complex, often included
    "Czech Republic": 75.2, # Also known as Czechia
    "Denmark": 79.3,
    "Estonia": 73.9,
    "Finland": 78.9,
    "France": 79.1, # Note: May include overseas departments
    "Georgia": 70.1, # Geographically complex, often included
    "Germany": 78.3,
    "Greece": 77.5,
    "Hungary": 72.8,
    "Iceland": 81.5,
    "Ireland": 80.4,
    "Italy": 80.5,
    "Kazakhstan": 68.5, # Transcontinental, often included in broader Europe region stats
    "Kosovo": None, # Data availability varies significantly due to recognition status
    "Latvia": 70.9,
    "Liechtenstein": None, # Data often unavailable in standard datasets
    "Lithuania": 71.5,
    "Luxembourg": 80.4,
    "Malta": 80.7,
    "Moldova": 67.6,
    "Monaco": None, # Data often unavailable in standard datasets
    "Montenegro": 73.8,
    "Netherlands": 80.0,
    "North Macedonia": 71.3,
    "Norway": 81.3,
    "Poland": 73.4,
    "Portugal": 77.9,
    "Romania": 71.6,
    "Russia": 64.2, # Transcontinental
    "San Marino": None, # Data often unavailable in standard datasets
    "Serbia": 72.8,
    "Slovakia": 73.5, # Also known as Slovak Republic
    "Slovenia": 77.8,
    "Spain": 79.6,
    "Sweden": 81.1,
    "Switzerland": 81.6,
    "Turkey": 74.6, # Transcontinental
    "Ukraine": 67.6, # Note: Pre-2022 full-scale invasion data
    "United Kingdom": 78.7,
    "Vatican City": None # No data typically available
}

female_life_expectancy_europe = {
    "Albania": 80.5,
    "Andorra": 86.3,  # Often estimated, can vary significantly by source
    "Armenia": 79.3, # Often included culturally/politically with Europe
    "Austria": 84.0,
    "Azerbaijan": 75.5, # Often included culturally/politically with Europe
    "Belarus": 78.5,
    "Belgium": 84.1,
    "Bosnia and Herzegovina": 78.8,
    "Bulgaria": 78.9,
    "Croatia": 81.5,
    "Cyprus": 84.5, # Geographically Asia, culturally/politically Europe
    "Czech Republic": 81.9,
    "Denmark": 83.2,
    "Estonia": 82.8,
    "Finland": 84.5,
    "France": 85.5,
    "Georgia": 80.4, # Often included culturally/politically with Europe
    "Germany": 83.6,
    "Greece": 83.5,
    "Hungary": 79.8,
    "Iceland": 84.4,
    "Ireland": 84.3,
    "Italy": 84.9,
    "Kazakhstan": 74.9, # Transcontinental, national average shown
    "Kosovo": 82.1, # Data availability can vary
    "Latvia": 79.9,
    "Liechtenstein": 85.0, # Often estimated
    "Lithuania": 80.9,
    "Luxembourg": 85.0,
    "Malta": 84.6,
    "Moldova": 75.5,
    "Monaco": 87.0, # Often highest, based on estimates
    "Montenegro": 80.0,
    "Netherlands": 83.0,
    "North Macedonia": 77.5,
    "Norway": 84.7,
    "Poland": 81.6,
    "Portugal": 84.4,
    "Romania": 79.4,
    "Russia": 77.8, # Transcontinental, national average shown
    "San Marino": 86.5, # Often estimated
    "Serbia": 78.5,
    "Slovakia": 80.7,
    "Slovenia": 83.9,
    "Spain": 86.2,
    "Sweden": 84.9,
    "Switzerland": 85.9,
    "Turkey": 80.5, # Transcontinental, national average shown
    "Ukraine": 76.7, # Pre-2022 or early 2022 data typically
    "United Kingdom": 82.9,
    # Vatican City data is typically not applicable/available in these datasets
}

# Convert dictionaries to DataFrames
european_life_expectancy_df = pd.DataFrame(list(european_life_expectancy.items()), columns=['country', 'lifeExp'])
male_life_expectancy_df = pd.DataFrame(list(male_life_expectancy_europe.items()), columns=['country', 'maleLifeExp'])
female_life_expectancy_df = pd.DataFrame(list(female_life_expectancy_europe.items()), columns=['country', 'femaleLifeExp'])

# Create choropleth maps
fig_total = px.choropleth(
    european_life_expectancy_df,
    locations="country",
    locationmode="country names",
    color="lifeExp",
    hover_name="country",
    hover_data={"lifeExp": True, "country": True},
    color_continuous_scale=px.colors.sequential.Viridis,
    title="Total Life Expectancy in Europe"
)

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
        projection_type="sinusoidal",
        fitbounds="locations",
        showcoastlines=True,
        coastlinecolor="Black",
        showland=True,
        landcolor="lightgray",
        showcountries=True,
        countrycolor="Black",
        showframe=False,
        showlakes=True,
        lakecolor="Blue",
        showocean=True,
        oceancolor="lightblue",
        countrywidth=0.5,
        showsubunits=True,
        resolution=50
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
fig = make_subplots(rows=2, cols=2, subplot_titles=("Total Life Expectancy", "Male Life Expectancy", "Female Life Expectancy"), specs=[[{'type': 'choropleth'}, {'type': 'choropleth'}],[{'type': 'choropleth'},{'type': 'choropleth'}]])

fig.add_trace(fig_total.data[0], row=1, col=1)
fig.add_trace(fig_male.data[0], row=2, col=2)
fig.add_trace(fig_female.data[0], row=2, col=1)
# Update layout for the combined figure
fig.update_layout(
    width=1200,
    height=800,
    title_text="Life Expectancy in Europe by Gender",
    geo=dict(
        showframe=False,
        projection_scale=4,
        center=dict(lat=54, lon=15),
        showlakes=True,
        showocean=True,
        oceancolor="darkblue",
        showcountries=True,  # Ensure countries are shown
        countrycolor="Black"   # Set the color for country borders
    ),
    geo2=dict(
        showframe=False,
        projection_scale=4,
        center=dict(lat=54, lon=15),
        showlakes=True,
        showocean=True,
        oceancolor="darkblue",
        showcountries=True,  # Ensure countries are shown
        countrycolor="Black"   # Set the color for country borders
    ),
    geo3=dict(
        showframe=False,
        projection_scale=5,
        center=dict(lat=54, lon=15),
        showlakes=True,
        showocean=True,
        oceancolor="darkblue",
        showcountries=True,  # Ensure countries are shown
        countrycolor="Black"   # Set the color for country borders
    ),
    geo4=dict(
        showframe=False,
        projection_scale=5,
        center=dict(lat=54, lon=15),
        showlakes=True,
        showocean=True,
        oceancolor="darkblue",
        showcountries=True,  # Ensure countries are shown
        countrycolor="Black"   # Set the color for country borders
    ),
)
file_path = os.path.abspath("european_life_expectancy.html")
fig.write_html(file_path)

webbrowser.open("file://" + file_path)