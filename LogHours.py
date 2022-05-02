from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import Select
from webdriver_manager.firefox import GeckoDriverManager
from datetime import datetime, timedelta, date

username = input("Username: ")
password = input("Password: ")
dayInput = input("Enter First Date to Log (m/d/YYYY): ")

format = "%m/%d/%Y"
firstDay = date(2022, 5, 2)

addDay = timedelta(days=1)
addWeek = timedelta(days=4)

dates=[]
for i in range(2):
	dates.append(firstDay.strftime(format))
	for j in range(3):
		firstDay = firstDay + addDay
		dates.append(firstDay.strftime(format))
	firstDay = firstDay + addWeek

fromTime = 7
toTime = 12

driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
driver.get("http://tas.asu.edu")

userInput = driver.find_element_by_id("username")
passInput = driver.find_element_by_id("password")

userInput.send_keys(username)
passInput.send_keys(password)
passInput.send_keys(Keys.RETURN)

try:
	duoFrame = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "duo_iframe")))
	driver.switch_to.frame(duoFrame)
	pushButton = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Send Me a Push')]")))
	pushButton.click()
	print("click")
except TimeoutException:
	print("Timeout")
	exit()

input("Press enter after authorization...")

driver.switch_to.default_content()

for day in dates:
	newReqBtn = driver.find_element(By.ID, "btnNewRequest")
	newReqBtn.click()


	typeSel = Select(WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.ID, "cbotype"))))
	typeSel.select_by_value("Hours Worked")

	fromInp = driver.find_element(By.ID, "txtfrom")
	fromInp.clear()
	fromInp.send_keys(day)
	fromInp.send_keys(Keys.RETURN)

	WebDriverWait(driver, 2).until(EC.invisibility_of_element((By.CLASS_NAME, "ui-datepicker-title")))

	hours = toTime - fromTime
	fromTime = str(fromTime) + ":00 AM"
	toTime = str(toTime) + ":00 PM"

	fromSel = Select(driver.find_element(By.ID, "txthourfrom"))
	fromSel.select_by_value(fromTime)
	toSel = Select(driver.find_element(By.ID, "txthourto"))
	toSel.select_by_value(toTime)

	hoursInp = driver.find_element(By.ID, "txthours")
	hoursInp.send_keys(str(hours))

	subBtn = driver.find_element(By.XPATH, "//*[contains(text(), 'Submit Request')]")
	subBtn.click()

	confBtn = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Yes, submit request')]")))
	confBtn.click()