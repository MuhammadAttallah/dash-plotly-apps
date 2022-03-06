from dash import Dash, dcc, html, Input, Output
import plotly.express as px
from siphon.simplewebservice.ndbc import NDBC


app = Dash(__name__)

df = NDBC.latest_observations()
print(df.columns)

@app.callback(
    Output("buoy-correlations", "figure"),
    Input("xvar-dropdown", "value"),
    Input("yvar-dropdown", "value"),
    Input("cvar-dropdown", "value")
)
def update_figure(x_var, y_var, c_var):
    fig = px.scatter(df, x=x_var, y=y_var,
                     color=c_var, hover_name="station")
    fig.update_layout(transition_duration=1000)
    return fig

@app.callback(
    Output("buoy-timeseries", "figure"),
    Input("buoy-correlations", "hoverData")
)
def update_timeseries(hoverData):
    station_name = hoverData["points"][0]["hovertext"]
    df = NDBC.realtime_observations(station_name)
    fig = px.scatter(df, x="time", y="pressure")
    fig.update_layout(transition_duration=1000)
    return fig

app.layout = html.Div([
    html.Div([
        html.H1("NDBC Network Data", style={"textAlign":"center"})
        ]),
    html.Div([
        html.Div([], style={"width":"10%"}),
        html.Div([
            html.Label("X variable"),
            html.Br(),
            dcc.Dropdown(df.columns, "water_temperature", id="xvar-dropdown")
            ], style={"width":"20%"}),
        html.Div([], style={"width":"10%"}),
        html.Div([
            html.Label("Y variable"),
            html.Br(),
            dcc.Dropdown(df.columns, "air_temperature", id="yvar-dropdown")
            ], style={"width":"20%"}),
        html.Div([], style={"width":"10%"}),
        html.Div([
            html.Label("Color variable"),
            html.Br(),
            dcc.Dropdown(df.columns, "pressure", id="cvar-dropdown")
            ], style={"width":"20%"}),
        html.Div([], style={"width":"10%"})
        ], style={"display":"flex", "flex-direction":"row"}),
    html.Div([
        html.Div([
            dcc.Graph(id="buoy-correlations",
                      hoverData={"points":[{"hovertext":"ASTO3"}]})
            ], style={"width":"35%"}),
        html.Div([], style={"width":"5%"}),
        html.Div([
            dcc.Graph(id="buoy-timeseries")
            ], style={"width":"60%"})
        ], style={"display":"flex", "flex-direction":"row"})
    ])

if __name__=="__main__":
    app.run_server(debug=True)