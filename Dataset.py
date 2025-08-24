import pandas as pd
import numpy as np

# Set seed for reproducibility
np.random.seed(42)

# Number of rows
n_rows = 50000

# Possible values
device_types = ['sensor', 'router', 'camera', 'thermostat', 'gateway']
manufacturers = ['Acme', 'Globex', 'Umbrella', 'Initech', 'Soylent']
firmware_versions = ['1.0', '1.1', '2.0', '2.1', '3.0']
locations = ['North America', 'Europe', 'Asia', 'South America', 'Africa']
usage_patterns = ['low', 'medium', 'high']
operating_modes = ['normal', 'test', 'power_saving']

# Generate synthetic data
df = pd.DataFrame({
    'device_id': [f'DEV{100000+i}' for i in range(n_rows)],
    'device_type': np.random.choice(device_types, n_rows),
    'manufacturer': np.random.choice(manufacturers, n_rows),
    'firmware_version': np.random.choice(firmware_versions, n_rows),
    'location': np.random.choice(locations, n_rows),
    'uptime_days': np.random.randint(1, 1000, n_rows),
    'device_age_days': np.random.randint(30, 2000, n_rows),
    'temperature_C': np.round(np.random.normal(45, 10, n_rows), 2),
    'cpu_usage_percent': np.round(np.random.uniform(10, 100, n_rows), 2),
    'memory_usage_percent': np.round(np.random.uniform(10, 100, n_rows), 2),
    'disk_usage_percent': np.round(np.random.uniform(10, 100, n_rows), 2),
    'network_latency_ms': np.round(np.random.exponential(scale=50, size=n_rows), 2),
    'error_count': np.random.poisson(2, n_rows),
    'sensor_faults_detected': np.random.poisson(1, n_rows),
    'restarts_last_30_days': np.random.poisson(0.5, n_rows),
    'last_maintenance_days_ago': np.random.randint(0, 365, n_rows),
    'firmware_update_pending': np.random.choice([0, 1], n_rows, p=[0.85, 0.15]),
    'security_alerts_last_30_days': np.random.poisson(0.3, n_rows),
    'is_connected': np.random.choice([0, 1], n_rows, p=[0.1, 0.9]),
    'battery_health_percent': np.round(np.random.uniform(60, 100, n_rows), 2),
    'usage_pattern': np.random.choice(usage_patterns, n_rows),
    'maintenance_priority': np.random.randint(1, 6, n_rows),
    'operating_mode': np.random.choice(operating_modes, n_rows)
})

# Failure logic: Weighted random based on some conditions
def generate_failure(row):
    score = 0
    if row['temperature_C'] > 70: score += 1
    if row['cpu_usage_percent'] > 90: score += 1
    if row['error_count'] > 5: score += 1
    if row['sensor_faults_detected'] > 2: score += 1
    if row['firmware_update_pending'] == 1: score += 0.5
    if row['battery_health_percent'] < 70: score += 1
    if row['device_age_days'] > 1500: score += 1
    if row['restarts_last_30_days'] > 3: score += 1
    # Add some randomness
    prob = min(score / 6.0, 1.0)
    return np.random.rand() < prob * 0.7  # scale overall failure rate


# Randomly introduce NaN values (to simulate dirty data)
df.loc[df.sample(frac=0.01).index, "temperature_C"] = np.nan
df.loc[df.sample(frac=0.01).index, "manufacturer"] = None


df['failure'] = df.apply(generate_failure, axis=1).astype(int)

# Save to CSV
df.to_csv('device_failure_dataset.csv', index=False)

print("✅ Dataset saved as 'device_failure_dataset.csv'")