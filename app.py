import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

# Import custom modules
from data_processing import load_and_clean_data, preprocess_data, handle_missing_values
from visualization import (
    create_pollutant_timeseries, 
    create_correlation_heatmap, 
    create_scatter_plot,
    create_distribution_plot,
    create_pollutant_radar,
    create_3d_scatter
)
from analysis import (
    perform_statistical_analysis, 
    calculate_aqi, 
    detect_outliers,
    perform_time_analysis
)
from styles import set_sci_fi_style, COLORS, add_logo, add_glowing_effect

# Page configuration
st.set_page_config(
    page_title="AirVision 2084 - Atmospheric Analysis Hub",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply sci-fi styling
set_sci_fi_style()

# Main application
def main():
    # Add page header with glowing effect
    add_glowing_effect(
        st.title("AirVision 2084 - Atmospheric Analysis Hub"),
        color=COLORS["neon_cyan"]
    )
    
    st.markdown("""
    <div style='text-align: center; margin-bottom: 30px;'>
        <p style='color: #00BFFF; font-style: italic;'>
            Analyzing Earth's atmosphere through advanced quantum processing algorithms
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Apply clean dark background
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #0E1117;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    # Display sleek loader animation
    with st.spinner("Initializing quantum processors..."):
        time.sleep(1)
    
    # Sidebar
    with st.sidebar:
        st.image("https://images.unsplash.com/photo-1584111514731-a3efadd23914", use_column_width=True)
        st.title("Control Panel")
        
        # Data loading section
        st.header("Data Source")
        uploaded_file = st.file_uploader("Upload Atmospheric Data (CSV)", type="csv")
        
        use_sample_data = st.checkbox("Use Planetary Reference Data", value=True)
        
        show_cleaned_data = st.checkbox("Show Cleansed Data", value=False)
        
        st.header("Analysis Parameters")
        analysis_time_period = st.slider(
            "Analysis Time Window (Days)",
            min_value=1,
            max_value=30,
            value=7
        )
        
        st.header("Visualization Controls")
        chart_theme = st.selectbox(
            "Quantum Visualization Theme",
            options=["dark", "cyberpunk", "matrix", "plasma"],
            index=0
        )
        
        st.header("Export Options")
        export_format = st.selectbox(
            "Data Export Format",
            options=["CSV", "Excel", "JSON"],
            index=0
        )
        
        if st.button("🔄 Initialize Analysis", key="initialize"):
            st.success("Analysis parameters configured!")
    
    # Load data
    @st.cache_data
    def get_data():
        if uploaded_file is not None:
            df = load_and_clean_data(uploaded_file)
        elif use_sample_data:
            df = load_and_clean_data("attached_assets/AirQualityUCI.csv")
        else:
            st.error("Please upload data or use sample data.")
            return None
        return df
    
    df = get_data()
    
    if df is not None:
        # Add subtle animation effect
        with st.container():
            st.markdown(
                """
                <div class="scanner-wrapper">
                    <div class="scanner"></div>
                </div>
                <style>
                .scanner-wrapper {
                    position: relative;
                    height: 5px;
                    overflow: hidden;
                    margin-bottom: 20px;
                }
                .scanner {
                    position: absolute;
                    height: 5px;
                    width: 100px;
                    background: linear-gradient(to right, transparent, #00FFFF, transparent);
                    animation: scan 3s infinite;
                }
                @keyframes scan {
                    0% { left: -100px; }
                    100% { left: 100%; }
                }
                </style>
                """,
                unsafe_allow_html=True,
            )
            
            # Process the data
            df_processed = preprocess_data(df)
            
            # Show data if requested
            if show_cleaned_data:
                st.subheader("Processed Atmospheric Data")
                st.dataframe(df_processed.head(100), use_container_width=True)
            
            # Create tabs for different analyses
            tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
                "Atmospheric Overview", 
                "Pollutant Analysis", 
                "Correlation Matrix", 
                "Temporal Patterns",
                "Advanced Analytics",
                "Machine Learning"
            ])
            
            with tab1:
                st.subheader("Planetary Atmosphere Status")
                
                # Summary statistics
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### Statistical Analysis")
                    stats = perform_statistical_analysis(df_processed)
                    st.dataframe(stats, use_container_width=True)
                
                with col2:
                    st.markdown("#### Atmospheric Composition")
                    fig = create_pollutant_radar(df_processed)
                    st.plotly_chart(fig, use_container_width=True)
                
                # AQI calculation
                st.subheader("Air Quality Index Analysis")
                aqi_data = calculate_aqi(df_processed)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Time series of AQI
                    fig = px.line(
                        aqi_data, 
                        x='DateTime', 
                        y='AQI',
                        color_discrete_sequence=[COLORS["neon_green"]],
                        title="Temporal AQI Fluctuations"
                    )
                    fig.update_layout(
                        template="plotly_dark",
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0.2)',
                        xaxis_title="Timeline",
                        yaxis_title="AQI Value",
                        hovermode="x unified"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # AQI distribution
                    fig = px.histogram(
                        aqi_data, 
                        x='AQI', 
                        color_discrete_sequence=[COLORS["neon_purple"]],
                        title="AQI Distribution Analysis"
                    )
                    fig.update_layout(
                        template="plotly_dark",
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0.2)',
                        xaxis_title="AQI Value",
                        yaxis_title="Frequency",
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            with tab2:
                st.subheader("Pollutant Molecular Analysis")
                
                # Allow user to select pollutants to display
                pollutants = [
                    'CO(GT)', 'PT08.S1(CO)', 'NMHC(GT)', 'C6H6(GT)',
                    'PT08.S2(NMHC)', 'NOx(GT)', 'PT08.S3(NOx)', 'NO2(GT)',
                    'PT08.S4(NO2)', 'PT08.S5(O3)', 'T', 'RH', 'AH'
                ]
                
                selected_pollutants = st.multiselect(
                    "Select Atmospheric Components for Analysis",
                    options=pollutants,
                    default=['CO(GT)', 'C6H6(GT)', 'NOx(GT)', 'NO2(GT)']
                )
                
                if selected_pollutants:
                    # Time series visualization
                    fig = create_pollutant_timeseries(df_processed, selected_pollutants)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Distribution plots
                    st.subheader("Component Distribution Analysis")
                    col1, col2 = st.columns(2)
                    
                    for i, pollutant in enumerate(selected_pollutants):
                        with col1 if i % 2 == 0 else col2:
                            fig = create_distribution_plot(df_processed, pollutant)
                            st.plotly_chart(fig, use_container_width=True)
                    
                    # Outlier detection
                    st.subheader("Anomalous Molecular Readings")
                    outliers = detect_outliers(df_processed, selected_pollutants)
                    
                    if not outliers.empty:
                        st.dataframe(outliers, use_container_width=True)
                    else:
                        st.info("No significant anomalies detected in the selected components.")
                
                else:
                    st.warning("Please select at least one atmospheric component for analysis.")
            
            with tab3:
                st.subheader("Molecular Interdependence Matrix")
                
                # Correlation heatmap
                fig = create_correlation_heatmap(df_processed)
                st.plotly_chart(fig, use_container_width=True)
                
                # Scatter plot matrix
                st.subheader("Component Relationship Analysis")
                
                x_var = st.selectbox("Select X-axis Component", pollutants, index=0)
                y_var = st.selectbox("Select Y-axis Component", pollutants, index=3)
                color_var = st.selectbox("Color by Component", ['None'] + pollutants, index=0)
                
                if color_var == 'None':
                    color_var = None
                
                fig = create_scatter_plot(df_processed, x_var, y_var, color_var)
                st.plotly_chart(fig, use_container_width=True)
                
                # 3D visualization
                st.subheader("3-Dimensional Component Analysis")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    x_var_3d = st.selectbox("X-axis Component", pollutants, index=0)
                with col2:
                    y_var_3d = st.selectbox("Y-axis Component", pollutants, index=1)
                with col3:
                    z_var_3d = st.selectbox("Z-axis Component", pollutants, index=2)
                
                fig = create_3d_scatter(df_processed, x_var_3d, y_var_3d, z_var_3d)
                st.plotly_chart(fig, use_container_width=True)
            
            with tab4:
                st.subheader("Temporal Atmosphere Analysis")
                
                # Time analysis
                time_analysis = perform_time_analysis(df_processed)
                
                # Hourly patterns
                st.markdown("#### Diurnal Component Patterns")
                fig = px.line(
                    time_analysis['hourly'], 
                    x='Hour', 
                    y=selected_pollutants if selected_pollutants else ['CO(GT)'],
                    title="Hourly Fluctuation Patterns",
                    color_discrete_sequence=list(COLORS.values())
                )
                fig.update_layout(
                    template="plotly_dark",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0.2)',
                    hovermode="x unified"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Daily patterns
                st.markdown("#### Weekly Component Patterns")
                fig = px.bar(
                    time_analysis['daily'], 
                    x='Day', 
                    y=selected_pollutants[0] if selected_pollutants else 'CO(GT)',
                    title=f"Daily {selected_pollutants[0] if selected_pollutants else 'CO(GT)'} Patterns",
                    color='Day',
                    color_discrete_sequence=list(COLORS.values())
                )
                fig.update_layout(
                    template="plotly_dark",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0.2)',
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Monthly patterns if data spans multiple months
                if 'monthly' in time_analysis:
                    st.markdown("#### Monthly Component Patterns")
                    fig = px.line(
                        time_analysis['monthly'], 
                        x='Month', 
                        y=selected_pollutants if selected_pollutants else ['CO(GT)'],
                        title="Monthly Fluctuation Patterns",
                        color_discrete_sequence=list(COLORS.values())
                    )
                    fig.update_layout(
                        template="plotly_dark",
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0.2)',
                        hovermode="x unified"
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            with tab5:
                st.subheader("Advanced Atmospheric Analytics")
                
                # Weather correlation analysis
                st.markdown("#### Weather Influence Matrix")
                weather_vars = ['T', 'RH', 'AH']
                pollutant_vars = [p for p in pollutants if p not in weather_vars]
                
                # Create correlation matrix between weather and pollutants
                weather_corr = df_processed[weather_vars + pollutant_vars].corr().loc[weather_vars, pollutant_vars]
                
                fig = px.imshow(
                    weather_corr,
                    x=pollutant_vars,
                    y=weather_vars,
                    color_continuous_scale=px.colors.diverging.RdBu_r,
                    title="Weather-Pollutant Correlation Matrix",
                    labels=dict(x="Pollutant", y="Weather Variable", color="Correlation")
                )
                fig.update_layout(
                    template="plotly_dark",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0.2)',
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Trend analysis over time
                st.markdown("#### Long-term Trend Analysis")
                
                trend_pollutant = st.selectbox(
                    "Select Component for Trend Analysis",
                    options=pollutants,
                    index=0
                )
                
                # Resample to daily for trend analysis
                df_trend = df_processed.copy()
                df_trend['Date'] = pd.to_datetime(df_trend['Date'] + ' ' + df_trend['Time'])
                df_trend = df_trend.set_index('Date')
                df_trend_daily = df_trend[trend_pollutant].resample('D').mean().reset_index()
                df_trend_daily.columns = ['Date', trend_pollutant]
                
                # Add trend line
                fig = px.scatter(
                    df_trend_daily, 
                    x='Date', 
                    y=trend_pollutant,
                    trendline="lowess",
                    trendline_color_override=COLORS["neon_cyan"],
                    title=f"Long-term {trend_pollutant} Trend Analysis",
                    color_discrete_sequence=[COLORS["neon_purple"]]
                )
                fig.update_layout(
                    template="plotly_dark",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0.2)',
                    xaxis_title="Timeline",
                    yaxis_title=trend_pollutant,
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Data export section
                st.subheader("Data Export Module")
                
                export_options = st.multiselect(
                    "Select Data to Export",
                    options=["Raw Data", "Cleaned Data", "Statistical Summary", "AQI Data", "Outliers"],
                    default=["Cleaned Data"]
                )
                
                if st.button("Generate Export Package"):
                    st.success("Export package generated! Ready for download.")
                    
                    if "Cleaned Data" in export_options:
                        csv = df_processed.to_csv(index=False)
                        st.download_button(
                            label="Download Cleaned Data",
                            data=csv,
                            file_name="air_quality_cleaned.csv",
                            mime="text/csv",
                        )
        
        # Footer with sci-fi theme
        st.markdown(
            """
            <div style='text-align: center; margin-top: 50px; padding: 20px; border-top: 1px solid #00FFFF;'>
                <p style='color: #00BFFF; font-style: italic;'>
                    AirVision 2084 - Quantum Atmospheric Analysis System v1.0
                </p>
                <p style='color: #888; font-size: 0.8em;'>
                    Powered by Biodigital Quantum Processing • Satellite Data Link Active
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

if __name__ == "__main__":
    main()
