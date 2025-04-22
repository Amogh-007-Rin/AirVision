import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Import color scheme
from styles import COLORS

def create_pollutant_timeseries(df, pollutants):
    """
    Create time series visualization for selected pollutants
    
    Parameters:
    df (pd.DataFrame): Processed dataframe
    pollutants (list): List of pollutant columns to visualize
    
    Returns:
    go.Figure: Plotly figure object
    """
    fig = go.Figure()
    
    for i, pollutant in enumerate(pollutants):
        color = list(COLORS.values())[i % len(COLORS)]
        
        fig.add_trace(
            go.Scatter(
                x=df['DateTime'],
                y=df[pollutant],
                mode='lines',
                name=pollutant,
                line=dict(color=color, width=2),
                hovertemplate=f"{pollutant}: %{{y:.2f}}<br>Time: %{{x}}<extra></extra>"
            )
        )
    
    fig.update_layout(
        title="Temporal Component Analysis",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0.2)',
        xaxis_title="Timeline",
        yaxis_title="Concentration",
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Add futuristic grid lines
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(0, 255, 255, 0.1)',
        zeroline=False
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(0, 255, 255, 0.1)',
        zeroline=False
    )
    
    return fig

def create_correlation_heatmap(df):
    """
    Create correlation heatmap for all variables
    
    Parameters:
    df (pd.DataFrame): Processed dataframe
    
    Returns:
    go.Figure: Plotly figure object
    """
    # Calculate correlation matrix
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    corr_matrix = df[numeric_cols].corr()
    
    # Create heatmap
    fig = px.imshow(
        corr_matrix,
        x=numeric_cols,
        y=numeric_cols,
        color_continuous_scale=[
            [0, COLORS["dark_blue"]],
            [0.5, COLORS["dark_bg"]],
            [1, COLORS["neon_pink"]]
        ],
        zmin=-1,
        zmax=1
    )
    
    # Update layout
    fig.update_layout(
        title="Interdimensional Component Correlation Matrix",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0.2)',
        xaxis_title="Component Variable",
        yaxis_title="Component Variable",
        height=700
    )
    
    # Add correlation values as text
    for i, row in enumerate(corr_matrix.index):
        for j, col in enumerate(corr_matrix.columns):
            fig.add_annotation(
                x=col,
                y=row,
                text=f"{corr_matrix.loc[row, col]:.2f}",
                showarrow=False,
                font=dict(
                    color="white" if abs(corr_matrix.loc[row, col]) < 0.7 else "black",
                    size=8
                )
            )
    
    return fig

def create_scatter_plot(df, x_var, y_var, color_var=None):
    """
    Create scatter plot for two variables
    
    Parameters:
    df (pd.DataFrame): Processed dataframe
    x_var (str): Column name for x-axis
    y_var (str): Column name for y-axis
    color_var (str, optional): Column name for color encoding
    
    Returns:
    go.Figure: Plotly figure object
    """
    if color_var:
        fig = px.scatter(
            df,
            x=x_var,
            y=y_var,
            color=color_var,
            color_continuous_scale=[
                COLORS["dark_blue"],
                COLORS["neon_cyan"],
                COLORS["neon_green"],
                COLORS["neon_yellow"],
                COLORS["neon_pink"]
            ],
            opacity=0.7,
            title=f"Component Correlation: {x_var} vs {y_var}"
        )
    else:
        fig = px.scatter(
            df,
            x=x_var,
            y=y_var,
            color_discrete_sequence=[COLORS["neon_cyan"]],
            opacity=0.7,
            title=f"Component Correlation: {x_var} vs {y_var}"
        )
    
    # Add trend line
    fig.add_trace(
        go.Scatter(
            x=df[x_var],
            y=df[y_var].rolling(window=min(50, len(df))).mean(),
            mode='lines',
            name='Quantum Trend Analysis',
            line=dict(color=COLORS["neon_pink"], width=2)
        )
    )
    
    # Update layout
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0.2)',
        xaxis_title=x_var,
        yaxis_title=y_var,
        height=600
    )
    
    # Add futuristic grid lines
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(0, 255, 255, 0.1)',
        zeroline=False
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(0, 255, 255, 0.1)',
        zeroline=False
    )
    
    return fig

