import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


def get_artists_origins(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function finds origins o artists in https://www.famousbirthdays.com/.

    :param df: the input Dataframe
    :return: Dataframe of found artists and their origins
    """
    artists = df["artist_name"].unique().tolist()
    driver = webdriver.Chrome("chromedriver.exe")
    driver.get("https://www.famousbirthdays.com/")
    artists_df = pd.DataFrame(columns=["artist_name", "age", "origin"])

    for artist in artists:
        origin, age = "", ""
        input_element = driver.find_element(By.ID, "main-search")
        input_element.send_keys(artist)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        try:
            age = driver.find_element(By.XPATH, "//a[contains(text(),'years old')]").text.split(" ")[0]
            origin = driver.find_element(By.XPATH, "//h6[contains(text(),'Birthplace')]/parent::div").text.split("\n")[
                1]
        except NoSuchElementException:
            try:
                origin = driver.find_element(By.XPATH, "//h6[contains(text(),'Origin')]/parent::div").text.split("\n")[
                    1]
            except NoSuchElementException:
                try:
                    age = driver.find_element(By.XPATH, "//span[contains(text(),'age')]/parent::a").text.split("age ")[
                        1]
                    origin = \
                        driver.find_element(By.XPATH, "//h6[contains(text(),'Birthplace')]/parent::div").text.split(
                            "\n")[1]
                except NoSuchElementException:
                    continue
        finally:
            if origin:
                found_df = pd.DataFrame([[artist, age, origin]], columns=["artist_name", "age", "origin"])
                artists_df.append(found_df, ignore_index=True)

    driver.quit()
    return artists_df
