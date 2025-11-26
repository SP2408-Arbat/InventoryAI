import os
import google.generativeai as genai
import hashlib
import json
import streamlit as st
import pandas as pd
from datetime import datetime

# Simple JSON Cache Implementation
CACHE_FILE = "cache_db.json"

def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_cache(cache_data):
    try:
        with open(CACHE_FILE, "w") as f:
            json.dump(cache_data, f, indent=4)
    except Exception as e:
        print(f"Error saving cache: {e}")

def configure_gemini(api_key):
    genai.configure(api_key=api_key)

def get_cache_key(context_data):
    """Creates a deterministic hash of the input context."""
    return hashlib.md5(json.dumps(context_data, sort_keys=True).encode()).hexdigest()

def generate_explanation(product_name, history_summary, forecast_summary, inventory_status, api_key):
    """
    Generates an explanation for the forecast and inventory recommendations.
    Checks cache first.
    """
    if not api_key:
        return "⚠️ Please provide a Gemini API Key to generate insights."

    configure_gemini(api_key)
    
    # Construct Context
    context = {
        "product": product_name,
        "history": history_summary,
        "forecast": forecast_summary,
        "inventory": inventory_status
    }
    
    cache_key = get_cache_key(context)
    cache = load_cache()
    
    # 1. Check Cache
    if cache_key in cache:
        print("Cache Hit!")
        return cache[cache_key]['explanation'] + "\n\n*(Cached Insight)*"

    # 2. Call Gemini
    # Using gemini-2.5-flash as verified available
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""
    You are an expert Retail Demand Planner.
    
    Product: {product_name}
    
    Data Context:
    - Recent Sales Trend: {history_summary}
    - Forecasted Demand (Next 30 days): {forecast_summary}
    - Current Inventory: {inventory_status}
    
    Task:
    1. Explain the forecast. Why is it trending this way? (Assume seasonality/trends based on the data).
    2. Provide actionable inventory recommendations. Should we reorder? Run a promo?
    
    Keep it concise, professional, and actionable. Use bullet points.
    """
    
    try:
        response = model.generate_content(prompt)
        explanation = response.text
        
        # 3. Save to Cache
        cache[cache_key] = {
            "explanation": explanation,
            "product": product_name,
            "timestamp": str(datetime.now())
        }
        save_cache(cache)
        
        return explanation
    except Exception as e:
        return f"Error generating explanation: {e}"

def get_embedding_function():
    # Placeholder if we wanted to use semantic search
    return None
