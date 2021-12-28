from pathlib import Path

from selenium import webdriver

driver = webdriver.Chrome(executable_path=Path.cwd() / "chromedriver.exe")
