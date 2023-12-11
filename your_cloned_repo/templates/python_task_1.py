import pandas as pd


def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here
    unique_id_1 = df['id_1'].unique()
    unique_id_2 = df['id_2'].unique()

    # Generate all combinations of id_1 and id_2
    id_combinations = list(multiply_matrix(unique_id_1, unique_id_2))

    # Create an empty DataFrame with id_1 and id_2 as indices and columns
    matrix = pd.DataFrame(index=unique_id_1, columns=unique_id_2)

    # Fill the DataFrame with 'car' values
    for id_1, id_2 in id_combinations:
        car_value = df[(df['id_1'] == id_1) & (df['id_2'] == id_2)]['car'].values
        if len(car_value) > 0:
            matrix.at[id_1, id_2] = car_value[0]

    return matrix

    


def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    car_type_counts = df['car'].value_counts().to_dict()

    return car_type_counts

    


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
    bus_indexes = df[(df['car'] == 'bus') & (df['car'].gt(2 * df['car'].mean()))].index.tolist()

    return bus_indexes

    


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    route_averages = df.groupby('route')['truck'].mean()

    # Filter routes where the average 'truck' value is greater than 7
    selected_routes = route_averages[route_averages > 7].index.tolist()

    return selected_routes

    


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    threshold = 5  # Define  custom threshold

    # Use applymap to apply a function element-wise to the entire matrix
    modified_matrix = matrix.applymap(lambda x: x * 2 if x > threshold else x)

    return modified_matrix

    


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Calculate the time difference for each unique (`id`, `id_2`) pair
    time_diff = df.groupby(['id', 'id_2'])['timestamp'].apply(lambda x: (x.max() - x.min()))

    # Check if each time difference covers a full 24-hour and 7 days period
    completeness_check = time_diff == pd.Timedelta(days=7) - pd.Timedelta(seconds=1)

    return completeness_check

    
