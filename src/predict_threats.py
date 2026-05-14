import joblib
import pandas as pd
import numpy as np
import time
import os

def simulate_realtime_threat_detection():
    # Load Model
    model_path = 'models/cybersecurity_rf_model.pkl'
    if not os.path.exists(model_path):
        print(f"Error: Model file {model_path} not found. Please run train_model.py first.")
        return
        
    model = joblib.load(model_path)
    print("Cybersecurity AI Model Loaded successfully.")
    print("Initializing Real-Time Network Monitoring...\n")
    time.sleep(2)
    
    print("-" * 60)
    print(f"{'TIMESTAMP':<20} | {'PACKET SIZE':<15} | {'PREDICTION'}")
    print("-" * 60)
    
    try:
        # Simulate continuous monitoring
        while True:
            # Randomly generate a network packet
            is_malicious = np.random.rand() > 0.85 # 15% chance of being a synthetic attack
            
            if not is_malicious:
                packet_size = abs(np.random.normal(500, 100))
                logins = np.random.randint(1, 4)
                duration = abs(np.random.normal(5, 2))
                errors = np.random.uniform(0.0, 0.05)
            else:
                packet_size = abs(np.random.normal(5000, 1000))
                logins = np.random.randint(20, 100)
                duration = abs(np.random.normal(120, 30))
                errors = np.random.uniform(0.5, 0.9)
                
            features = pd.DataFrame([[packet_size, logins, duration, errors]], 
                                    columns=['packet_size', 'login_attempts', 'connection_duration', 'error_rate'])
                                    
            # AI Prediction
            prediction = model.predict(features)[0]
            
            # Formatted Output
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            size_str = f"{packet_size:.2f} B"
            
            if prediction == 0:
                # Normal
                print(f"[{current_time}] | {size_str:<15} | [NORMAL TRAFFIC]")
            else:
                # Threat
                print(f"\033[91m[{current_time}] | {size_str:<15} | [THREAT DETECTED!] (Possible DoS/Brute Force)\033[0m")
                
            time.sleep(1.5) # Wait 1.5 seconds before next packet
            
    except KeyboardInterrupt:
        print("\nMonitoring Stopped by User.")

if __name__ == "__main__":
    simulate_realtime_threat_detection()
