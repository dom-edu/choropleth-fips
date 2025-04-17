from urllib.request import urlopen
import json
import pandas as pd
import plotly.express as px
from dash import Dash, html , dcc, callback, Input, Output

# specify data sources 
COUNTIES_FIPS_URL = 'https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json'

FIPS_UNEMP_RATES = "https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv"

# Load in data 
with urlopen(COUNTIES_FIPS_URL) as response:
    counties = json.load(response)

fips_df = pd.read_csv(FIPS_UNEMP_RATES, dtype={"fips": str})


def create_choropleth(df):


    # create figure 
    choro = px.choropleth(df, geojson=counties, locations='fips', color='unemp',
                            color_continuous_scale="Viridis",
                            range_color=(0, 12),
                            scope="usa",
                            labels={'unemp':'unemployment rate'}
                            )
    choro.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return choro

# add range slider 
rs1 = dcc.RangeSlider(
    0, 
    12, 
    value=[2, 4], 
    id="range-slider-1", 
    included=True,
    tooltip={'always_visible':True}
    )


# instantiate app 
app = Dash() 
choro = create_choropleth(fips_df)

app.layout = [
    html.H1("Unemployment Rate By FIPS County ", style={'textAlign':'center'}),
    dcc.Graph(figure=choro, id="fips-choropleth"),
    rs1 
]
# setup callback
@callback(
    Output("fips-choropleth","figure"),
    Input("range-slider-1","value")
)
def update_graph(value):
    print(value)
    # filter counties by range values 
    # is the counties value between the start and the end?

    start = value[0]
    end = value[1]

    # greater than the start of slider point
    filter_ = fips_df['unemp'] >= start
    # less than the end slider point 
    filter_2 = (fips_df['unemp'] <= end)
    choro_filtered_df = fips_df[filter_ & filter_2]
    choro = create_choropleth(choro_filtered_df)

    return choro 

if __name__ == '__main__':
    app.run(port=5008, debug=True)
