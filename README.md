# ReCAAP-Web-scraping

# ReCAAP Incident Data Extraction and Save to Excel

This script extracts incident data from the ReCAAP portal's API and saves the response to an Excel file. The data is retrieved by sending a POST request to the ReCAAP server and then parsing the JSON response. The results are cleaned and saved in an Excel file format for further analysis.

## Features
- Sends a POST request to the ReCAAP portal API.
- Parses the JSON response and extracts relevant details.
- Cleans data by removing null values and unnecessary columns.
- Saves the cleaned data to an Excel file.

## Requirements
- Python 3.x
- Required Python libraries:
  - `requests` - for sending HTTP requests.
  - `pandas` - for processing and cleaning the response data.
  - `openpyxl` - for saving the data to an Excel file.

## Installation

1. **Clone the repository** (if applicable):
   ```bash
   git clone <repository_url>
   ```

2. **Install dependencies**:
   Use pip to install the required libraries:
   ```bash
   pip install requests pandas openpyxl
   ```

## Configuration

### Headers and Cookies
- You need to extract and update the **headers** and **cookies** from the **Network Tab** in your browser's developer tools (F12).
- Replace the `JSESSIONID` cookie with your session's ID.

### Payload
- The `payload` variable contains parameters for the POST request. You can modify the values of `incidentDateFrom`, `incidentDateTo`, etc., based on your requirements.

### Example:
```python
cookies = {
    "JSESSIONID": "your_session_cookie_here"
}

headers = {
    "accept": "*/*",
    "content-type": "application/json",
    "user-agent": "your_user_agent_here"
}

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
```

## How to Run

1. Ensure the required libraries are installed (`requests`, `pandas`, and `openpyxl`).
2. Update the headers, cookies, and payload with actual values.
3. Run the script:
   ```bash
   python extract_recaap_data.py
   ```

4. The script will make a POST request to the ReCAAP API, process the response, and save it to an Excel file (e.g., `response_data.xlsx`).

## Output

- The extracted incident data will be saved to an Excel file named `response_data.xlsx`.
- Columns with null values will be removed, and the `viewUrl` column will be excluded.

## Example of the Output Excel:

| id   | incidentNo   | incidentType | incidentDate | areaDescription           | shipName   | shipImoNumber | shipFlag   | shipType    | classification | remarks |
|------|--------------|--------------|--------------|---------------------------|------------|---------------|------------|-------------|----------------|---------|
| 32879| IC-2024-090  | Attempted    | 1731772800000| Straits of Malacca & Singapore| Dokos      | 9941049       | MARSHALL ISLANDS | BULK CARRIER | Attempted     | On 17 Nov 2024 at about 0350H... |
| ...  | ...          | ...          | ...          | ...                       | ...        | ...           | ...        | ...         | ...            | ...     |

## Error Handling
- The script will handle errors such as:
  - **Request exceptions** (e.g., network issues).
  - **JSON parsing errors** if the response is not in valid JSON format.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
