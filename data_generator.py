import pandas as pd
import numpy as np
import datetime

def generate_data():
    """Generates synthetic sales and inventory data and saves it to CSV files."""
    print("Generating synthetic data...")

    # --- Configuration ---
    num_products = 5
    num_months = 12
    base_date = datetime.date(2023, 1, 1)

    product_names = [f"Product {chr(65 + i)}" for i in range(num_products)]
    product_ids = [101 + i for i in range(num_products)]
    base_prices = [19.99, 29.99, 9.99, 49.99, 14.99]
    
    # --- Generate Sales Data ---
    all_sales_data = []
    
    for i in range(num_products):
        product_id = product_ids[i]
        product_name = product_names[i]
        base_price = base_prices[i]
        
        # Introduce trend and seasonality
        base_demand = 20 + i * 10
        trend_factor = 1.05 
        
        for month in range(1, num_months + 1):
            # Monthly seasonality (e.g., higher sales in Q4)
            if month in [10, 11, 12]:
                seasonal_factor = 1.8
            elif month in [6, 7, 8]:
                seasonal_factor = 1.2
            else:
                seasonal_factor = 0.9

            # Calculate demand for the month
            monthly_demand = base_demand * seasonal_factor
            
            days_in_month = 31 if month in [1,3,5,7,8,10,12] else 30 if month in [4,6,9,11] else 28
            
            for day in range(1, days_in_month + 1):
                date = base_date + datetime.timedelta(days=(month-1)*30 + day -1) # Approximate date
                
                # Daily noise
                daily_fluctuation = np.random.uniform(0.8, 1.2)
                
                units_sold = int(monthly_demand / days_in_month * daily_fluctuation)
                if units_sold < 0:
                    units_sold = 0

                all_sales_data.append({
                    "date": date,
                    "product_id": product_id,
                    "product_name": product_name,
                    "units_sold": units_sold,
                    "price": base_price
                })
            
            # Apply trend for next month
            base_demand *= trend_factor

    sales_df = pd.DataFrame(all_sales_data)
    sales_df.to_csv("sales.csv", index=False)
    print("-> sales.csv created successfully.")

    # --- Generate Inventory Data ---
    inventory_data = []
    for i in range(num_products):
        inventory_data.append({
            "product_id": product_ids[i],
            "product_name": product_names[i],
            "stock_level": np.random.randint(50, 200) # Random stock level
        })
    
    inventory_df = pd.DataFrame(inventory_data)
    inventory_df.to_csv("inventory.csv", index=False)
    print("-> inventory.csv created successfully.")
    print("Data generation complete.")

if __name__ == "__main__":
    generate_data()
