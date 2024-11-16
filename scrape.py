import requests
from bs4 import BeautifulSoup

# URL of the website to scrape
url = 'https://www.cvedetails.com/vulnerability-list/vendor_id-33/Linux.html'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}

try:
    # Send an HTTP GET request to the URL
    response = requests.get(url,headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # print(soup)
    # Extract data (e.g., titles of articles)
    articles = soup.find_all('h3', class_='text-nowrap')  # Adjust tag and class based on the site structure

    # Print the extracted titles
    for index, article in enumerate(articles, start=1):
        print(f"{index}. {article.text.strip()}")
        res = requests.get(f"https://www.cvedetails.com/cve/article.text.strip()",headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors

         # Parse the HTML content of the page
        soupi = BeautifulSoup(response.text, 'html.parser')
        print(soupi)
        articl = soup.find_all('div', class_='cvesummarylong')  # Adjust tag and class based on the site structure
        for index, arti in enumerate(articl, start=1):
            print(f"{index}. {arti.text.strip()}")
except requests.exceptions.RequestException as e:
    print(f"Error fetching the URL: {e}")
