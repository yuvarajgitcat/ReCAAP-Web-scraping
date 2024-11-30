import requests
import ssl
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
import pandas as pd
import json

class TLSAdapter(HTTPAdapter):
    """Custom HTTPSAdapter to enforce TLS 1.2+."""
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()
        context.set_ciphers("ALL")
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Enforce TLS 1.2 or later
        kwargs['ssl_context'] = context
        return super(TLSAdapter, self).init_poolmanager(*args, **kwargs)

def create_session():
    """Create and configure a session with TLS 1.2+."""
    session = requests.Session()
    adapter = TLSAdapter()
    session.mount("https://", adapter)
    return session

def save_response_to_excel(url, headers, cookies, payload, output_excel_file):
    """Send a POST request, parse the JSON response, and save it to an Excel file."""
    session = create_session()
    try:
        # Send the POST request
        response = session.post(url, headers=headers, cookies=cookies, json=payload)
        response.raise_for_status()  # Raise an error for HTTP errors

        # Parse the JSON response
        data = response.json()  # Ensure the response is JSON
        records = [record for record in data if isinstance(record, dict)]  # Filter valid records

        # Convert to a DataFrame
        df = pd.DataFrame(records)

        # Remove null values and unwanted columns (like `viewUrl`)
        df = df.dropna(axis=1, how='all')  # Drop columns with all null values
        if "viewUrl" in df.columns:
            df = df.drop(columns=["viewUrl"])  # Drop 'viewUrl' column if present

        # Save the DataFrame to an Excel file
        df.to_excel(output_excel_file, index=False, engine="openpyxl")
        print(f"Response successfully saved to '{output_excel_file}'")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    except ValueError as e:
        print(f"Error parsing JSON: {e}")

# Headers and Cookies (Update with actual values from F12 Network Tab)
headers = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "cache-control": "no-cache",
    "content-type": "application/json",
    "origin": "https://portal.recaap.org",
    "referer": "https://portal.recaap.org/OpenMap",
    "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

cookies = {
    "JSESSIONID": "3EE837C8A30FC67C3E02F7D792AFB953"  # Replace with your actual session cookie
}

# Payload (Update with the actual payload from F12 Network Tab)
payload = {
    "incidentDateFrom": "01 November 2012",
    "incidentDateTo": "30 November 2024",
    "shipName": "",
    "shipImoNumber": "",
    "shipFlag": "",
    "shipType": "",
    "areaLocation": [],
    "incidentType": "",
    "reportType": "Case",
    "incidentNo": ""
}

# URL of the API endpoint
url = "https://portal.recaap.org/OpenMap/MapSearchIncidentServlet/"

# Output file path
output_excel_file = "response_data.xlsx"

# Call the function to save data to an Excel file
save_response_to_excel(url, headers, cookies, payload, output_excel_file)
