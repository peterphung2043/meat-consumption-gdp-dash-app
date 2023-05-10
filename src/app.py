from dash import Dash, html
from dash.dependencies import Input, Output
import plotting as plotting
from meat_and_gdp_data import generate_meat_and_gdp_df
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from numpy import sort
from app_children import generate_children


meat_and_gdp_df = generate_meat_and_gdp_df()
# Array consisting of different meat types
subject_array = meat_and_gdp_df['SUBJECT'].unique().tolist()
subject_array.append('ALL')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
                        dbc.themes.BOOTSTRAP]

app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.title = "GDP and Meat Consumption Per Capita Dash App"


country_list = [{'label': x, 'value': x} for x in sort(meat_and_gdp_df['Country'].unique())]
year_list = [{'label': x, 'value': x} for x in sort(meat_and_gdp_df['Year'].unique())]
subject_list = meat_and_gdp_df['SUBJECT'].unique().tolist()
subject_list.append('ALL')

app.layout = html.Div(
    children = generate_children(subject_list, country_list, year_list)
)

@app.callback([Output('ts_fig', 'figure'),
              Output('corr_fig', 'figure'),
              Output('gdp_fig_high', 'figure'),
              Output('gdp_fig_low', 'figure')],
              [Input('subject_selection', 'value'),
               Input('country_selection', 'value'),
               Input('year_selection', 'value')])

def update_figures(subject_selection: str, country_selection: str, year_selection: str) -> list[go.Figure]:
    """Updates the 4 figures in the dash app.

    Args:
        subject_selection (str): Meat type consumed. Uses the `SUBJECT` column in the `meat_and_gdp_df`
        country_selection (str): Meat consumption data is selected by the country in this `country_selection` variable.
        year_selection (str): Meat consumption data is selected by the year in this `year_selection` variable.

    Returns:
        list[go.Figure]:
            This list of figures is displayed on the Plotly Dash app.
    """

    df = meat_and_gdp_df.query("Country == \'{}\'".format(country_selection))

    ts_fig = plotting.generate_subject_time_series_plots(subject_selection = subject_selection, country_selection = country_selection, df = df)
    
    corr_fig = plotting.generate_correlation_fig(df)

    gdp_fig_high = plotting.generate_gdp_fig(
        meat_and_gdp_df.query('Year == {}'.format(year_selection)).groupby('Country').first().dropna(subset = 'GDP Per Capita')[['GDP Per Capita']].reset_index().round(2),
        year = year_selection,
        number_of_countries = 5)
    
    gdp_fig_low = plotting.generate_gdp_fig(
        meat_and_gdp_df.query('Year == {}'.format(year_selection)).groupby('Country').first().dropna(subset = 'GDP Per Capita')[['GDP Per Capita']].reset_index().round(2),
        year = year_selection,
        ascending = True,
        number_of_countries = 5)


    return [ts_fig, corr_fig, gdp_fig_high, gdp_fig_low]

if __name__ == '__main__':
    app.run_server(debug = True, port = 8000, use_reloader = False)