import requests
from bs4 import BeautifulSoup
import html  # For decoding HTML entities
# Base URL for CVE Details
# BASE_URL = "https://www.cvedetails.com/vulnerability-list/vendor_id-33/Linux.html"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}


def fetchQuery(query):
    if query==None:
        return  {"error":'query cant be none'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
    }
    params = {
        'q': query,
    }
    response = requests.get(
        'https://www.cvedetails.com/vulnerability-search-autocomplete.php',
        params=params,
        headers=headers,
    )
    data= response.json()
    if len(data)==0:
        return {
        "query": query,
        "results": []
    }
    else:
        return  data[0]

def clean_text(text):
    # Decode HTML entities (like &lt;, &gt;, etc.)
    cleaned_text = html.unescape(text)
    
    # Replace multiple newlines or spaces with a single space
    cleaned_text = ' '.join(cleaned_text.split())
    
    # Optionally, clean up any other unwanted characters
    # Example: Remove any trailing whitespaces, or anything else specific
    cleaned_text = cleaned_text.strip()
    
    return cleaned_text

def scrape_cves(query):
    # Format the query into the URL
    
    data= fetchQuery(query)
    
    # Ensure data is valid and contains the expected fields
    if 'id' not in data or 'value' not in data:
        return {"error": "Invalid data format returned from fetchQuery"}
    
    # Dynamically build the BASE_URL using the 'id' and 'value' from the query result
    BASE_URL = f"https://www.cvedetails.com/vulnerability-list/vendor_id-{data['id']}/{data['value'].replace(' ', '-')}.html"
    print("Dynamic BASE_URL:", BASE_URL)
    
    url = BASE_URL
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()  # Raise an exception for HTTP errors

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find and extract CVE details
    cve_list = []
    articles = soup.find_all('div', class_='hover-bg-light')  # Adjust tag and class based on the site structure

    for row in articles[:10]:  # Limit to 10 CVEs
        cve_id = row.find('a').text.strip()  # Extract CVE ID
        description = row.find('div', class_='cvesummarylong').text.strip()  # Extract description
        score = row.find('div', class_='cvssbox').text.strip()  # Extract CVSS score (if available)
        publishDate = row.find('div', {'data-tsvfield': 'publishDate'}).text.strip()  # Extract CVSS score (if available)
        # Clean up the description text
        cleaned_description = clean_text(description)
        
        cve_list.append({
            "cve_id": cve_id,
            "description": cleaned_description,
            "cvss_score": score,
            "publish_date":publishDate
        })

    return {
        "query": query,
        "results": cve_list
    }