import streamlit as st
import pandas as pd
import sqlite3
import joblib
import os
from PIL import Image

# Page Configuration
st.set_page_config(
    page_title="Global Shark Attack Insights",
    page_icon="🦈",
    layout="wide"
)

# CSS for a premium look
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #0077b6;
        color: white;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    .stMetric {
        background-color: #ffffff; /* Card background white hi rehne dein */
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        color: #000000 !important; /* Yeh line text ko black kar degi */
    }
    /* Metric label aur value dono ko black karne ke liye */
    [data-testid="stMetricValue"] {
        color: #0077b6 !important; /* Numbers ko blue kar dega */
    }
    [data-testid="stMetricLabel"] {
        color: #333333 !important; /* Labels ko dark grey kar dega */
    }

    </style>
    """, unsafe_allow_html=True)

# Load Data and Models
@st.cache_resource
def load_resources():
    conn = sqlite3.connect('master_sharks.db')
    df = pd.read_sql('SELECT * FROM sharks', conn)
    conn.close()
    
    model = joblib.load('fatality_predictor.pkl')
    encoder = joblib.load('activity_encoder.pkl')
    
    return df, model, encoder

try:
    df, model, encoder = load_resources()
except Exception as e:
    st.error(f"Error loading resources: {e}")
    st.stop()

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Data Insights", "Fatality Predictor"])

# --- Home Page ---
if page == "Home":
    st.title("🦈 Global Shark Attack Insights & Predictor")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Welcome!")
        st.write("""
        Shark attacks are rare but fascinating events that happen in our oceans. 
        This application uses real-world data from the Global Shark Attack File to help us 
        understand where, when, and how these incidents occur.
        
        Our goal is to use data science to promote ocean safety and debunk myths about 
        these magnificent creatures. By looking at patterns, we can learn to share the water 
        more safely with sharks.
        """)
        
        st.info("**Did you know?** You are more likely to be struck by lightning than to be attacked by a shark!")

    with col2:
        # Check if we have an image to show
        img_path = 'outputs/wordcloud_species.png'
        if os.path.exists(img_path):
            st.image(img_path, caption="Commonly involved Shark Species", use_container_width=True)

    st.divider()
    
    # Quick Stats
    st.subheader("At a Glance")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Recorded Attacks", f"{len(df):,}")
    c2.metric("Total Countries", f"{df['Country'].nunique()}")
    c3.metric("Fatal Incidents", f"{len(df[df['is_fatal'] == 1]):,}")
    c4.metric("Non-Fatal Incidents", f"{len(df[df['is_fatal'] == 0]):,}")

# --- Data Insights Page ---
elif page == "Data Insights":
    st.title("📊 Ocean Trends")
    st.write("Visual evidence generated from over 6,000 recorded shark attack cases.")
    
    tab1, tab2 = st.tabs(["Global Heatmap", "Attack Analysis"])
    
    with tab1:
        st.subheader("Where and When? (Monthly Heatmap)")
        heatmap_path = 'outputs/heatmap_attacks.png'
        if os.path.exists(heatmap_path):
            st.image(heatmap_path, use_container_width=True)
            st.write("""
            This heatmap shows the number of attacks per month for the most active countries. 
            Darker colors indicate higher frequency. Notice how patterns differ between 
            the Northern and Southern Hemispheres!
            """)
        else:
            st.warning("Heatmap image not found. Please run the visualization script.")

    with tab2:
        st.subheader("Top Activities During Attacks")
        activity_counts = df['Activity'].value_counts().nlargest(10)
        st.bar_chart(activity_counts)
        st.write("Activities like Surfing and Swimming are most common in reports, reflecting where humans interact with sharks most frequently.")

# --- Fatality Predictor Page ---
elif page == "Fatality Predictor":
    st.title("🔮 Safety Predictor")
    st.write("""
    Based on historical patterns, our Random Forest AI can estimate the probability 
    of a fatality given specific conditions. 
    *Note: This is for educational purposes only.*
    """)
    
    with st.container():
        st.subheader("Input Conditions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Sort activities for the dropdown
            sorted_activities = sorted(df['Activity'].unique().tolist())
            user_activity = st.selectbox("What was the person doing?", sorted_activities, index=sorted_activities.index("Surfing") if "Surfing" in sorted_activities else 0)
            
        with col2:
            months = ["Unknown", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
            user_month_str = st.selectbox("Which month did it happen?", months, index=1)
            user_month = months.index(user_month_str) - 1 # Adjusted for 0-12 scale used in training (where 0 is unknown)
            if user_month < 0: user_month = 0

    if st.button("Calculate Outcome Probability"):
        try:
            # Encode inputs
            # Handle activity not in encoder (though here we use dropdown from data)
            try:
                activity_enc = encoder.transform([user_activity])[0]
            except:
                activity_enc = 0 # Default/Unknown
            
            # Predict
            features = pd.DataFrame([[activity_enc, user_month]], columns=['Activity_Encoded', 'Month'])
            prob = model.predict_proba(features)[0]
            prediction = model.predict(features)[0]
            
            st.divider()
            
            if prediction == 1:
                st.warning(f"### Outcome Prediction: Critical / Fatal")
            else:
                st.success(f"### Outcome Prediction: Non-Fatal / Recovered")
                
            st.write(f"Confidence Level: **{max(prob)*100:.2f}%**")
            
            # Helpful advice
            if prediction == 1:
                st.markdown("""
                **Safety Tip:** In areas known for shark activity, avoid swimming during dawn or dusk, 
                and always stay in groups.
                """)
            else:
                st.markdown("""
                **Did you know?** Many interactions with sharks are curiosity-based or accidental, 
                resulting in non-fatal injuries.
                """)
                
        except Exception as e:
            st.error(f"Prediction Error: {e}")

# --- Safety Quiz Page ---
elif page == "Safety Quiz":
    st.title("🧠 Test Your Shark Knowledge!")
    q1 = st.radio("Sharks are attracted to human blood more than anything else?", ["True", "False"])
    if st.button("Check Answer"):
        if q1 == "False":
            st.success("Correct! Sharks are actually more interested in fish and seals.")
        else:
            st.error("Try again! Most sharks don't actually like the taste of humans.")

# --- Sidebar info ---
st.sidebar.divider()
st.sidebar.info("Data Source: Global Shark Attack File (GSAF)")