from selenium import webdriver
from selenium.webdriver.common.by import By

file_contents = None

with open("createObjects.py", "rt") as file:
    file_contents = file.read()

# Now you can execute the code
exec(file_contents)
