from dash import Dash, dcc, html
import plotly.express as px
from siphon.simplewebservice.ndbc import NDBC

app = Dash(__name__)

df = NDBC.latest_observations()
print(df.columns)

fig = px.scatter(df, x="water_temperature", y="air_temperature",
                 color="pressure", hover_name="station")

app.layout = html.Div([dcc.Graph(id="buoy-correlations", figure=fig)])

if __name__=="__main__":
    app.run_server(debug=True)