import joblib
import pandas as pd

# Load the model
model = joblib.load('engine_model.pkl')

# Demo prediction with sample sensor data
demo_data = {
    'engine_rpm': 1200,
    'lub_oil_pressure': 4.5,
    'fuel_pressure': 15.0,
    'coolant_pressure': 2.5,
    'lub_oil_temp': 85.0,
    'coolant_temp': 85.0
}

input_df = pd.DataFrame([demo_data])
probabilities = model.predict_proba(input_df)
failure_probability = probabilities[0, 1]

if failure_probability < 0.3:
    health = 'GOOD'
elif failure_probability <= 0.7:
    health = 'WARNING'
else:
    health = 'CRITICAL'

print('Demo Prediction Results:')
print(f'Input Data: {demo_data}')
print(f'Failure Probability: {failure_probability:.4f}')
print(f'Engine Health Status: {health}')
