from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

print("Libraries imported")

# Selenium web driver configurated
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

url = "https://www.reclameaqui.com.br/empresa/hp"
driver.get(url)

# Wait the page load
time.sleep(3)

# Get the data
page_source = driver.page_source

# Using beautiful soup to parse html
soup = BeautifulSoup(page_source, 'html.parser')

print("Content Parsed.")

data = []

# Extrair informações dos elementos
print("Getting infos: ")

titles = soup.find_all('h4', class_='bVKmkO') 
descriptions = soup.find_all('p', class_='eHoNfA')
responses = soup.find_all('span', class_='ihkTSQ')
datas = soup.find_all('span', class_='dspDoZ')

if titles:
    print("Titles obtained")
if descriptions:
    print("Descriptions obtained")
if responses:
    print("Responses obtained")
if datas:
    print("Dates obtained")

# Iter with elements extracted added with the data list
for title, description, response_text, data_text in zip(titles, descriptions, responses, datas):
    data.append({
        'title': title.get_text().strip(),
        'description': description.get_text().strip(),
        'response': response_text.get_text().strip(),
        'data': data_text.get_text().strip()
    })

# Creating the dataframe with data extracted
df = pd.DataFrame(data)

# Saving the data with csv format
df.to_csv('reports_hp_selenium.csv', index=False, encoding='utf-8')
print("Dados salvos com sucesso!")

# Close driver
driver.quit()
