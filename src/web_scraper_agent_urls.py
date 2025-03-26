from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

def get_agent_profiles(search_url, max_pages=50):

    """
        This is what this function supposed to do:
            1. Go to the url "https://www.zillow.com/professionals/real-estate-agent-reviews/stockton-ca/?page=1".
                This URL contains the links for all of the Real Estate Agents personal pages.
            2. It has to go one by one through all of the pages (.../?page=2 then 3 then 4 till the end)
                and store the links of the agents' personal pages.
            3. Once this function is done, I will create another function to go to those stored URL of the agents and fetch the 
                review data.
    """

    # Set up Selenium WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    agent_links = []
    
    for page_num in range(1, max_pages + 1):
        url = f"{search_url}?page={page_num}"
        print(f"Scraping page {page_num}: {url}")
        driver.get(url)
        time.sleep(30)  # Allow time for JavaScript to load

        # Find all agent profile links
        agents = driver.find_elements(By.XPATH, '//a[contains(@href, "/profile/")]')

        # Stop if no new agents are found
        if not agents:
            print("No more agents found. Stopping pagination.")
            break

        for agent in agents:
            link = agent.get_attribute("href")
            if link and "profile" in link and link not in agent_links:
                agent_links.append(link)

    driver.quit()

    # Save to CSV
    df = pd.DataFrame({"Agent Profile URL": agent_links})
    df.to_csv("zillow_agents.csv", index=False)

    print(f"Scraped {len(agent_links)} agent profiles and saved to zillow_agents.csv")

# Example: Zillow real estate agents in Stockton, CA
search_url = "https://www.zillow.com/professionals/real-estate-agent-reviews/stockton-ca"
get_agent_profiles(search_url)
