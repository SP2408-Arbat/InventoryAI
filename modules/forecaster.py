import pandas as pd
import numpy as np

def calculate_forecast(df_sales, product_id, forecast_days=30):
    """
    Generates a simple statistical forecast using Exponential Smoothing.
    """
    # Filter for product
    product_sales = df_sales[df_sales['ProductID'] == product_id].copy()
    product_sales['Date'] = pd.to_datetime(product_sales['Date'])
    product_sales = product_sales.sort_values('Date')
    
    # Set index to Date
    product_sales.set_index('Date', inplace=True)
    
    # Resample to daily to ensure no gaps (fill with 0)
    daily_sales = product_sales['UnitsSold'].resample('D').sum().fillna(0)
    
    # Simple Exponential Smoothing
    alpha = 0.2
    forecast = [daily_sales.iloc[0]]
    for i in range(1, len(daily_sales)):
        forecast.append(alpha * daily_sales.iloc[i-1] + (1 - alpha) * forecast[-1])
        
    # Future forecast
    last_val = forecast[-1]
    future_forecast = []
    for _ in range(forecast_days):
        future_forecast.append(last_val) # Naive forecast for simplicity in this demo
        
    # Create DataFrame for results
    history_df = pd.DataFrame({
        'Date': daily_sales.index,
        'Actual': daily_sales.values,
        'Smoothed': forecast
    })
    
    last_date = daily_sales.index[-1]
    future_dates = [last_date + pd.Timedelta(days=i+1) for i in range(forecast_days)]
    
    forecast_df = pd.DataFrame({
        'Date': future_dates,
        'Forecast': future_forecast
    })
    
    return history_df, forecast_df

def get_product_stats(df_sales, product_id):
    product_sales = df_sales[df_sales['ProductID'] == product_id]
    total_sold = product_sales['UnitsSold'].sum()
    avg_price = product_sales['UnitPrice'].mean()
    
    return {
        "total_sold": total_sold,
        "avg_price": avg_price,
        "last_30_days_sales": product_sales.tail(30)['UnitsSold'].sum()
    }
