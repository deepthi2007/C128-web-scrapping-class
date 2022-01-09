from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests

url = 'https://exoplanets.nasa.gov/discovery/exoplanet-catalog/'
browser = webdriver.Chrome('D:/deepthi class/C127/chromedriver.exe')
browser.get(url)
time.sleep(10)
new_planets_data = []
headers = ["name","light_years","planet_mass","stellar_magnitude","discovery_date","hyperlink","planet_type","mass","planet_radius","orbital_radius","orbital_period","eccentricity"]
planet_data = []

def getmoreData(link):
    try:
        hyperLink = requests.get(link)
        soup = BeautifulSoup(hyperLink.content,"html.parser")
        all_tr_tags = soup.find_all("tr",attrs={"class","fact_row"})
        temp_list=[]
        for tr_tag in all_tr_tags:
            all_td_tags = tr_tag.find_all("td")
            for td_tag in all_td_tags :
                try:
                    temp_list.append(td_tag.find_all("div",attrs={"class","value"})[0].contents[0])
                except:
                    temp_list.append(" ")
        new_planets_data.append(temp_list)
    except:
        time.sleep(0)
        getmoreData(link)

def scraping():
    for i in range(0,489):
        while True:
            time.sleep(2)
            soup = BeautifulSoup(browser.page_source,"html.parser")
            current_page_num = int(soup.find_all("input",attrs={"class","page_num"})[0].get("value"))
            if current_page_num <i :
                browser.find_element_by_xpath("/html/body/div[2]/div/div[3]/section[2]/div/section[2]/div/div/article/div/div[2]/div[1]/div[2]/div[1]/div/nav/span[1]/a").click()
            elif current_page_num>i:
                browser.find_element_by_xpath("/html/body/div[2]/div/div[3]/section[2]/div/section[2]/div/div/article/div/div[2]/footer/div/div/div/nav/span[2]/a").click()
            else:
                break

        all_ul_tags = soup.find_all("ul",attrs={"class","exoplanet"})
        for ul_tag in all_ul_tags:
            all_li_tags = ul_tag.find_all("li")
            li_values = []
            for index,li_tag in enumerate(all_li_tags):
                if index==0 :
                    li_values.append(li_tag.find_all("a")[0].contents[0])
                else :
                    li_values.append(li_tag.contents[0])
            hyperlink_li_tag = li_tag[0]
            li_values.append("https://exoplanets.nasa.gov"+hyperlink_li_tag.find_all("a",href=True)[0]["href"])
            planet_data.append(li_values)
        browser.find_element_by_xpath("/html/body/div[2]/div/div[3]/section[2]/div/section[2]/div/div/article/div/div[2]/section/div/div/div/ul[2]/li[1]/a").click()
        print(f"{i} page done 1")


scraping()
for i,data in enumerate(planet_data):
    getmoreData(data[5])
    print(f"{i+1} page done 2")
final_planet_data = []
for i,data in enumerate(planet_data):
    new_planet_data_element = new_planets_data[i]
    new_planet_data_element= [elem.replace("\n","") for elem in new_planet_data_element]
    new_planet_data_element=new_planet_data_element[:7]
    final_planet_data.append(data+new_planet_data_element)

with open("scraped_data.csv","W") as f :
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(final_planet_data)