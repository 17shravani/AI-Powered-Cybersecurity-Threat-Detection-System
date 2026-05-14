import streamlit as st
import pandas as pd
import numpy as np
import joblib
import time
import os

# Page configuration
st.set_page_config(page_title="SOC Dashboard", page_icon="🛡️", layout="wide")

# Dashboard Header
st.title("🛡️ AI-Powered Cybersecurity SOC Dashboard")
st.markdown("Real-time network traffic analysis using Random Forest Anomaly Detection.")

# Load Model
@st.cache_resource
def load_model():
    # Make sure the model exists
    model_path = "models/cybersecurity_rf_model.pkl"
    if os.path.exists(model_path):
        return joblib.load(model_path)
    return None

model = load_model()

if model is None:
    st.error("⚠️ Model not found! Please run `python src/train_model.py` first to generate the AI model.")
    st.stop()

# Layout layout
col1, col2 = st.columns([2, 1])

with col2:
    st.subheader("Control Panel")
    simulation_running = st.checkbox("🟢 Start Live Network Capture", value=False)
    st.markdown("---")
    st.markdown("**Threat Alerts:**")
    alert_placeholder = st.empty()

with col1:
    st.subheader("Live Traffic Feed")
    # Table headers
    df_placeholder = st.empty()


# Initialize state
if 'traffic_data' not in st.session_state:
    st.session_state.traffic_data = pd.DataFrame(columns=['Timestamp', 'Packet Size (Bytes)', 'Logins', 'Duration (s)', 'Status'])

# Simulation Loop
if simulation_running:
    while simulation_running:
        # Generate fake network packet
        is_malicious = np.random.rand() > 0.85
        if not is_malicious:
            packet_size, logins, duration, error = abs(np.random.normal(500, 100)), np.random.randint(1, 4), abs(np.random.normal(5, 2)), np.random.uniform(0.0, 0.05)
        else:
            packet_size, logins, duration, error = abs(np.random.normal(5000, 1000)), np.random.randint(20, 100), abs(np.random.normal(120, 30)), np.random.uniform(0.5, 0.9)
            
        features = pd.DataFrame([[packet_size, logins, duration, error]], columns=['packet_size', 'login_attempts', 'connection_duration', 'error_rate'])
        
        # Predict
        prediction = model.predict(features)[0]
        
        timestamp = time.strftime("%H:%M:%S")
        size = f"{packet_size:.2f}"
            
        if prediction == 0:
            status = "✅ NORMAL"
        else:
            status = "🚨 THREAT DETECTED"
            # Show alert
            with col2:
                alert_placeholder.error(f"Potential DoS / Brute Force attempt blocked at {timestamp}!")
                
        # Add to dataframe
        new_row = pd.DataFrame([[timestamp, size, logins, f"{duration:.2f}", status]], columns=st.session_state.traffic_data.columns)
        
        # Keep only the last 15 rows for UI cleaness
        st.session_state.traffic_data = pd.concat([new_row, st.session_state.traffic_data]).head(15).reset_index(drop=True)
        
        # Update Table safely checking status for styling
        def highlight_threats(val):
            color = 'red' if 'THREAT' in val else 'green' if 'NORMAL' in val else 'white'
            return f'color: {color}; font-weight: bold'
            
        styled_df = st.session_state.traffic_data.style.map(highlight_threats, subset=['Status'])
        
        # Render Table
        with col1:
            df_placeholder.dataframe(styled_df, use_container_width=True, hide_index=True)
            
        time.sleep(1.0) # Speed of new packets
else:
    # Render empty or paused state
    with col1:
        if not st.session_state.traffic_data.empty:
            df_placeholder.dataframe(st.session_state.traffic_data, use_container_width=True, hide_index=True)
        else:
            st.info("System Idle. Check 'Start Live Network Capture' to begin.")
