from dash import html, dcc
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dropdowns import generate_dropdowns
from typing import Any

def generate_children(subject_list: list[str], 
                      country_list: list[dict[str, str]], 
                      year_list: list[dict[str, str]]
                      ) -> list[Any]:
    """Generates the overall Dash app layout stored in the `children` variable in `app.layout`.

    Args:
        subject_list (list[str]): 
            The different meat types stored in a list.
        country_list (list[dict[str, str]]): 
            The different countries to select from stored in a list of dicts.
        year_list (list[dict[str, str]]): 
            The different years to select from stored in a list of dicts.

    Returns:
        list[Any]:
            The overall schema of the app.
    """
    
    
    meat_type_dropdown, country_dropdown, year_dropdown = generate_dropdowns(
        subject_list, 
        country_list, 
        year_list
        )
    
    children=[
        html.Div(
            children = [
                html.H1(children='GDP and Meat Consumption Per Capita Dash App',
                        className = "header-title",
                        style = {"text-align": "center",
                                    "fontSize": 40,
                                    "color": "red"}),
                html.P(
                    children = (
                        "Exploration of GDP Per Capita collected from The World Bank"
                        " and meat consumption data collected from OECD. Created by"
                        " Peter Phung."
                    ),
                    className = "header-description",
                    style = {"fontSize": 20,
                             "text-align": "center"}
                ),
                html.Hr()
            ],
            className = "header"
        ),

    dbc.Container(
        [
            dbc.Row([dbc.Col(meat_type_dropdown), dbc.Col(country_dropdown)])
        ],
        fluid = True
    ),

    dmc.Grid([
        dmc.Col([
            dcc.Graph(
                figure={}, 
                id='ts_fig',
                style = {"border": "2px black solid"})
        ], span=6),
        dmc.Col([
            dcc.Graph(
                figure={}, 
                id='corr_fig',
                style = {"border": "2px black solid"})
        ], span=6)
    ]),

    dbc.Container(
        [
            dbc.Row([dbc.Col(year_dropdown)])
        ],
        fluid = True
    ),

    dmc.Grid([
        dmc.Col([
            dcc.Graph(
                figure={}, 
                id='gdp_fig_low',
                style = {"border": "2px black solid"})
        ], span=6),
        dmc.Col([
            dcc.Graph(
                figure={}, 
                id='gdp_fig_high',
                style = {"border": "2px black solid"})
        ], span=6)
    ]),
    ]

    return children
