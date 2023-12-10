import pandas as pd
from sklearn.metrics.pairwise import haversine_distances
from math import radians


def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here
    coords = df[['latitude', 'longitude']].applymap(radians)
    distance_matrix = pd.DataFrame(haversine_distances(coords, coords), index=df['id'], columns=df['id'])

    return distance_matrix

    


def unroll_distance_matrix(distance_matrix)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here
    unrolled_df =distance_matrix.unstack().reset_index()
    unrolled_df.columns = ['id_start', 'id_end', 'distance']

    return unrolled_df

    


def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Write your logic here
    reference_avg_distance = df[df['id_start'] == reference_id]['distance'].mean()
    threshold = 0.1 * reference_avg_distance

    selected_ids = df.groupby('id_start')['distance'].mean().loc[lambda x: (x >= reference_avg_distance - threshold) & (x <= reference_avg_distance + threshold)].index

    result_df = df[df['id_start'].isin(selected_ids)]

    return result_df

    


def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here
    toll_rates = {'car': 0.1, 'truck': 0.2, 'bus': 0.15}
    df['toll_rate'] = df['vehicle_type'].map(toll_rates)

    return df

   


def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here
    df['hour'] = df['timestamp'].dt.hour

    # Define time-based toll rates (example rates, you can modify as needed)
    time_based_toll_rates = {
        (0, 6): 0.1,
        (6, 12): 0.15,
        (12, 18): 0.2,
        (18, 24): 0.1
    }

    # Assign toll rates based on time intervals
    for (start_hour, end_hour), rate in time_based_toll_rates.items():
        df.loc[(df['hour'] >= start_hour) & (df['hour'] < end_hour), 'time_based_toll_rate'] = rate

    df = df.drop(columns=['hour'])

    return df

    
