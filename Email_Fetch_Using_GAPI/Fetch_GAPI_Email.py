import requests
from bs4 import BeautifulSoup
import re
import time

# Replace these with your actual API Key and Custom Search Engine ID (CX)
API_KEY = 'AIzaSyBSTrYZPnDeb-Aj3bbhCtIGakQDWVqIsBk'  # Your Google API Key
CX = '563f4fa7fe000433d'  # Your Custom Search Engine ID (CX)

# Function to search Google
def search_google(query, start):
    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "cx": CX,
        "key": API_KEY,
        "start": start,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Function to scrape emails from a webpage
def scrape_emails(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            emails = set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", soup.text))
            return emails
    except Exception as e:
        print(f"Error scraping {url}: {e}")
    return set()

# Main function to collect emails
def collect_emails(query, max_results=1000):
    emails = set()
    start = 1
    while len(emails) < max_results:
        # Fetch Google search results
        results = search_google(query, start)
        if not results or "items" not in results:
            break
        
        for item in results["items"]:
            link = item.get("link")
            if link:
                # Scrape emails from the link
                found_emails = scrape_emails(link)
                emails.update(found_emails)
        
        # Google Custom Search API paginates every 10 results
        start += 10
        if start > 1000:  # Limit to 100 results due to API restrictions
            break
        
        # Sleep to avoid rate limits
        time.sleep(1)
    
    return list(emails)[:max_results]

# Run the script
query = "small building construction contractors in Colombia"
emails = collect_emails(query, max_results=1000)

# Save emails to a file
with open("emails.txt", "w") as f:
    f.write("\n".join(emails))

print(f"Collected {len(emails)} emails. Saved to 'emails.txt'.")
