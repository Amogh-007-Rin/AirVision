import pandas as pd
import numpy as np
from scipy import stats

def perform_statistical_analysis(df):
    """
    Perform statistical analysis on the dataset
    
    Parameters:
    df (pd.DataFrame): Processed dataframe
    
    Returns:
    pd.DataFrame: DataFrame with statistical summaries
    """
    # Get numerical columns only
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    # Calculate statistics
    stats_df = pd.DataFrame({
        'Mean': df[numeric_cols].mean(),
        'Median': df[numeric_cols].median(),
        'Std Dev': df[numeric_cols].std(),
        'Min': df[numeric_cols].min(),
        'Max': df[numeric_cols].max(),
        'Q1 (25%)': df[numeric_cols].quantile(0.25),
        'Q3 (75%)': df[numeric_cols].quantile(0.75)
    })
    
    # Round for better display
    stats_df = stats_df.round(2)
    
    return stats_df

def calculate_aqi(df):
    """
    Calculate Air Quality Index (AQI) from pollutant data
    
    Parameters:
    df (pd.DataFrame): Processed dataframe
    
    Returns:
    pd.DataFrame: DataFrame with AQI values
    """
    # Create a copy of datetime column for the output
    aqi_data = pd.DataFrame()
    aqi_data['DateTime'] = df['DateTime']
    
    # Get key pollutants for AQI calculation
    # This is a simplified AQI calculation for demonstration purposes
    # In a real application, you would use standard EPA formulas
    
    # Normalize and combine key pollutants
    key_pollutants = ['CO(GT)', 'C6H6(GT)', 'NOx(GT)', 'NO2(GT)']
    
    # Check if all key pollutants are in the dataframe
    available_pollutants = [p for p in key_pollutants if p in df.columns]
    
    if not available_pollutants:
        raise ValueError("None of the key pollutants needed for AQI calculation are available in the dataset.")
    
    # Normalize each pollutant (0-100 scale where 100 is the max value)
    normalized = pd.DataFrame()
    
    for pollutant in available_pollutants:
        max_val = df[pollutant].max()
        min_val = df[pollutant].min()
        
        if max_val > min_val:  # Avoid division by zero
            normalized[pollutant] = 100 * (df[pollutant] - min_val) / (max_val - min_val)
        else:
            normalized[pollutant] = 0
    
    # Calculate AQI as the max of normalized pollutants
    aqi_data['AQI'] = normalized.max(axis=1)
    
    return aqi_data

def detect_outliers(df, columns=None):
    """
    Detect outliers in the dataset
    
    Parameters:
    df (pd.DataFrame): Processed dataframe
    columns (list, optional): List of columns to check for outliers
    
    Returns:
    pd.DataFrame: DataFrame containing only the outlier rows
    """
    if columns is None:
        # Use all numeric columns
        columns = df.select_dtypes(include=[np.number]).columns
    
    # Create a mask for rows that contain outliers
    outlier_mask = pd.Series(False, index=df.index)
    
    for column in columns:
        if column in df.columns and df[column].dtype in [np.float64, np.int64]:
            # Use Z-score to detect outliers
            z_scores = np.abs(stats.zscore(df[column].dropna()))
            z_score_mask = pd.Series(False, index=df.index)
            z_score_mask.loc[df[column].dropna().index] = z_scores > 3
            
            # Update the overall mask
            outlier_mask = outlier_mask | z_score_mask
    
    # Filter the dataframe to get only the outlier rows
    outliers_df = df[outlier_mask].copy()
    
    # Add information about which columns caused each row to be considered an outlier
    for column in columns:
        if column in df.columns and df[column].dtype in [np.float64, np.int64]:
            z_scores = pd.Series(np.nan, index=df.index)
            non_na_idx = df[column].dropna().index
            z_scores.loc[non_na_idx] = np.abs(stats.zscore(df[column].dropna()))
            
            outliers_df[f"{column}_z_score"] = z_scores
            outliers_df[f"{column}_is_outlier"] = z_scores > 3
    
    return outliers_df

def perform_time_analysis(df):
    """
    Perform time-based analysis on the dataset
    
    Parameters:
    df (pd.DataFrame): Processed dataframe
    
    Returns:
    dict: Dictionary with different time-based analyses
    """
    result = {}
    
    # Ensure we have the datetime columns
    if 'DateTime' not in df.columns:
        raise ValueError("DataFrame must contain 'DateTime' column for time analysis")
    
    # Get numeric columns for analysis
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    numeric_cols = [col for col in numeric_cols if col not in ['Hour', 'Day', 'Month']]
    
    # Hourly analysis
    hourly_df = df.groupby('Hour')[numeric_cols].mean().reset_index()
    result['hourly'] = hourly_df
    
    # Daily analysis if we have day names
    if 'Day' in df.columns:
        # Define day order for proper sorting
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        # Create categorical day variable with ordered categories
        df['Day_cat'] = pd.Categorical(df['Day'], categories=day_order, ordered=True)
        
        daily_df = df.groupby('Day_cat', observed=True)[numeric_cols].mean().reset_index()
        daily_df.rename(columns={'Day_cat': 'Day'}, inplace=True)
        
        result['daily'] = daily_df
    
    # Monthly analysis if we have month data
    if 'Month' in df.columns:
        # Define month order for proper sorting
        month_order = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]
        
        # Check if we have enough months to make this analysis meaningful
        unique_months = df['Month'].nunique()
        
        if unique_months > 1:
            # Create categorical month variable with ordered categories
            df['Month_cat'] = pd.Categorical(df['Month'], categories=month_order, ordered=True)
            
            monthly_df = df.groupby('Month_cat', observed=True)[numeric_cols].mean().reset_index()
            monthly_df.rename(columns={'Month_cat': 'Month'}, inplace=True)
            
            result['monthly'] = monthly_df
    
    return result
