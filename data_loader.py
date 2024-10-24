import requests
import os
from bs4 import BeautifulSoup
import pandas as pd

__all__ = ['download_data', 'extract_last_date_updated', 'preprocess_df']

def download_data(url="https://api.neso.energy/dataset/cbd45e54-e6e2-4a38-99f1-8de6fd96d7c1/resource/17becbab-e3e8-473f-b303-3806f43a6a10/download/tec-register-27-09-2024.csv",
                  filename="tecregister.csv"):
    """
    Download data from the specified URL and save it to a file.

    Parameters:
        url (str): The URL to download data from.
        filename (str): The name of the file where the data will be saved.

    Returns:
    
        DataFrame: Dataframe of csv file downloaded.
    """
    resp = requests.get(url)
    
    if resp.ok:
        os.makedirs("datastore", exist_ok=True)
        filepath = f"datastore/{filename}"
        
        with open(filepath, "wb") as f:
            f.write(resp.content)
        return pd.read_csv(filepath)
    else:
        return pd.DataFrame([])
    


def extract_last_date_updated():
    """
    Extract the last updated date from a webpage using a CSS selector.

    Parameters:
    
        url (str): The URL of the webpage to scrape.
        
        selector (str): The CSS selector to locate the target elements.

    Returns:
    
        str: The text of the first matching element containing "ago" if found,
            otherwise "Element not found".
        List[str]: If a request error occurs, returns a list containing the error message.
    """
    url = 'https://www.neso.energy/data-portal/transmission-entry-capacity-tec-register'

    try:
        # Fetch the webpage content
        response = requests.get(url)

        soup = BeautifulSoup(response.text, "lxml")

        extracted_texts = soup.find_all('td', class_="views-field views-field-title")
        last_updated = [element.text.split('-')[1].strip() for element in extracted_texts]

        return last_updated if last_updated else "unknown"

    except requests.RequestException as e:
        return [f"Error fetching the URL: {e}"]


# Convert to datetime and format date
def preprocess_df(df: pd.DataFrame):
    """
    Preprocess the DataFrame by converting date columns and renaming specific columns.

    Parameters:
    
        df (pd.DataFrame): The DataFrame to preprocess.

    Returns:
    
        pd.DataFrame: The preprocessed DataFrame with updated column names and 
                    'MW Effective From' converted to datetime format.
    """
    df["MW Effective From"] = pd.to_datetime(df["MW Effective From"], errors="coerce")
    df.rename(
                columns={
                    "MW Increase / Decrease": "MW Change",
                    "Cumulative Total Capacity (MW)": "Connection Cap (MW)",
                    "MW Effective From": "Connection Date",
                },
                inplace=True,
            )
    return df
