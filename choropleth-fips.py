from urllib.request import urlopen
import json
import pandas as pd
import plotly.express as px
from dash import Dash, html , dcc

# specify data sources 
COUNTIES_FIPS_URL = 'https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json'

FIPS_UNEMP_RATES = "https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv"

# Load in data 
with urlopen(COUNTIES_FIPS_URL) as response:
    counties = json.load(response)

fips_df = pd.read_csv(FIPS_UNEMP_RATES, dtype={"fips": str})


# create figure 
choro = px.choropleth(fips_df, geojson=counties, locations='fips', color='unemp',
                           color_continuous_scale="Viridis",
                           range_color=(0, 12),
                           scope="usa",
                           labels={'unemp':'unemployment rate'}
                          )
choro.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# add range slider 
rs1 = dcc.RangeSlider(0, 12, value=[2, 4], id="range-slider-1", included=True)


# instantiate app 
app = Dash() 

app.layout = [
    html.H1("Unemployment Rate By FIPS County ", style={'textAlign':'center'}),
    dcc.Graph(figure=choro),
    rs1 
]

if __name__ == '__main__':
    app.run(port=5008, debug=True)
