import pandas as pd
import duckdb
from langchain_core.tools import tool
from pydantic import BaseModel, Field

# --- Pydantic Input Schemas ---
class ForecastInput(BaseModel):
    """Input model for the demand forecast tool."""
    product_name: str = Field(description="The name of the product to forecast, e.g., 'Product A'.")
    days: int = Field(description="The number of future days to forecast demand for, e.g., 7 or 30.")

# --- Sales Query Tool ---
@tool
def query_sales_data(query: str) -> str:
    """
    Executes a SQL query against the 'sales.csv' data file and returns the result.
    The table is named 'sales'.
    Example query: 'SELECT product_name, SUM(units_sold) FROM sales GROUP BY product_name'
    """
    try:
        con = duckdb.connect(database=':memory:')
        # Read the csv file into a virtual table named 'sales'
        con.execute("CREATE TABLE sales AS SELECT * FROM read_csv_auto('sales.csv');")
        result = con.execute(query).fetchdf()
        return result.to_string()
    except Exception as e:
        return f"Error executing query: {e}"

# --- Inventory Tool ---
@tool
def get_inventory_levels() -> str:
    """
    Reads the 'inventory.csv' file and returns the current stock levels for all products.
    """
    try:
        inventory_df = pd.read_csv("inventory.csv")
        return inventory_df.to_string()
    except FileNotFoundError:
        return "Error: inventory.csv not found. Please generate the data first."
    except Exception as e:
        return f"Error reading inventory: {e}"

# --- Forecast Tool (Using Pydantic Schema) ---
@tool(args_schema=ForecastInput)
def generate_demand_forecast(product_name: str, days: int) -> str:
    """
    Generates a statistical demand forecast for a specified product over a specified number of future days.
    Requires the product_name (e.g., 'Product A') and the number of days (e.g., 30).
    """
    try:
        sales_df = pd.read_csv("sales.csv")
        product_sales = sales_df[sales_df['product_name'] == product_name].copy()
        
        if product_sales.empty:
            return f"Error: No sales data found for product '{product_name}'."
        
        # Ensure the date column is datetime objects for tail operations
        product_sales['date'] = pd.to_datetime(product_sales['date'])
        
        # Calculate average daily sales from the most recent 30 days
        # Use simple mean for stability
        avg_daily_sales = product_sales['units_sold'].tail(30).mean()
        
        if pd.isna(avg_daily_sales) or avg_daily_sales == 0:
            # Fallback to overall mean if recent data is bad/empty
            avg_daily_sales = product_sales['units_sold'].mean()

        forecast = avg_daily_sales * days
        
        total_sales_period = product_sales['date'].min().strftime('%Y-%m-%d') + " to " + product_sales['date'].max().strftime('%Y-%m-%d')
        total_units_sold = product_sales['units_sold'].sum()

        explanation = (
            f"Demand Forecast Report for '{product_name}' for the next {days} days:\n"
            f"-----------------------------------------------------------------\n"
            f"1. **Forecasted Demand**: Approximately {int(round(forecast))} units.\n"
            f"2. **Methodology**: The forecast is based on the average daily sales from the most recent 30 days of data.\n"
            f"3. **Historical Context**:\n"
            f"   - Average daily sales used for forecast: {avg_daily_sales:.2f} units/day.\n"
            f"   - Total units sold in the historical period ({total_sales_period}): {total_units_sold} units.\n"
            f"4. **Confidence**: This is a simple statistical forecast. It assumes future sales will mirror the recent past and does not account for external factors like promotions or holidays."
        )
        return explanation

    except FileNotFoundError:
        return "Error: sales.csv not found. Please run data_generator.py first."
    except Exception as e:
        return f"An error occurred in generate_demand_forecast: {e}"