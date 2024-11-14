import requests
import time
import json

#importing all required urls
NSE = 'https://www.nseindia.com'
NIFTYURL = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'
HDFCBANKURL = 'https://www.nseindia.com/api/option-chain-equities?symbol=HDFCBANK'


#importing headers file from website Network option
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
    'Referer': NSE
}

# Create a session to manage cookies and headers
session = requests.Session()

# Initial request to capture cookies
session.get(NSE, headers=headers)
time.sleep(1)  # Mimic browser behavior by waiting


# Function to fetch data and save as json file
def fetch_and_save_data(url, filename):
    try:
        response = session.get(url, headers=headers, cookies=session.cookies)
        if response.status_code == 200:
            json_data = response.json()  # Parse JSON data
            # Save JSON data to file
            with open(filename, 'w') as f:
                json.dump(json_data, f, indent=4)
            print(f"Data saved to {filename}")
        else:
            print(f"Failed to fetch data. Status Code: {response.status_code}")
    except requests.exceptions.JSONDecodeError:
        print("Failed to parse JSON - the response may not be JSON-formatted.")
        print("Response Text:")
        print(response.text)  # Print raw text for diagnosis


# Fetch data every 3 minutes
while True:
    print("Fetching NIFTY data...")
    fetch_and_save_data(NIFTYURL, 'nifty.json')

    print("Fetching HDFCBANK data...")
    fetch_and_save_data(HDFCBANKURL, 'hdfcbank.json')

    print("Wait for 3 minutes before the next fetch...")
    time.sleep(180)  # Wait for 3 minutes before the next fetch
