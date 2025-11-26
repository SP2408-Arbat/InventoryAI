import sys
import os
import google.generativeai as genai

# Add current dir to path
sys.path.append(os.getcwd())

from modules import ai_engine

print("Testing AI Engine with REAL KEY...")

# Mock data
product = "Test Product"
hist = "Sales up 10%"
forecast = "Sales flat"
inv = "Stock low"
api_key = "AIzaSyD-LBQ_VNDWTef8MBFOtOWj68cVDKX2wg0"

try:
    print("Calling generate_explanation...")
    result = ai_engine.generate_explanation(product, hist, forecast, inv, api_key)
    print(f"Result: {result[:100]}...")
except Exception as e:
    print(f"CRITICAL FAILURE: {e}")

print("Test Complete.")
