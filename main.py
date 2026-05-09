from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.by import By

from time import sleep

driver = webdriver.Chrome()
driver.get("https://gymkhana.iitb.ac.in/sports/turfbooking")

name = "insert name"
nm = driver.find_element(By.XPATH, "/html/body/div/div/main/div/form/div[1]/input")
nm.send_keys(name)

rollNum = "Roll_number"
roll = driver.find_element(By.XPATH, "/html/body/div/div/main/div/form/div[2]/input")
roll.send_keys(rollNum)

LdapId = rollNum+"@iitb.ac.in"
ldap = driver.find_element(By.XPATH, "/html/body/div/div/main/div/form/div[3]/input")
ldap.send_keys(LdapId)

otherRoll = "roll1, roll2, roll3, ..."
Other = driver.find_element(By.XPATH, "/html/body/div/div/main/div/form/div[4]/input")
Other.send_keys(otherRoll)

numPlayer = 12
Players = driver.find_element(By.XPATH, "/html/body/div/div/main/div/form/div[5]/input")
Players.send_keys(numPlayer)

# /html/body/div/div/main/div/form/div[6]/button[1]
# /html/body/div/div/main/div/form/div[6]/button[14]

print("Available slots:")
print("1.  6:30 AM - 7:30 AM")
print("2.  7:30 AM - 8:30 AM")
print("3.  8:30 AM - 9:30 AM")
print("4.  9:30 AM - 10:30 AM")
print("5.  10:30 AM - 11:30 AM")
print("6.  11:30 AM - 12:30 PM")
print("7.  12:30 PM - 1:30 PM")
print("8.  1:30 PM - 2:30 PM")
print("9.  2:30 PM - 3:30 PM")
print("10. 3:30 PM - 5:00 PM")
print("11. 5:00 PM - 6:00 PM")
print("12. 6:00 PM - 7:00 PM")
print("13. 7:00 PM - 8:00 PM")
print("14. 8:00 PM - 9:30 PM")

i = input("enter slot: ")

slot = driver.find_element(By.XPATH, f"/html/body/div/div/main/div/form/div[6]/button[{i}]")
driver.execute_script("arguments[0].scrollIntoView(true);", slot)
driver.execute_script("arguments[0].click();", slot)

try:
    driver.switch_to.alert.accept()
except NoAlertPresentException:
    pass

check = driver.find_element(By.XPATH, "/html/body/div/div/main/div/form/div[7]/input")
driver.execute_script("arguments[0].scrollIntoView(true);", check)
driver.execute_script("arguments[0].click();", check)

book = driver.find_element(By.XPATH, "/html/body/div/div/main/div/form/button")
driver.execute_script("arguments[0].scrollIntoView(true);", book)
driver.execute_script("arguments[0].click()", book)

try:
    driver.switch_to.alert.accept()
except NoAlertPresentException:
    pass

sleep(5)
driver.quit()