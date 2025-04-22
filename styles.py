import streamlit as st

# Define color scheme for futuristic sci-fi theme
COLORS = {
    "dark_bg": "#0E1117",
    "dark_blue": "#051C2C",
    "neon_blue": "#007BFF",
    "neon_cyan": "#00FFFF",  # Tron-like cyan
    "neon_green": "#39FF14",
    "neon_yellow": "#FFFF00",
    "neon_pink": "#FF10F0",
    "neon_purple": "#9D00FF",
    "text_light": "#F5F5F5",
    "grid_color": "rgba(0, 255, 255, 0.1)"
}

def set_sci_fi_style():
    """
    Set the sci-fi style for the Streamlit app
    """
    # Apply custom CSS for sci-fi styling
    st.markdown(
        """
        <style>
        /* Base theme overrides */
        .stApp {
            font-family: 'Orbitron', sans-serif;
        }
        
        /* Header styling */
        h1, h2, h3 {
            font-family: 'Orbitron', sans-serif;
            color: #00FFFF !important;
            text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
            letter-spacing: 1px;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background-color: rgba(5, 28, 44, 0.8);
        }
        
        /* Button styling */
        .stButton button {
            background: linear-gradient(45deg, #051C2C, #0E1117) !important;
            color: #00FFFF !important;
            border: 1px solid #00FFFF !important;
            border-radius: 5px !important;
            box-shadow: 0 0 10px rgba(0, 255, 255, 0.2) !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton button:hover {
            box-shadow: 0 0 15px rgba(0, 255, 255, 0.5) !important;
            transform: translateY(-2px) !important;
        }
        
        /* Radio button, checkbox, and selectbox styling */
        .stRadio, .stCheckbox, .stSelectbox {
            color: #F5F5F5 !important;
        }
        
        /* Expander styling */
        .streamlit-expanderHeader {
            background-color: rgba(5, 28, 44, 0.8) !important;
            color: #00FFFF !important;
            border: none !important;
            border-radius: 5px !important;
        }
        
        /* DataFrame styling */
        .stDataFrame {
            border: 1px solid #00FFFF !important;
            border-radius: 5px !important;
            box-shadow: 0 0 10px rgba(0, 255, 255, 0.2) !important;
        }
        
        /* Text input styling */
        .stTextInput input, .stNumberInput input {
            background-color: rgba(5, 28, 44, 0.8) !important;
            color: #F5F5F5 !important;
            border: 1px solid #00FFFF !important;
            border-radius: 5px !important;
        }
        
        /* Slider styling */
        .stSlider {
            color: #00FFFF !important;
        }
        
        /* Metric styling */
        .stMetric {
            background-color: rgba(5, 28, 44, 0.8) !important;
            border: 1px solid #00FFFF !important;
            border-radius: 5px !important;
            box-shadow: 0 0 10px rgba(0, 255, 255, 0.2) !important;
        }
        
        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: rgba(5, 28, 44, 0.8) !important;
            color: #F5F5F5 !important;
            border-radius: 5px 5px 0 0 !important;
            border: 1px solid #00FFFF !important;
            border-bottom: none !important;
            padding: 10px 20px !important;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: rgba(0, 255, 255, 0.1) !important;
            color: #00FFFF !important;
            box-shadow: 0 0 10px rgba(0, 255, 255, 0.2) !important;
        }
        
        /* Tooltip styling */
        [data-tooltip]:hover:after {
            background-color: rgba(5, 28, 44, 0.9) !important;
            color: #00FFFF !important;
            border: 1px solid #00FFFF !important;
            box-shadow: 0 0 10px rgba(0, 255, 255, 0.5) !important;
        }
        
        /* Container styling */
        .stContainer {
            border-radius: 10px !important;
            backdrop-filter: blur(10px) !important;
        }
        
        /* Add custom fonts */
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700&display=swap');
        
        </style>
        """,
        unsafe_allow_html=True,
    )

def add_logo(image_url):
    """
    Add a logo to the top of the sidebar
    
    Parameters:
    image_url (str): URL of the logo image
    """
    st.sidebar.markdown(
        f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <img src="{image_url}" width="150">
        </div>
        """,
        unsafe_allow_html=True
    )

def add_glowing_effect(st_element, color="#00FFFF"):
    """
    Add a glowing effect to a Streamlit element using HTML/CSS
    
    Parameters:
    st_element: Streamlit element
    color (str): Color for the glow effect
    """
    # This is just a placeholder function since we can't directly modify 
    # Streamlit elements after they're created.
    # In a real application, we would apply this in our custom CSS
    pass
