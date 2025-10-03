import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.data as pldata
import webbrowser

# Initialize Dash
app = dash.Dash(__name__)
server = app.server  # Needed for Render deployment

# Load data
df = pldata.gapminder()
countries = df["country"].unique()

# Layout
app.layout = html.Div([
    html.H1("GDP Growth Dashboard"),
    dcc.Dropdown(
        id="country-dropdown",
        options=[{"label": c, "value": c} for c in countries],
        value="Canada"
    ),
    dcc.Graph(id="gdp-growth")
])

# Callback
@app.callback(
    Output("gdp-growth", "figure"),
    [Input("country-dropdown", "value")]
)
def update_graph(selected_country):
    filtered = df[df["country"] == selected_country]
    fig = px.line(
        filtered, x="year", y="gdpPercap",
        title=f"GDP Per Capita Growth for {selected_country}"
    )
    return fig

# Entry point
if __name__ == "__main__":
    import webbrowser
    webbrowser.open("http://127.0.0.1:8050/")
    app.run(debug=True)

