import sys
import os

# Add current dir to path so we can import modules
sys.path.append(os.getcwd())

from modules import ai_engine

print("Testing AI Engine...")

# Mock data
product = "Test Product"
hist = "Sales up 10%"
forecast = "Sales flat"
inv = "Stock low"
api_key = "dummy_key" # This will fail auth, but verify code path

try:
    print("Calling generate_explanation...")
    # We expect this to fail with an API error (400/403) not a NameError or ImportError
    result = ai_engine.generate_explanation(product, hist, forecast, inv, api_key)
    print(f"Result: {result}")
except Exception as e:
    print(f"CRITICAL FAILURE: {e}")

print("Test Complete.")
