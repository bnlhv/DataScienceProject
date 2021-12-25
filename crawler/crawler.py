import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time

i = 0
not_found_artists = []
df = pd.read_csv("tracks.csv", sep=",")
artists = df["artist_name"].unique()
pd.DataFrame(artists)
driver = webdriver.Chrome("chromedriver.exe")
driver.get("https://www.famousbirthdays.com/")
artists_df = pd.DataFrame(columns=["artist", "age", "birth place"])

for artist in artists:

    input_element = driver.find_element(By.ID, "main-search")
    input_element.send_keys(artist)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    try:
        age = driver.find_element(By.XPATH, "//a[contains(text(),'years old')]").text
        birth_place = driver.find_element(By.XPATH, "//h6[contains(text(),'Birthplace')]/parent::div").text
    except NoSuchElementException:
        not_found_artists.append(artist)
        print(f"{artist} not found")
        continue


    birth_place = birth_place.split("\n")[1]
    age = age.split(" ")[0]
    row = [artist, age, birth_place]
    artists_df.loc[i] = row
    print(f"{i}: {artist}")
    i += 1

artists_df.to_csv("artists.csv", index=False)
not_found_artists_pd = pd.DataFrame(not_found_artists)
not_found_artists_pd.to_csv("not_found.csv", index=False)

driver.quit()


