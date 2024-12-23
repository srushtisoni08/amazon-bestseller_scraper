from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import re
from collections import defaultdict
import json

email = input("Enter email:")
password= input("Enter password: ")

driver = webdriver.Firefox()

try:
    driver.get("https://www.amazon.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3Fref_%3Dnav_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0")    
    
    time.sleep(2)

    email_field = driver.find_element(By.NAME, "email")
    email_field.send_keys(email)
    email_field.send_keys(Keys.RETURN)

    time.sleep(2) 

    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)

    time.sleep(2) 

    account_link = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "nav-line-1-container"))
)
    print(account_link.text)
    if "sign in" not in account_link.text:
        print("Logged in successfully")
        options = Options()
        options.set_preference("general.useragent.override", 
                            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
        driver = webdriver.Firefox(options=options)
        try:
            driver.get("https://www.amazon.in/gp/bestsellers/?ref_=nav_em_cs_bestsellers_0_1_1_2")            
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.ID, "zg_left_col1")))
            try:
                search_box = driver.find_element(By.ID, "twotabsearchtextbox")
                print("Search box found!")
            except Exception as e:
                print("Could not find search box:", str(e))
            try:
                elements = driver.find_elements(By.ID, "zg_left_col1")
                categories = defaultdict(list)  
                current_category = "General"  
                product_pattern = re.compile(r"#\d+\n(.*?)(\n\d[\d,]*\n₹[\d,.]+)", re.S)  
                for element in elements:
                    data = element.text
                    lines = data.splitlines()
                    for line in lines:
                        line = line.strip()
                        if "Bestsellers in" in line:  
                            current_category = line.replace("See More", "").strip()
                        elif re.match(r"#\d+", line):  # Start capturing product details
                            match = product_pattern.match("\n".join(lines[lines.index(line):]))  # Try to match a product block
                            if match:
                                product_details = match.group(1).strip() + " " + match.group(2).strip()
                                categories[current_category].append(product_details)                      
                with open("bestseller_products.json", "w", encoding="utf-8") as file:
                    json.dump(categories, file, indent=4, ensure_ascii=False)
                print("Product data saved successfully to 'bestseller_products.json'.")
            except Exception as e:
                print("Error while finding Best Sellers content:", str(e))
        finally:          
            print("Terminating browser...")
            time.sleep(1)
            driver.quit()
    else:
        print("Login failed")
except Exception:
    print("Wrong login credentials.")
finally:
    driver.quit()