from dash import dcc, html
from pandas import DataFrame

def generate_dropdowns(
        subject_list: list[str], 
        country_list: list[dict[str, str]], 
        year_list: list[dict[str, str]],
        ) -> list[html.Div]:
    """Generates a list of `html.Div` objects that act as dropdowns for
    the Dash app.

    Args:
        subject_list (list[str]): 
            The different meat types stored in a list.
        country_list (list[dict[str, str]]): 
            The different countries to select from stored in a list of dicts.
        year_list (list[dict[str, str]]): 
            The different years to select from stored in a list of dicts.

    Returns:
        list[html.Div]: 
            Each element represents a dropdown that is displayed on
            the Dash app.
    """

    meat_type_dropdown = html.Div(
                [
                    "Select Meat Type For Time Series Figure Below:",
                    dcc.RadioItems(
                    options=subject_list, 
                    value='BEEF', 
                    id='subject_selection'), 
                ],
                style={"width": 250,
                    "font-size": "15px"},
            )

    country_dropdown = html.Div(
            [
                "Select Country For Time Series and Correlation Figure Below:",
                dcc.Dropdown(
                id='country_selection', 
                options=country_list,
                value = 'Australia'),
            ],
            style={"width": 250,
                "font-size": "15px"},
        )

    year_dropdown = html.Div(
            [
                "Select Year For Bar Plots Below:",
                dcc.Dropdown(
                id='year_selection', 
                options=year_list,
                value = '2021'
                ),
            ],
            style={"width": 250,
                "font-size": "15px"},
        )
    
    return [meat_type_dropdown, country_dropdown, year_dropdown]