import streamlit as st

def load_css():
    st.markdown("""
        <style>
        /* Modern Dark Theme Tweaks */
        .stApp {
            background-color: #0e1117;
            color: #fafafa;
        }
        
        /* Card Style */
        .metric-card {
            background-color: #262730;
            border: 1px solid #464b5d;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
        }
        
        .metric-value {
            font-size: 2rem;
            font-weight: bold;
            color: #4CAF50;
        }
        
        .metric-label {
            font-size: 1rem;
            color: #b0b0b0;
        }
        
        /* Chat/Explanation Box */
        .explanation-box {
            background-color: #1e2130;
            border-left: 5px solid #7c4dff;
            padding: 15px;
            border-radius: 5px;
            margin-top: 20px;
        }
        
        </style>
    """, unsafe_allow_html=True)

def metric_card(label, value, prefix=""):
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{prefix}{value}</div>
        </div>
    """, unsafe_allow_html=True)
