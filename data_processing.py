import pandas as pd
import numpy as np
from datetime import datetime

def load_and_clean_data(file_path):
    """
    Load the air quality dataset and perform initial cleaning
    
    Parameters:
    file_path (str): Path to the CSV file
    
    Returns:
    pd.DataFrame: Cleaned dataframe
    """
    try:
        # Load data with semicolon separator and handle European decimal format
        df = pd.read_csv(file_path, sep=";", decimal=",")
        
        # Remove trailing semicolons in column names
        df.columns = df.columns.str.rstrip(';')
        
        # Drop empty columns if they exist
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        
        # Replace -200 with NaN in numeric columns (represents missing data in this dataset)
        for col in df.columns:
            if col not in ['Date', 'Time']:
                df[col] = df[col].replace(-200, np.nan)
        
        return df
    
    except Exception as e:
        raise Exception(f"Error loading data: {str(e)}")

def handle_missing_values(df):
    """
    Handle missing values in the dataset
    
    Parameters:
    df (pd.DataFrame): Input dataframe
    
    Returns:
    pd.DataFrame: Dataframe with handled missing values
    """
    # Create a copy to avoid modifying the original
    df_cleaned = df.copy()
    
    # For each column, apply appropriate missing value strategy
    for col in df_cleaned.columns:
        if col not in ['Date', 'Time']:
            # For missing values, use linear interpolation first
            df_cleaned[col] = df_cleaned[col].interpolate(method='linear', limit_direction='both')
            
            # If there are still NaN values, use forward fill
            df_cleaned[col] = df_cleaned[col].fillna(method='ffill')
            
            # If there are still NaN values (at the start), use backward fill
            df_cleaned[col] = df_cleaned[col].fillna(method='bfill')
            
            # If any NaN values remain, fill with column mean
            df_cleaned[col] = df_cleaned[col].fillna(df_cleaned[col].mean())
    
    return df_cleaned

def preprocess_data(df):
    """
    Preprocess the data for analysis
    
    Parameters:
    df (pd.DataFrame): Input dataframe
    
    Returns:
    pd.DataFrame: Preprocessed dataframe
    """
    # Create a copy to avoid modifying the original
    df_processed = df.copy()
    
    # Handle missing values
    df_processed = handle_missing_values(df_processed)
    
    # Convert date and time columns to datetime format
    if 'Date' in df_processed.columns and 'Time' in df_processed.columns:
        # Combine date and time and convert to datetime
        df_processed['DateTime'] = pd.to_datetime(
            df_processed['Date'] + ' ' + df_processed['Time'], 
            format='%d/%m/%Y %H.%M.%S',
            errors='coerce'
        )
    
    # Ensure all numeric columns are of the right type
    numeric_cols = df_processed.columns.difference(['Date', 'Time', 'DateTime'])
    df_processed[numeric_cols] = df_processed[numeric_cols].apply(pd.to_numeric, errors='coerce')
    
    # Optionally, add derived features
    # Calculate hour of day
    if 'DateTime' in df_processed.columns:
        df_processed['Hour'] = df_processed['DateTime'].dt.hour
        df_processed['Day'] = df_processed['DateTime'].dt.day_name()
        df_processed['Month'] = df_processed['DateTime'].dt.month_name()
    
    return df_processed
