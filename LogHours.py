from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import Select
from webdriver_manager.firefox import GeckoDriverManager
from datetime import timedelta, date, time

# Get user input for login and shift info
username = input("Username: ")
password = input("Password: ")
dayInput = input("Enter First Date to Log (m/d/YYYY): ")
print("Hours (0-23) : Minutes (increments of 15)")
startInput = input("Enter Start Time (H:mm): ")
endInput = input("Enter End Time (H:mm): ")

# Parse dayInput as date object
dayValues = dayInput.split('/')
m = int(dayValues[0])
d = int(dayValues[1])
Y = int(dayValues[2])
firstDay = date(Y, m, d)

# Create dates for 8 days across 2 weeks
format = "%m/%d/%Y"
addDay = timedelta(days=1)
addWeek = timedelta(days=4)
dates=[]
for i in range(2):
	dates.append(firstDay.strftime(format))
	for j in range(3):
		firstDay = firstDay + addDay
		dates.append(firstDay.strftime(format))
	firstDay = firstDay + addWeek

# Parse Time inputs into formatted strings
# and calculate hours worked
timeValues = startInput.split(":")
timeValues += endInput.split(":")

# Only converts hours to ints
for i in range(0,4,2):
	timeValues[i] = int(timeValues[i])

# Creates timedelta objects to subtract
fromTime = timedelta(hours=timeValues[0], minutes=int(timeValues[1]))
toTime = timedelta(hours=timeValues[2], minutes=int(timeValues[3]))
hours = toTime - fromTime
hours = hours.seconds/3600

# Formats 24 to 12 hh and adds AM/PM
if timeValues[0] > 12:
	timeValues[0] -= 12
	fromTime = str(timeValues[0]) + ":" + timeValues[1] + " PM"
elif timeValues[0] == 12:
	fromTime = str(timeValues[0]) + ":" + timeValues[1] + " PM"
elif timeValues[0] == 0:
	fromTime = "12:" + timeValues[1] + " AM"
else:
	fromTime = str(timeValues[0]) + ":" + timeValues[1] + " AM"

if timeValues[2] > 12:
	timeValues[2] -= 12
	toTime = str(timeValues[2]) + ":" + timeValues[3] + " PM"
elif timeValues[2] == 12:
	toTime = str(timeValues[2]) + ":" + timeValues[3] + " PM"
elif timeValues[2] == 0:
	toTime = "12:" + timeValues[3] + " AM"
else:
	toTime = str(timeValues[2]) + ":" + timeValues[3] + " AM"

# Get Firefox Webdriver automatically
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

# Create wait object
wait = WebDriverWait(driver, 10)

# Load TAS login page
driver.get("http://tas.asu.edu")

# Log in to ASU
userInput = driver.find_element(By.ID, "username")
passInput = driver.find_element(By.ID, "password")

userInput.send_keys(username)
passInput.send_keys(password)
passInput.send_keys(Keys.RETURN)

try:
	# Wait for Duo Login page to load and switch focus to duo iFrame
	duoFrame = wait.until(EC.presence_of_element_located((By.ID, "duo_iframe")))
	driver.switch_to.frame(duoFrame)

	# Wait for push buttons to load and click
	pushButton = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Send Me a Push')]")))
	pushButton.click()
except TimeoutException:
	print("Timeout")
	exit()

# Wait for user to authorize and load page
input("Press enter after authorization and page load...")

# Return focus to main page
driver.switch_to.default_content()

# Iterate once for each date
for day in dates:
	newReqBtn = driver.find_element(By.ID, "btnNewRequest")
	newReqBtn.click()
	
	# Wait for popup window to load
	typeSel = Select(wait.until(EC.element_to_be_clickable((By.ID, "cbotype"))))
	typeSel.select_by_value("Hours Worked")

	fromInp = driver.find_element(By.ID, "txtfrom")
	fromInp.clear()
	fromInp.send_keys(day)
	fromInp.send_keys(Keys.RETURN)

	# Wait for datepicker to vanish
	wait.until(EC.invisibility_of_element((By.CLASS_NAME, "ui-datepicker-title")))

	fromSel = Select(driver.find_element(By.ID, "txthourfrom"))
	fromSel.select_by_value(fromTime)
	toSel = Select(driver.find_element(By.ID, "txthourto"))
	toSel.select_by_value(toTime)

	hoursInp = driver.find_element(By.ID, "txthours")
	hoursInp.send_keys(str(hours))

	subBtn = driver.find_element(By.XPATH, "//*[contains(text(), 'Submit Request')]")
	subBtn.click()

	confBtn = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Yes, submit request')]")))
	# Get both overlay divs
	overlays = driver.find_elements(By.CLASS_NAME, "ui-widget-overlay ui-front")
	confBtn.click()

	# Wait for popups to close
	for overlay in overlays:
		wait.until(EC.invisibility_of_element(overlay))
	