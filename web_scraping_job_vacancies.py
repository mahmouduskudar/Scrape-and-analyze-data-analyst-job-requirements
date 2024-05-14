# -*- coding: utf-8 -*-
"""# **Web Scraping Job Vacancies**

# Introduction
In this project, we'll build a web scraper to extract job listings from a popular job search platform. We'll extract job titles, companies, locations, job descriptions, and other relevant information.

Here are the main steps we'll follow in this project:


1.   Setup our development environment
2.   Understand the basics of web scraping
3. Analyze the website structure of our job search platform
4. Write the Python code to extract job data from our job search platform
5. Save the data to a CSV file
6. Test our web scraper and refine our code as needed


# Prerequisites
Before starting this project, you should have some basic knowledge of Python programming and HTML structure. In addition, you may want to use the following packages in your Python environment:


These packages should already be installed in Coursera's Jupyter Notebook environment, however if you'd like to install additional packages that are not included in this environment or are working off platform you can install additional packages.

# Install Selenium and Chrome Driver Once """
"""!pip install selenium

!apt-get update
!apt install chromium-chromedriver
!cp /usr/lib/chromium-browser/chromedriver /usr/bin"""


"""# Import the require Libraries"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup as sb
import pandas as pd
from tqdm import tqdm
import requests
import re
from google.colab import files


"""# Set up to the ChromeDriver"""
chrome_driver_path = "/bin/chromedriver"

#Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
chrome_options.add_argument("--max-retry-time=90")

#Initialize the WebDriver
driver = webdriver.Chrome(options=chrome_options)


"""# Main Code where Extract Ad Link From List Page The get"""
base_url = "https://www.kariyer.net/is-ilanlari?cs={}"
# Initialize lists to store scraped data
ad_links = []
sector = {"001000000": "Bilişim","002000000": "Üretim / Endüstriyel Ürünler","003000000": "Elektrik & Elektronik","004000000": "Güvenlik","005000000": "Enerji",
          "006000000": "Gıda","007000000": "Kimya","008000000": "Maden ve Metal Sanayi","009000000": "Mobilya & Aksesuar","010000000": "Ev Eşyaları",
          "011000000": "Orman Ürünleri","012000000": "Ofis / Büro Malzemeleri","013000000": "Otomotiv","014000000": "Sağlık","015000000": "Tarım / Ziraat",
          "016000000": "Taşımacılık","017000000": "Tekstil","018000000": "Telekomünikasyon","019000000": "Turizm","020000000": "Yapı",
          "021000000": "Topluluklar","022000000": "Hizmet","023000000": "Danışmanlık","024000000": "Reklam ve Tanıtım","025000000": "Eğitim",
          "026000000": "Finans - Ekonomi","027000000": "Ticaret","028000000": "Denizcilik","029000000": "Eğlence - Kültür - Sanat","030000000": "Basım - Yayın",
          "031000000": "Medya","032000000": "Havacılık","033000000": "Hızlı Tüketim Malları","034000000": "Hayvancılık","035000000": "Sigortacılık",
          "036000000": "Dayanıklı Tüketim Ürünleri","037000000": "Atık Yönetimi ve Geri Dönüşüm","038000000": "Arşiv Yönetimi ve Saklama","039000000": "Perakende","040000000": "Çevre",
          "041000000": "İletişim Danışmanlığı","042000000": "Kaynak ve Kesme Ekipmanları","044000000": "Bina ve Site Yönetimi","045000000": "Sondaj","999000000": "Diğer"}

# Loop through each sector
for sector_code, sector_name in sector.items():
    print(f"Scraping job listings for {sector_name} sector...")
    # Construct the sector-specific URL
    sector_url = base_url.format(sector_code)

    # Load the sector page
    driver.get(sector_url)

    # Wait for the page to load completely
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Get the last page number from pagination
    soup = sb(driver.page_source, "html.parser")
    pagination = soup.find("ul", class_="pagination")
    last_page = int(pagination.find_all("li")[-2].text)  # Get the second-to-last page number

    # Loop through each page of job listings
    for page_num in tqdm(range(1, last_page + 1), desc=f"Scraping Pages for {sector_name}"):
        # Construct the URL for the current page
        url = f"{sector_url}&cp={page_num}"

        # Load the page
        driver.get(url)

        # Wait for the page to load completely
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Extract job listings from the current page
        soup = sb(driver.page_source, "html.parser")
        job_listings = soup.find_all("div", class_="list-items")

        # Extract ad links from job listings
        for card in job_listings:
            ad_link = card.find("a", class_="k-ad-card").get("href") if card.find("a", class_="k-ad-card") else None
            if ad_link:
                full_link = "https://www.kariyer.net" + ad_link
                ad_links.append(full_link)
