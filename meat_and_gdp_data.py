from pandas import merge, read_csv, DataFrame

def generate_meat_and_gdp_df(
        meat__filepath_or_buffer: str = "https://raw.githubusercontent.com/peterphung2043/CUNY_DATA_608/master/Final%20Project/data/world_meat_consumption.csv",
        gdp_per_cap__filepath_or_buffer: str = "https://raw.githubusercontent.com/peterphung2043/CUNY_DATA_608/master/Final%20Project/data/gdp_data.csv"
) -> DataFrame:
    """Generates the merged meat consumption and GDP per capita dataframe.

    Args:
        meat__filepath_or_buffer (_type_, optional): 
            The filepath to the `world_meat_consumption.csv`. The `.csv` file contains meat consumption data from OECD. collected from several countries
            Defaults to "https://raw.githubusercontent.com/peterphung2043/CUNY_DATA_608/master/Final%20Project/data/world_meat_consumption.csv".
        gdp_per_cap__filepath_or_buffer (_type_, optional): 
            The filepath to the `gdp_data.csv`. This `.csv` file contains GDP per capita data from The
            World Bank collected from many countries around the world. 
            Defaults to "https://raw.githubusercontent.com/peterphung2043/CUNY_DATA_608/master/Final%20Project/data/gdp_data.csv".

    Returns:
        DataFrame: 
            The merged meat consumption and GDP per capita dataframe.
    """
    # OECD Meat Consumption Data
    meat_consumption_df = read_csv(
        filepath_or_buffer=meat__filepath_or_buffer
    )

    # GDP Per Capita Data collected from The World Bank
    gdp_per_cap_df = read_csv(
        filepath_or_buffer=gdp_per_cap__filepath_or_buffer,
        nrows = 266,
        na_values=".."
    ).drop(columns = ['Series Name', 'Series Code'])

    gdp_per_cap_df = gdp_per_cap_df.rename(columns = (lambda x: x[:4] if x not in ['Country Code', 'Country Name'] else x)).melt(id_vars=['Country Code', 'Country Name']).rename(columns = {'variable': 'Year', 'value': 'GDP Per Capita'}).astype({'Year': "int64"})

    return merge(meat_consumption_df, gdp_per_cap_df, left_on=['LOCATION', 'TIME'], right_on=['Country Code', 'Year']).query('MEASURE == \'KG_CAP\' & Value != 0').drop(columns=['TIME', 'Country Code', 'INDICATOR', 'FREQUENCY', 'Flag Codes', 'LOCATION', 'MEASURE']).rename(columns = {'Country Name': 'Country'})

