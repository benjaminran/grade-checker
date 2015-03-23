#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import smtplib
from email.mime.text import MIMEText

EMAIL_SUBJECT = "New Grades Posted"
EMAIL_TO = "****@****.com"
EMAIL_FROM = "****@****.com"
EMAIL_PASSWORD = "********"

def send_email(body):
    global EMAIL_TO
    global EMAIL_SUBJECT
    global EMAIL_FROM
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(EMAIL_FROM, EMAIL_PASSWORD)
    server.sendmail(EMAIL_FROM, EMAIL_TO, body)
    server.quit()

#
# Main Routine: Check grades and notify me if new grades are posted
#

browser = webdriver.Firefox()
browser.implicitly_wait(10)

# Log in to my.ucsc.edu
browser.get("https://my.ucsc.edu")
browser.find_element_by_id("userid").clear()
browser.find_element_by_id("userid").send_keys("********")
browser.find_element_by_id("pwd").clear()
browser.find_element_by_id("pwd").send_keys("********")
browser.find_element_by_name("Submit").click()

# Navigate to "My Student Center"
browser.find_element_by_id("pthnavbca_MYFAVORITES").click()
browser.find_element_by_link_text("My Student Center").click()
# Navigate to "Grades"
browser.switch_to_frame(browser.find_element_by_id("ptifrmtgtframe"))
browser.find_element_by_id("DERIVED_SSS_SCR_SSS_LINK_ANCHOR4").click()
browser.find_element_by_id("DERIVED_SSS_SCT_SSS_TERM_LINK").click()
browser.find_element_by_id("SSR_DUMMY_RECV1$sels$1$$0").click()
browser.find_element_by_id("DERIVED_SSS_SCT_SSR_PB_GO").click()
browser.find_element_by_id("STDNT_ENRL_SSV1_CRSE_GRADE_OFF$0").click()

# Check if new grades added
numgrades = 0
for element in browser.find_elements_by_class_name("PABOLDTEXT"):
    grade = element.text.strip()
    if grade != '' and len(grade)<5 : numgrades += 1

gradecountfile = open('gradecount', 'r+')
prevnumgrades = int(gradecountfile.read().strip())

# If new grades added, update gradecount file and notify me
if numgrades != prevnumgrades:
    gradecountfile.seek(0)
    gradecountfile.write(str(numgrades))
    gradecountfile.truncate()

    message = browser.find_elements_by_class_name("PSLEVEL1GRID")[0].text
    send_email(message)

# Clean up
browser.quit()
