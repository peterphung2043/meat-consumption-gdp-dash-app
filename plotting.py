import plotly.graph_objects as go
from pandas import DataFrame
import plotly.express as px
from plotly.subplots import make_subplots

def add_figure_layers_by_subject(fig: go.Figure, df: DataFrame) -> go.Figure:
    """Adds figure layers by SUBJECT from the `meat_and_gdp_df`.

    Args:
        fig (go.Figure): 
            Plotly figure object

    Returns:
        go.Figure: 
            Plotly figure object with meat consumption data plotted by SUBJECT in different layers
    """
    for meat_type in df['SUBJECT'].unique():
        subject_df = df.query("SUBJECT == \'{}\'".format(meat_type))
        fig.add_trace(
            go.Scattergl(
                x = subject_df['Year'],
                y = subject_df['Value'],
                name = 'KG {} Consumed Per Capita'.format(meat_type)
            ),
            secondary_y = False
        )

    fig.update_layout(
        plot_bgcolor = "white"
    )
    
    return fig

def generate_correlation_df(
        df: DataFrame, 
        variable_1: str = 'Value', 
        variable_2: str = 'GDP Per Capita', 
        grouping_variables_list: list[str] = ['Country', 'SUBJECT']) -> DataFrame:
    """Calculates correlation between `variable_1` and `variable_2` after grouping by `grouping_variables_list` for `df`

    Args:
        df (pd.DataFrame): 
            The dataframe to perform the groupby and calculate the correlation.
        variable_1 (str, optional): 
            One of the correlation variables. Defaults to 'Value'.
        variable_2 (str, optional): 
            One of the correlation variables. Defaults to 'GDP Per Capita'.
        grouping_variables_list (list[str], optional): 
            The `by` parameter in the `pandas.groupby` function uses this variable. Defaults to ['Country', 'SUBJECT'].
    
    Returns:
        pd.DataFrame:
            Dataframe containing the correlations between `variable_1` and `variable_2`
    """
    corr_df = df.groupby(['Country', 'SUBJECT'])[['Value', 'GDP Per Capita']].corr().drop('GDP Per Capita', level = 2).reset_index()
    return corr_df.drop(columns = ['level_2', 'Value']).rename(columns = {'GDP Per Capita': 'Correlation'.format(variable_1, variable_2)})

def generate_correlation_fig(
        df: DataFrame,
        variable_1: str = "Value",
        variable_2: str = 'GDP Per Capita') -> go.Figure:
    """Generate a Plotly graph object that plots the correlations stored in `df` as a bar chart.
    Used in conjunction with `generate_correlation_df`.

    Args:
        df (pd.DataFrame):
            Contains the correlations between `variable_1` and `variable_2` from `generate_correlation_df`
        variable_1 (str, optional): 
            One of the correlation variables. Defaults to 'Value'. Gets passed into `generate_correlation_df`.
        variable_2 (str, optional): 
            One of the correlation variables. Defaults to 'GDP Per Capita'. Gets passed into `generate_correlation_df`

    Returns:
        go.Figure: 
            Plotly figure graph object with plotted correlations.
    """

    correlation_df = generate_correlation_df(df, variable_1, variable_2).round(decimals = 2)
    
    corr_fig = px.bar(
        correlation_df, 
        x = "SUBJECT", 
        y = "Correlation",
        color = "Correlation",
        color_continuous_scale=['red', 'blue'],
        range_color=(-1, 1),
        text_auto = True)

    corr_fig.update_layout(
        title = "Correlation Bar Plot Between {} and {} for {}".format(variable_1, variable_2, correlation_df['Country'][0]),
        plot_bgcolor = "white")
    
    corr_fig.update_yaxes(visible = False)
    return corr_fig

