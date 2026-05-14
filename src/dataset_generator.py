import pandas as pd
import numpy as np
import os

def generate_synthetic_data(num_samples=5000):
    """
    Generates synthetic network traffic data for Cybersecurity Threat Detection.
    Features:
    - packet_size: size of the packet in bytes
    - login_attempts: number of login attempts
    - connection_duration: duration of the connection in seconds
    - error_rate: percentage of packets resulting in an error
    - attack_label: 0 for Normal, 1 for Threat
    """
    np.random.seed(42)

    data = {
        'packet_size': [],
        'login_attempts': [],
        'connection_duration': [],
        'error_rate': [],
        'attack_label': []
    }

    for _ in range(num_samples):
        # 80% Normal traffic, 20% Anomalies/Threats
        is_threat = np.random.rand() > 0.8
        
        if not is_threat:
            # Normal Behavior
            data['packet_size'].append(np.random.normal(500, 100)) # Approx 500 bytes
            data['login_attempts'].append(np.random.randint(1, 4)) # 1 to 3 attempts
            data['connection_duration'].append(np.random.normal(5, 2)) # 5 seconds
            data['error_rate'].append(np.random.uniform(0.0, 0.05)) # Max 5% errors
            data['attack_label'].append(0)
        else:
            # Threat Behavior (e.g., DoS or Brute Force)
            attack_type = np.random.choice(['dos', 'brute_force'])
            if attack_type == 'dos':
                data['packet_size'].append(np.random.normal(5000, 1000)) # Large packets
                data['login_attempts'].append(np.random.randint(1, 3))
                data['connection_duration'].append(np.random.normal(120, 30)) # Long connection
                data['error_rate'].append(np.random.uniform(0.5, 0.9)) # High errors
            else: # brute force
                data['packet_size'].append(np.random.normal(200, 50)) # Small rapid packets
                data['login_attempts'].append(np.random.randint(20, 100)) # High login attempts
                data['connection_duration'].append(np.random.normal(20, 5))
                data['error_rate'].append(np.random.uniform(0.8, 1.0)) # Almost all fail
            
            data['attack_label'].append(1)

    df = pd.DataFrame(data)
    
    # Ensure all values are positive
    df['packet_size'] = df['packet_size'].abs()
    df['connection_duration'] = df['connection_duration'].abs()
    
    return df

if __name__ == "__main__":
    print("Generating synthetic network traffic data...")
    df = generate_synthetic_data(10000)
    
    # Ensure 'data' directory exists
    os.makedirs('../data', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    
    filepath = 'data/simulated_network_traffic.csv'
    df.to_csv(filepath, index=False)
    print(f"Dataset successfully created and saved to '{filepath}'.")
    print(df.head())