def create_distribution_plot(df, variable):
    """
    Create distribution plot for a variable
    
    Parameters:
    df (pd.DataFrame): Processed dataframe
    variable (str): Column name to visualize
    
    Returns:
    go.Figure: Plotly figure object
    """
    # Create figure with histogram and kde
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add histogram
    fig.add_trace(
        go.Histogram(
            x=df[variable],
            name="Frequency",
            marker=dict(
                color=COLORS["neon_blue"],
                line=dict(color=COLORS["neon_cyan"], width=1)
            ),
            opacity=0.7,
            nbinsx=30
        )
    )
    
    # Calculate kernel density estimate using numpy instead of matplotlib
    from scipy import stats as spstats
    
    # Create a safe range for KDE
    min_val = df[variable].min()
    max_val = df[variable].max()
    kde_x = np.linspace(min_val, max_val, 100)
    
    # Use scipy's gaussian_kde instead of pandas/matplotlib
    try:
        kde = spstats.gaussian_kde(df[variable].dropna())
        kde_y = kde(kde_x)
    except:
        # Fallback if KDE fails
        kde_y = np.zeros_like(kde_x)
        
    # Normalize to match the histogram scale
    if kde_y.max() > 0:
        kde_y = kde_y / kde_y.max() * df[variable].value_counts(bins=30, normalize=True).max() * 5
    
    fig.add_trace(
        go.Scatter(
            x=kde_x,
            y=kde_y,
            mode='lines',
            name="Density",
            line=dict(color=COLORS["neon_green"], width=3),
        ),
        secondary_y=True
    )
    
    # Update layout
    fig.update_layout(
        title=f"Quantum Distribution Analysis: {variable}",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0.2)',
        xaxis_title=variable,
        yaxis_title="Frequency",
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # Update secondary y-axis
    fig.update_yaxes(title_text="Density", secondary_y=True)
    
    # Add futuristic grid lines
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(0, 255, 255, 0.1)',
        zeroline=False
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(0, 255, 255, 0.1)',
        zeroline=False
    )
    
    return fig

def create_pollutant_radar(df):
    """
    Create radar chart for average pollutant levels
    
    Parameters:
    df (pd.DataFrame): Processed dataframe
    
    Returns:
    go.Figure: Plotly figure object
    """
    # Get relevant pollutant columns
    pollutant_cols = ['CO(GT)', 'NMHC(GT)', 'C6H6(GT)', 'NOx(GT)', 'NO2(GT)']
    
    # Calculate mean for each pollutant
    means = df[pollutant_cols].mean()
    
    # Normalize for radar chart (0-1 scale)
    normalized = (means - means.min()) / (means.max() - means.min())
    
    # Prepare radar chart data
    categories = pollutant_cols
    values = normalized.values.tolist()
    
    # Add the first value at the end to close the loop
    categories.append(categories[0])
    values.append(values[0])
    
    # Create radar chart
    fig = go.Figure()
    
    fig.add_trace(
        go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            fillcolor=f'rgba{tuple(int(COLORS["neon_blue"].lstrip("#")[i:i+2], 16) for i in (0, 2, 4)) + (0.5,)}',
            line=dict(color=COLORS["neon_cyan"], width=3),
            name="Normalized Concentration"
        )
    )
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                tickfont=dict(color=COLORS["text_light"]),
                gridcolor=COLORS["grid_color"],
                gridwidth=1
            ),
            angularaxis=dict(
                tickfont=dict(color=COLORS["text_light"]),
                gridcolor=COLORS["grid_color"],
                gridwidth=1
            ),
            bgcolor='rgba(0,0,0,0.2)'
        ),
        title="Atmospheric Component Radar Analysis",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        height=500
    )
    
    return fig

def create_3d_scatter(df, x_var, y_var, z_var):
    """
    Create 3D scatter plot
    
    Parameters:
    df (pd.DataFrame): Processed dataframe
    x_var (str): Column name for x-axis
    y_var (str): Column name for y-axis
    z_var (str): Column name for z-axis
    
    Returns:
    go.Figure: Plotly figure object
    """
    # Sample data to avoid overcrowding
    if len(df) > 1000:
        sample_df = df.sample(1000, random_state=42)
    else:
        sample_df = df
    
    # Create 3D scatter plot
    fig = go.Figure(data=[
        go.Scatter3d(
            x=sample_df[x_var],
            y=sample_df[y_var],
            z=sample_df[z_var],
            mode='markers',
            marker=dict(
                size=5,
                color=sample_df[x_var],
                colorscale=[
                    [0, COLORS["dark_blue"]],
                    [0.25, COLORS["neon_blue"]],
                    [0.5, COLORS["neon_cyan"]],
                    [0.75, COLORS["neon_green"]],
                    [1, COLORS["neon_yellow"]]
                ],
                opacity=0.8,
                colorbar=dict(
                    title=x_var,
                    thickness=20,
                    len=0.5
                )
            ),
            hovertemplate=
                f"{x_var}: %{{x:.2f}}<br>" +
                f"{y_var}: %{{y:.2f}}<br>" +
                f"{z_var}: %{{z:.2f}}<extra></extra>"
        )
    ])
    
    # Update layout
    fig.update_layout(
        title=f"3D Quantum Visualization: {x_var} vs {y_var} vs {z_var}",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0.2)',
        scene=dict(
            xaxis_title=x_var,
            yaxis_title=y_var,
            zaxis_title=z_var,
            xaxis=dict(
                gridcolor=COLORS["grid_color"],
                showbackground=False,
                zeroline=False
            ),
            yaxis=dict(
                gridcolor=COLORS["grid_color"],
                showbackground=False,
                zeroline=False
            ),
            zaxis=dict(
                gridcolor=COLORS["grid_color"],
                showbackground=False,
                zeroline=False
            )
        ),
        height=700
    )
    
    return fig
