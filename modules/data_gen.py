import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

def generate_data():
    # Setup
    np.random.seed(42)
    random.seed(42)
    
    products = [
        {"id": "P001", "name": "Wireless Headphones", "category": "Electronics", "base_price": 150},
        {"id": "P002", "name": "Smart Watch", "category": "Electronics", "base_price": 250},
        {"id": "P003", "name": "Running Shoes", "category": "Apparel", "base_price": 120},
        {"id": "P004", "name": "Yoga Mat", "category": "Fitness", "base_price": 40},
        {"id": "P005", "name": "Coffee Maker", "category": "Home", "base_price": 80},
    ]
    
    # 1. Generate Sales History (Last 365 days)
    sales_data = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    for product in products:
        # Create a seasonal trend (sine wave) + random noise
        # Different phase for different products to make it interesting
        phase = random.uniform(0, 2*np.pi)
        seasonality = 10 * np.sin(np.linspace(0, 4*np.pi, len(dates)) + phase)
        
        # Base demand
        base_demand = random.randint(20, 50)
        
        for i, date in enumerate(dates):
            # Weekend spike
            is_weekend = date.weekday() >= 5
            weekend_boost = 1.2 if is_weekend else 1.0
            
            # Holiday spike (simple approximation)
            is_holiday = False
            if date.month == 12 and date.day > 20: # Christmas season
                is_holiday = True
            
            holiday_boost = 1.5 if is_holiday else 1.0
            
            # Price fluctuation
            price_variance = random.uniform(0.9, 1.1)
            price = round(product["base_price"] * price_variance, 2)
            
            # Promotion
            is_promo = random.random() < 0.05 # 5% chance of promo
            promo_boost = 1.4 if is_promo else 1.0
            
            # Calculate units sold
            demand = (base_demand + seasonality[i]) * weekend_boost * holiday_boost * promo_boost
            units_sold = max(0, int(np.random.normal(demand, 5))) # Add noise
            
            sales_data.append({
                "Date": date.strftime("%Y-%m-%d"),
                "ProductID": product["id"],
                "ProductName": product["name"],
                "Category": product["category"],
                "UnitsSold": units_sold,
                "UnitPrice": price,
                "IsPromotion": is_promo,
                "IsHoliday": is_holiday
            })
            
    df_sales = pd.DataFrame(sales_data)
    
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    df_sales.to_csv("data/sales_history.csv", index=False)
    print(f"Generated sales_history.csv with {len(df_sales)} records.")

    # 2. Generate Inventory Data
    inventory_data = []
    for product in products:
        current_stock = random.randint(50, 200)
        reorder_level = random.randint(20, 50)
        lead_time = random.randint(3, 14) # Days
        
        inventory_data.append({
            "ProductID": product["id"],
            "ProductName": product["name"],
            "CurrentStock": current_stock,
            "ReorderLevel": reorder_level,
            "LeadTimeDays": lead_time,
            "Supplier": f"Supplier_{random.choice(['A', 'B', 'C'])}"
        })
        
    df_inventory = pd.DataFrame(inventory_data)
    df_inventory.to_csv("data/inventory.csv", index=False)
    print(f"Generated inventory.csv with {len(df_inventory)} records.")

if __name__ == "__main__":
    generate_data()
