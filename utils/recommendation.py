import pandas as pd

def run_recommendation_engine(inventory_df, target_budget, limit=5):
    """
    Core engine that identifies top-performing products within a specific 
    budget using a weighted scoring model.
    """
    
    # 1. PRE-PROCESSING & DATA INTEGRITY
    # Convert data types here to ensure the math doesn't fail due to string inputs
    inventory_df["price"] = pd.to_numeric(inventory_df["price"], errors='coerce')
    inventory_df["sales"] = pd.to_numeric(inventory_df["sales"], errors='coerce')
    inventory_df["rating"] = pd.to_numeric(inventory_df["rating"], errors='coerce')
    
    # 2. BUDGET FILTERING
    # Creating a copy to avoid 'SettingWithCopyWarning' during score generation
    candidates = inventory_df[inventory_df["price"] <= target_budget].copy()

    if candidates.empty:
        return pd.DataFrame()

    # 3. NORMALIZATION BASICS
    # We use max values from the filtered set to calculate relative performance
    max_observed_sales = candidates["sales"].max() if candidates["sales"].max() > 0 else 1
    max_observed_price = candidates["price"].max() if candidates["price"].max() > 0 else 1

    # 4. WEIGHTED SCORING MODEL
    # 40% Sentiment (Rating), 40% Volume (Sales), 20% Cost Efficiency
    # Price is inverted (1 - x) because a lower price is a 'better' efficiency score
    sentiment_score = candidates["rating"] / 5
    volume_score = candidates["sales"] / max_observed_sales
    efficiency_score = 1 - (candidates["price"] / max_observed_price)

    candidates["internal_score"] = (
        0.4 * sentiment_score + 
        0.4 * volume_score + 
        0.2 * efficiency_score
    )

    # Sort candidates by the highest score before generating labels
    candidates = candidates.sort_values("internal_score", ascending=False).reset_index(drop=True)

    # 5. STRATEGIC REASONING LOGIC
    def _map_business_logic(row, reference_data):
        """Internal helper to assign strategic badges based on data distribution."""
        labels = []
        
        # Priority 1: Ranking status
        if row.name == 0: 
            labels.append("👑 Best Overall")
        elif row.name == 1: 
            labels.append("🥈 Top Alternative")
            
        # Priority 2: Statistical outliers (Top 25% performers)
        sales_q3 = reference_data["sales"].quantile(0.75)
        price_q1 = reference_data["price"].quantile(0.25)
        price_q3 = reference_data["price"].quantile(0.75)

        # Sales Leadership
        if row["sales"] >= sales_q3 and "👑 Best Overall" not in labels:
            labels.append("🔥 Market Leader")
            
        # Quality Tiers
        if row["rating"] == 5.0:
            labels.append("💎 Flawless Quality")
        elif row["rating"] >= 4.7:
            labels.append("⭐ Premium Rated")
            
        # Pricing Segments
        if row["price"] <= price_q1:
            labels.append("💰 Best Value")
        elif row["price"] >= price_q3:
            labels.append("✨ Luxury Pick")
            
        # Safety Check
        if not labels:
            return "✅ Verified Performer"
            
        # Join top 2 insights for dashboard clarity
        return " | ".join(labels[:2])

    # Applying labels based on the final sorted list
    candidates["reason"] = candidates.apply(lambda x: _map_business_logic(x, candidates), axis=1)
    
    # Selecting output columns for the UI
    final_cols = ["name", "price", "sales", "rating", "reason"]
    return candidates[final_cols].head(limit)