# Create a DataFrame from the ad links
all_data = pd.DataFrame({"Ad Link": ad_links})

# Remove duplicate ad links
all_data.drop_duplicates(subset=["Ad Link"], keep="first", inplace=True)

# Define the output file name
output_file_name = "job_listings.xlsx"

# Save the DataFrame containing all data to an Excel file
all_data.to_excel(output_file_name, index=False)

print(f"Scraping completed. Data saved to {output_file_name}.")


"""# Extract Extra Information from each Ad's Page"""
# List of Turkey cities
turkey_cities = ['Adana', 'Adıyaman', 'Afyonkarahisar', 'Ağrı', 'Aksaray', 'Amasya', 'Ankara', 'Antalya', 'Ardahan', 'Artvin', 'Aydın',
                'Balıkesir', 'Bartın', 'Batman', 'Bayburt', 'Bilecik', 'Bingöl', 'Bitlis', 'Bolu', 'Burdur', 'Bursa', 'Çanakkale', 'Çankırı',
                'Çorum', 'Denizli', 'Diyarbakır', 'Düzce', 'Edirne', 'Elazığ', 'Erzincan', 'Erzurum', 'Eskişehir', 'Gaziantep', 'Giresun',
                'Gümüşhane', 'Hakkari', 'Hatay', 'Iğdır', 'Isparta', 'İstanbul(Asya)', 'İstanbul(Avr.)', 'İzmir', 'Kahramanmaraş', 'Karabük',
                'Karaman', 'Kars', 'Kastamonu', 'Kayseri', 'Kırıkkale', 'Kırklareli', 'Kırşehir', 'Kilis', 'Kocaeli', 'Konya', 'Kütahya', 'Malatya',
                'Manisa', 'Mardin', 'Mersin', 'Muğla', 'Muş', 'Nevşehir', 'Niğde', 'Ordu', 'Osmaniye', 'Rize', 'Sakarya', 'Samsun', 'Siirt', 'Sinop',
                'Sivas', 'Şanlıurfa', 'Şırnak', 'Tekirdağ', 'Tokat', 'Trabzon', 'Tunceli', 'Uşak', 'Van', 'Yalova', 'Yozgat', 'Zonguldak']

# Load the Excel file containing the scraped data
input_file_path = "/content/job_listings.xlsx"  # Update with the path to your file
output_file_path = "updated_data20000.xlsx"  # Update with the desired output file path

# Read the Excel file into a DataFrame
data = pd.read_excel(input_file_path)  # For Excel file

