import requests
from bs4 import BeautifulSoup

# The URL we want to scrape (a safe sandbox website)
url = "http://quotes.toscrape.com"

# --- STEP 1: REQUEST ---
# We simulate a browser sending a request to the server.
response = requests.get(url)

# --- STEP 2: RESPONSE ---
# The server sends back the raw HTML. We check if it worked (Status 200 = OK).
if response.status_code == 200:
    print("Server connected successfully!")

    # --- STEP 3: PARSING ---
    # We convert the raw text into a structured tree of objects.
    soup = BeautifulSoup(response.text, "html.parser")

    # --- STEP 4: EXTRACTION ---
    # We search for the specific HTML tag <span class="text">.
    # .find() gets the first one; .text removes the HTML tags.
    quote_data = soup.find("span", class_="text").text
    
    print("\n--- Extracted Result ---")
    print(quote_data)

else:
    print("Failed to retrieve data.")