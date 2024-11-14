import pandas as pd
import json
from datetime import datetime

# Load json data for NIFTY and HDFCBANK
with open('nifty.json') as f:
    nifty_data = json.load(f)

with open('hdfcbank.json') as f:
    hdfc_data = json.load(f)

# Target expiry date (e.g., for next Friday)
target= "2024-11-28"  # specify your expirydate in "YYYY-MM-DD" format


# Helper function to extract fields safely from CE and PE dictionaries
def safe_get(option_data, field):
    return option_data.get(field, None) if isinstance(option_data, dict) else None


# Function to extract and filter data by expiry date
def extract_by_expiry(data, expiry_date):
    # Convert JSON data to a DataFrame
    df = pd.DataFrame(data['records']['data'])

    # Extract relevant columns and filter by expiry date
    filtered_df = pd.DataFrame({
        'Strike Price': df['strikePrice'],
        'Call Open Interest': df['CE'].apply(lambda x: safe_get(x, 'openInterest')),
        'Put Open Interest': df['PE'].apply(lambda x: safe_get(x, 'openInterest')),
        'Call LTP': df['CE'].apply(lambda x: safe_get(x, 'lastPrice')),
        'Put LTP': df['PE'].apply(lambda x: safe_get(x, 'lastPrice')),
        'Call Change in OI': df['CE'].apply(lambda x: safe_get(x, 'changeinOpenInterest')),
        'Put Change in OI': df['PE'].apply(lambda x: safe_get(x, 'changeinOpenInterest')),
        'Call Volume': df['CE'].apply(lambda x: safe_get(x, 'volume')),
        'Put Volume': df['PE'].apply(lambda x: safe_get(x, 'volume')),
        'Call Bid Qty': df['CE'].apply(lambda x: safe_get(x, 'bidQty')),
        'Put Bid Qty': df['PE'].apply(lambda x: safe_get(x, 'bidQty')),
        'Call Bid': df['CE'].apply(lambda x: safe_get(x, 'bid')),
        'Put Bid': df['PE'].apply(lambda x: safe_get(x, 'bid')),
        'Call Ask': df['CE'].apply(lambda x: safe_get(x, 'ask')),
        'Put Ask': df['PE'].apply(lambda x: safe_get(x, 'ask')),
        'Call Ask Qty': df['CE'].apply(lambda x: safe_get(x, 'askQty')),
        'Put Ask Qty': df['PE'].apply(lambda x: safe_get(x, 'askQty')),
        'Expiry Date': pd.to_datetime(df['expiryDate'], errors='coerce').dt.date
    })

    # Filter for the specific expiry date
    filtered_df = filtered_df[filtered_df['Expiry Date'] == pd.to_datetime(expiry_date).date()]
    return filtered_df


# Extract and filter data for NIFTY and HDFCBANK based on the target expiry date
nifty_expiry_data = extract_by_expiry(nifty_data, target)
hdfc_expiry_data = extract_by_expiry(hdfc_data, target)

# Display the extracted data
print("NIFTY Option Chain Data for Expiry Date:", target)
print(nifty_expiry_data)

print("\nHDFCBANK Option Chain Data for Expiry Date:", target)
print(hdfc_expiry_data)