# Iterate through each link in the "Link" column
for index, row in tqdm(data.iterrows(), desc="Processing", total=len(data)):
    link = row["Ad Link"]
    response = requests.get(link)
    soup = sb(response.content, "html.parser")

    # Scrape data using BeautifulSoup from the link page...
    # (This part is where we scrape additional data)

    # Find the containers containing details
    details_container = soup.find("div", class_="details-container")
    location_container = soup.find("div", class_="company-location")
    company_container = soup.find("div", class_="company-info")
    position_Container = soup.find("div", class_="headline-top")
    benefits_container = soup.find("div", class_="company-benefits")

    # Find the specific detail containing
    if details_container:
      work_type_detail = details_container.find_all("div", class_="detail")[0]
      position_level_detail = details_container.find_all("div", class_="detail")[1]
      departman_detail = details_container.find_all("div", class_="detail")[2]
      app_count_detail = details_container.find_all("div", class_="detail")[3]

    if company_container:
      company_info = company_container.find_all("div")[2]

    if company_info:
      comapny_name_Url = company_info.find("div", id = "company-name")
      sectors = company_info.find("p", class_="company-department")

    # Find the container containing features and criteria using BeautifulSoup
    containers = soup.find_all("div", class_="aligment-container-section")

    # Extract the Values

    if work_type_detail:
      work_type = work_type_detail.find("p", class_="mb-0").text.strip() if work_type_detail("p", class_="mb-0") else None
    else:
      work_type = '-'
    if position_level_detail:
      position_level = position_level_detail.find("p", class_="mb-0").text.strip() if position_level_detail.find("p", class_="mb-0") else None
    else:
      position_level = '-'
    if departman_detail:
      departman = departman_detail.find("p", class_="mb-0").text.strip() if departman_detail.find("p", class_="mb-0") else None
    else:
      departman = '-'
    if app_count_detail:
      app_count = app_count_detail.find("p", class_="mb-0").text.strip() if app_count_detail.find("p", class_="mb-0") else None
    else:
      app_count = '-'
    if location_container:
      region_city = location_container.find("span").text.strip() if location_container.find("span") else None
    else:
      region_city = '-'
    if comapny_name_Url:
      company_link = comapny_name_Url.find("a").get("href") if comapny_name_Url.find("a") else None
    else:
      company_link = '-'
    if comapny_name_Url:
      company_name = comapny_name_Url.find("span").text.strip() if comapny_name_Url.find("span") else None
    else:
      company_name = '-'
    if sectors:
      sector = sectors.find("span").text.strip() if sectors.find("span") else None
    else:
      sector = '-'
    if position_Container:
      position = position_Container.find("span").text.strip() if position_Container.find("span") else None
    else:
      position = '-'
    work_model = soup.find("p", class_="mb-0").text.strip()  if soup.find("p", class_="mb-0").text.strip() else None
    if benefits_container:
      benefits = benefits_container.find("p").text.strip() if benefits_container.find("p") else None
    else:
      benefits = '-'


    # Remove unnecessary characters and whitespace from the "app_count" column
    remove = ["başvuru", "application", "redirection", "yönlendirme"]
    for word in remove:
      app_count = app_count.replace(word, "").strip() if app_count else None


    # Splite Region_city Data to City/s and Region/s
    region_city = region_city.replace(",", '')
    cities = []
    regions = []
    city_found = None

    for city in turkey_cities:
        if city in region_city:
            city_found = city  # Store the found city
            cities.append(city_found)

    if city_found:
        for city in cities:
            region_city = region_city.replace(city, '')  # Remove the cities from region_city
    else:
        cities = ['-']

    if not region_city or region_city == '-':
        regions = ['-']
    else:
        region = region_city.split('(')[-1].replace(')', '')
        regions = [region.strip()] if region else ['-']

    # Update the DataFrame with the scraped additional data
    data.at[index, "Position"] = position
    data.at[index, "Company Name"] = company_name
    data.at[index, 'City'] = ', '.join(cities)
    data.at[index, 'Region'] = ', '.join(regions)
    data.at[index, "Work Model"] = work_model
    data.at[index, "Work Type"] = work_type
    data.at[index, "Position Level"] = position_level
    data.at[index, "Departman"] = departman
    data.at[index, "Applications Count"] = app_count
    data.at[index, "Company Profile"] = company_link
    data.at[index, "Sectors"] = sector
    data.at[index, "Vested Benefits"] = benefits

    # Iterate through each container to extract features and criteria
    for container in containers:
        # Find the criterion label
        label = container.find("label", class_="d-none")
        if label:
            # Extract the feature and criterion
            feature = label.find("h3").text.strip()
            criterion = label.find("span").text.strip()

            # Check the feature and assign the criterion value to the appropriate column
            if "Tecrübe:" in feature:  # Experience
                data.at[index, "Experience"] = criterion
            elif "Eğitim Seviyesi" in feature or "Level of Education:" in feature:  # Education Level
                data.at[index, "Education Level"] = criterion
            elif "Askerlik Durumu:" in feature or "Military Status:" in feature:  # Military Status
                data.at[index, "Military Status"] = criterion
            elif "Ehliyet:" in feature or "Driving License:" in feature:  # Driver's License
                data.at[index, "License Level"] = criterion
            elif "Yabancı Dil:" in feature or "Languages:" in feature:    # languages
                data.at[index, "Languages"] = criterion

# Close the WebDriver
driver.quit()

# Save the updated DataFrame to a new Excel file
data.to_excel(output_file_path, index=False)  # For Excel file
files.download(output_file_path)
