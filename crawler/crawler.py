import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from pathlib import Path
import time

found_counter = 1
not_found_counter = 1
not_found_artists = []
df = pd.read_csv(Path.cwd().parent / "data" / "tracks.csv", sep=",")
artists = df["artist_name"].unique().tolist()

driver = webdriver.Chrome("chromedriver.exe")
driver.get("https://www.famousbirthdays.com/")
artists_df = pd.DataFrame(columns=["artist", "age", "origin"])

for artist in artists:

    input_element = driver.find_element(By.ID, "main-search")
    input_element.send_keys(artist)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    try:
        age = driver.find_element(By.XPATH, "//a[contains(text(),'years old')]").text
        origin = driver.find_element(By.XPATH, "//h6[contains(text(),'Birthplace')]/parent::div").text
        origin = origin.split("\n")[1]
        age = age.split(" ")[0]
        row = [artist, age, origin]
        artists_df.loc[found_counter] = row
        print(f"{found_counter}) {artist}, {age}, {origin}\n")
        found_counter += 1
    except NoSuchElementException:
        try:
            origin = driver.find_element(By.XPATH, "//h6[contains(text(),'Origin')]/parent::div").text
            age = ""
            origin = origin.split("\n")[1]
            row = [artist, age, origin]
            artists_df.loc[found_counter] = row
            print(f"{found_counter}) {artist}, {age}, {origin}\n")
            found_counter += 1
        except NoSuchElementException:
            try:
                age = driver.find_element(By.XPATH, "//span[contains(text(),'age')]/parent::a").text
                age = age.split("age ")[1]
                origin = driver.find_element(By.XPATH, "//h6[contains(text(),'Birthplace')]/parent::div").text
                origin = origin.split("\n")[1]
                row = [artist, age, origin]
                artists_df.loc[found_counter] = row
                print(f"{found_counter}) {artist}, {age}, {origin}\n")
                found_counter += 1
            except NoSuchElementException:
                not_found_artists.append(artist)
                print(f"not found {not_found_counter} artists\n")
                not_found_counter += 1
                continue


artists_df.to_csv(Path.cwd().parent / "data" / "artists_origin_and_age.csv")
not_found_artists_pd = pd.DataFrame(not_found_artists)
not_found_artists_pd.to_csv(Path.cwd().parent / "data" / "not_found.csv")

driver.quit()


