import pandas as pd
import os

def run_deep_dive():
    # Load processed metrics or raw data
    input_path = os.path.join('outputs', 'processed_export_metrics.csv')
    if not os.path.exists(input_path):
        input_path = os.path.join('outputs', 'processed_export_metrics.csv')
    
    df = pd.read_csv(input_path)
    
    print("--- TRADESIGHT MILESTONE 3: DEEP-DIVE ANALYSIS ---\n")
    
    # 1. Regional Export Performance (Revenue by Country)
    if 'destination_country' in df.columns:
        country_perf = df.groupby('destination_country')['total_value_inr'].agg(['sum', 'count']).reset_index()
        country_perf.columns = ['Destination_Country', 'Total_Revenue_INR', 'Order_Count']
        country_perf = country_perf.sort_values(by='Total_Revenue_INR', ascending=False)
        print("1. Top Export Markets (Destination Country):")
        print(country_perf.head(5).to_string(index=False))
        print("-" * 50)
    
    # 2. Client Concentration (Top Buyers)
    if 'company_name' in df.columns or 'buyer_id' in df.columns:
        buyer_col = 'company_name' if 'company_name' in df.columns else 'buyer_id'
        client_perf = df.groupby(buyer_col)['total_value_inr'].sum().reset_index()
        client_perf = client_perf.sort_values(by='total_value_inr', ascending=False)
        print("2. Top B2B Clients by Revenue:")
        print(client_perf.head(5).to_string(index=False))
        print("-" * 50)
        
    # 3. Payment Terms Risk Segmentation
    if 'payment_terms' in df.columns:
        payment_summary = df.groupby('payment_terms')['total_value_inr'].agg(['sum', 'count']).reset_index()
        payment_summary.columns = ['Payment_Terms', 'Total_Revenue_INR', 'Order_Count']
        print("3. Payment Terms Breakdown:")
        print(payment_summary.to_string(index=False))
        print("-" * 50)
        
    # Save deep dive outputs
    os.makedirs('outputs', exist_ok=True)
    if 'destination_country' in df.columns:
        country_perf.to_csv('outputs/revenue_by_country.csv', index=False)
    print("Deep-dive analytical tables saved successfully to outputs/")

if __name__ == "__main__":
    run_deep_dive()
    