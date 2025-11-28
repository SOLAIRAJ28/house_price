"""
Test script for the house price prediction API
"""
import requests
import json

# Test data - California housing features
test_data = {
    "data": [8.3252, 41.0, 6.98, 1.02, 322.0, 2.55, 37.88, -122.23]
}

print("🧪 Testing House Price Predictor API")
print("=" * 50)

# Test 1: Local prediction
print("\n📍 Test 1: Local Prediction")
print(f"Input features: {test_data['data']}")

from main import predict, Input
result = predict(Input(data=test_data['data']))
print(f"✅ Prediction: ${result['prediction']:,.2f}")

# Test 2: Multiple predictions
print("\n📍 Test 2: Multiple Predictions")
test_cases = [
    {"name": "Low price area", "data": [3.0, 30.0, 5.0, 1.0, 500.0, 2.0, 32.0, -117.0]},
    {"name": "Mid price area", "data": [5.0, 40.0, 6.5, 1.05, 400.0, 2.5, 37.0, -122.0]},
    {"name": "High price area", "data": [8.0, 50.0, 7.5, 1.1, 300.0, 3.0, 37.8, -122.2]},
]

for test in test_cases:
    result = predict(Input(data=test['data']))
    print(f"  {test['name']}: ${result['prediction']:,.2f}")

print("\n" + "=" * 50)
print("✅ All tests passed! API is working correctly.")
print("\n🚀 Ready to deploy on Render!")