def generate_gdp_fig(
        top_gdp_df: DataFrame,
        year: int, 
        ascending: bool = False,
        number_of_countries: int = 10,
        continuous_column_to_plot: str = 'GDP Per Capita') -> go.Figure:
    """Generates Plotly graph figure object that plots the top `number_of_countries` highest or lowest 
    `continuous_column_to_plot`s and shows the respective countries for each value on the x-axis.

    Args:
        top_gdp_df (pd.DataFrame): 
            Contains the `Country` and the `GDP Per Capita`
        year (int):
            The year that the data in `top_gdp_df` pertains to.
        ascending (bool, optional): 
            If ascending, plots the top lowest `number_of_countries`. 
            Otherwise plots the top highest. Defaults to False.
        number_of_countries (int, optional): 
            The number of top highest or lowest GDP Per Capitas that are plotted. 
            Defaults to 10.
        continuous_column_to_plot (str, optional):
            The continuous data that is plotted on the y-axis. Defaults to `GDP Per Capita`.

    Returns:
        go.Figure: Plotly figure object that shows the top lowest or highest GDP per Capitas
        and the respective countries.
    """

    if ascending:
        highest_or_lowest = "Lowest"
    else:
        highest_or_lowest = "Highest"

    gdp_fig = px.bar(
        top_gdp_df.sort_values(by = continuous_column_to_plot, ascending=ascending)[0:number_of_countries], 
        x = "Country", 
        y = continuous_column_to_plot,
        text_auto = '%text:.3s')

    gdp_fig.update_layout(
        title = "Top {} {} {}s for {}".format(number_of_countries, highest_or_lowest, continuous_column_to_plot, year),
        plot_bgcolor = 'white',
        xaxis_title = None)

    gdp_fig.update_layout(yaxis_tickformat = ',')

    gdp_fig.update_yaxes(visible = False)
    return gdp_fig

# Create figure with secondary y-axis
def generate_subject_time_series_plots(
        subject_selection: str, 
        country_selection: str, 
        df: DataFrame) -> go.Figure:
    """Generates a Plotly figure object that plots each of the different meat types.

    Args:
        subject_selection (str): 
            A meat type. Can be any value from this list: `['POULTRY', 'SHEEP', 'BEEF', 'PIG', 'ALL']`.
            If this argument is set to `ALL`, then all 4 different meat types will be plotted.
        country_selection (str): 
            The country from which the meat data was collected from.
        df (pd.DataFrame): 
            Contains the meat data for the country selected using `country_selection`

    Returns:
        go.Figure: 
            Plotly figure object plotting one or all the different meat types on different layers.
    """
    ts_fig = make_subplots(specs=[[{"secondary_y": True}]])

    if subject_selection == 'ALL':
        ts_fig = add_figure_layers_by_subject(ts_fig, df)
    else:
        ts_fig.add_trace(
            go.Scattergl(x = df.query("SUBJECT == \'{}\'".format(subject_selection))['Year'], 
                        y = df.query("SUBJECT == \'{}\'".format(subject_selection))['Value'],
                        name = "KG Consumed Per Capita",
                        line = dict(color='firebrick', width=4, dash='dot')),
            secondary_y=False,
        )

    ts_fig.add_trace(
        go.Scatter(x = df.query("SUBJECT == \'{}\'".format(subject_selection))['Year'], 
                    y = df.query("SUBJECT == \'{}\'".format(subject_selection))['GDP Per Capita'],
                    name = "GDP Per Capita",
                    line=dict(color='royalblue', width=4, dash='dot')),
        secondary_y=True,
    )

    # Add figure title
    ts_fig.update_layout(
        title_text="KG Consumed and GDP Per Capita for {} in {}".format(subject_selection, country_selection)
    )

    # Set x-axis title
    ts_fig.update_xaxes(title_text="Year")

    # Set y-axes titles
    ts_fig.update_yaxes(title_text="KG Consumed Per Capita", secondary_y=False)
    ts_fig.update_yaxes(title_text="GDP Per Capita", secondary_y=True)

    ts_fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))

    return ts_fig