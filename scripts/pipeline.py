import pandas as pd
import numpy as np
import os

def run_pipeline():
    orders_path = os.path.join('data', 'da_b2b_orders.csv')
    products_path = os.path.join('data', 'da_product_catalogue.csv')
    customers_path = os.path.join('data', 'da_customer_profiles.csv')
    
    # 1. Ingestion
    print("Ingesting data packs...")
    orders = pd.read_csv(orders_path)
    products = pd.read_csv(products_path)
    customers = pd.read_csv(customers_path)
    
    # 2. Cleaning & Standardization
    orders['order_date'] = pd.to_datetime(orders['order_date'], errors='coerce')
    
    # 3. Merging (buyer_id matches Customer_ID)
    print("Processing pipeline transformations...")
    df = orders.merge(customers, left_on='buyer_id', right_on='Customer_ID', how='left')
    
    # 4. Baseline Metrics Computation
    total_revenue_inr = df['total_value_inr'].sum()
    total_orders = len(df)
    avg_order_value = df['total_value_inr'].mean()
    
    print("\n--- TRADESIGHT BASELINE METRICS ---")
    print(f"Total Export Orders Processed : {total_orders}")
    print(f"Total Export Revenue (INR)    : ₹{total_revenue_inr:,.2f}")
    print(f"Average Order Value (INR)     : ₹{avg_order_value:,.2f}")
    print("-----------------------------------")
    
    # Save processed output
    os.makedirs('outputs', exist_ok=True)
    df.to_csv('outputs/processed_export_metrics.csv', index=False)
    print("Processed metrics saved to outputs/processed_export_metrics.csv")

if __name__ == "__main__":
    run_pipeline()
    