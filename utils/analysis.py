import pandas as pd

# --- DATA INGESTION ---

def load_data(file_path):
    """
    Handles the initial data import. 
    Using a wrapper function here allows us to swap read_csv 
    for other formats (like Excel or SQL) in the future if needed.
    """
    try:
        raw_df = pd.read_csv(file_path)
        return clean_business_data(raw_df)
    except Exception as e:
        # Returning an empty DF if the file is corrupted prevents the app from crashing
        print(f"Error loading file: {e}")
        return pd.DataFrame()

def clean_business_data(df):
    """
    Standardizes the dataset. 
    In retail data, prices often have symbols (₹, $) or commas.
    This logic strips non-numeric characters to ensure the math doesn't break.
    """
    processed_df = df.copy()
    targets = ["price", "rating", "sales"]
    
    for col in targets:
        if col in processed_df.columns:
            # Strip formatting (like ₹ or commas) using Regex
            if processed_df[col].dtype == 'object':
                processed_df[col] = processed_df[col].str.replace(r'[^\d.]', '', regex=True)
            
            # Convert to float; invalid entries become 0 to keep calculations safe
            processed_df[col] = pd.to_numeric(processed_df[col], errors="coerce").fillna(0)
            
    return processed_df

# --- VALIDATION & AGGREGATION ---

def validate_data_schema(df):
    """Ensures the uploaded CSV has the columns our algorithm expects."""
    required_schema = ["name", "price", "rating", "sales"]
    missing_fields = [field for field in required_schema if field not in df.columns]
    return missing_fields

def calculate_kpi_metrics(df):
    """
    Computes high-level business metrics.
    Note: Revenue is calculated as (Price * Units Sold).
    """
    if df.empty:
        return {
            "Total Products": 0, 
            "Total Sales": 0, 
            "Total Revenue (₹)": 0, 
            "Average Rating": 0
        }
    
    # Using 'int' for currency totals to keep the dashboard view clean (no decimals)
    total_sales = int(df["sales"].sum())
    total_revenue = int((df["price"] * df["sales"]).sum())
    avg_rating = round(df["rating"].mean(), 2)
    
    return {
        "Total Products": len(df),
        "Total Sales": total_sales,
        "Total Revenue (₹)": total_revenue,
        "Average Rating": avg_rating
    }

# --- ANALYTICS LOGIC ---

def get_market_leaders(df, top_n=5):
    """Simply returns the best-selling items regardless of price or rating."""
    return df.sort_values("sales", ascending=False).head(top_n)

def get_performance_ranking(df, top_n=5):
    """
    Advanced Scoring: This is the core logic for identifying 'Balanced' products.
    Weights: 40% Rating (Quality), 40% Sales (Popularity), 20% Price Efficiency.
    This helps find high-quality items that aren't necessarily the most expensive.
    """
    if df.empty: 
        return df
    
    ranked_df = df.copy()
    
    # Reference points for normalization
    global_max_price = ranked_df["price"].max() or 1
    global_max_sales = ranked_df["sales"].max() or 1

    # Weighted calculation
    rating_factor = (ranked_df["rating"] / 5) * 0.4
    sales_factor = (ranked_df["sales"] / global_max_sales) * 0.4
    price_efficiency = (1 - (ranked_df["price"] / global_max_price)) * 0.2

    ranked_df["internal_score"] = rating_factor + sales_factor + price_efficiency
    
    return ranked_df.sort_values("internal_score", ascending=False).head(top_n)