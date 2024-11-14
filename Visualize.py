import pandas as pd
import json
import matplotlib.pyplot as plt
from datetime import datetime

# Load JSON data for NIFTY and HDFCBANK
with open('nifty.json') as f:
    nifty_data = json.load(f)

with open('hdfcbank.json') as f:
    hdfc_data = json.load(f)

# Target expiry date (e.g., for next Friday)
target = "2024-11-28"  # Specify your expiry date in "YYYY-MM-DD" format


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
        'Call IV': df['CE'].apply(lambda x: safe_get(x, 'impliedVolatility')),
        'Put IV': df['PE'].apply(lambda x: safe_get(x, 'impliedVolatility')),
        'Expiry Date': pd.to_datetime(df['expiryDate'], errors='coerce').dt.date
    })

    # Filter for the specific expiry date
    filtered_df = filtered_df[filtered_df['Expiry Date'] == pd.to_datetime(expiry_date).date()]
    return filtered_df


# Extract and filter data for NIFTY and HDFCBANK based on the target expiry date
nifty_expiry_data = extract_by_expiry(nifty_data, target)
hdfc_expiry_data = extract_by_expiry(hdfc_data, target)


# Function to plot Strike Price vs Open Interest for Call and Put Options
def plot_strike_vs_open_interest(df, title):
    plt.figure(figsize=(12, 6))

    # Plot Call Open Interest
    plt.plot(df['Strike Price'], df['Call Open Interest'], label='Call Open Interest', color='blue', marker='o')

    # Plot Put Open Interest
    plt.plot(df['Strike Price'], df['Put Open Interest'], label='Put Open Interest', color='red', marker='o')

    # Set labels and title
    plt.xlabel('Strike Price')
    plt.ylabel('Open Interest')
    plt.title(f'Strike Price vs Open Interest for Call and Put Options ({title})')

    # Show legend
    plt.legend()

    # Display the plot
    plt.grid(True)
    plt.show()


# Function to plot Implied Volatility and Change in OI with Twin Axes
def plot_iv_and_oi_change(df, title):
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plot Change in OI on the primary y-axis
    ax1.plot(df['Strike Price'], df['Call Change in OI'], label='Call Change in OI', color='blue', marker='o')
    ax1.plot(df['Strike Price'], df['Put Change in OI'], label='Put Change in OI', color='red', marker='o')
    ax1.set_xlabel('Strike Price')
    ax1.set_ylabel('Change in Open Interest')
    ax1.tick_params(axis='y')

    # Create a second y-axis for Implied Volatility
    ax2 = ax1.twinx()
    ax2.plot(df['Strike Price'], df['Call IV'], label='Call Implied Volatility', color='purple', linestyle='--',
             marker='x')
    ax2.plot(df['Strike Price'], df['Put IV'], label='Put Implied Volatility', color='green', linestyle='--',
             marker='x')
    ax2.set_ylabel('Implied Volatility (%)')
    ax2.tick_params(axis='y')

    # Set the title
    plt.title(f'Implied Volatility and Change in OI vs Strike Price ({title})')

    # Combine legends from both axes
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc='upper left')

    # Display the plot
    plt.grid(True)
    plt.show()


# Plot for NIFTY
print("NIFTY Option Chain Data for Expiry Date:", target)
print(nifty_expiry_data)
plot_strike_vs_open_interest(nifty_expiry_data, "NIFTY")
plot_iv_and_oi_change(nifty_expiry_data, "NIFTY")

# Plot for HDFCBANK
print("\nHDFCBANK Option Chain Data for Expiry Date:", target)
print(hdfc_expiry_data)
plot_strike_vs_open_interest(hdfc_expiry_data, "HDFCBANK")
plot_iv_and_oi_change(hdfc_expiry_data, "HDFCBANK")
