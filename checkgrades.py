#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import smtplib
from email.mime.text import MIMEText
import time

EMAIL_SUBJECT = "New Grades Posted"
EMAIL_TO = "********"
EMAIL_FROM = "********"
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

print(time.strftime("Checking grades on: %c", time.localtime()))
browser = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs')
browser.set_window_size(1120, 550)
browser.implicitly_wait(10)

# Log in to my.ucsc.edu
print("Logging into student portal")
browser.get("https://my.ucsc.edu")
browser.find_element_by_id("userid").clear()
browser.find_element_by_id("userid").send_keys("********")
browser.find_element_by_id("pwd").clear()
browser.find_element_by_id("pwd").send_keys("********")
browser.find_element_by_name("Submit").click()

# Navigate to "My Student Center"
print("Navigating to \"My Student Center\"")
browser.find_element_by_id("pthnavbca_MYFAVORITES").click()
browser.find_element_by_link_text("My Student Center").click()
# Navigate to "Grades" for Winter 2015
print("Navigating to \"Grades\"")
browser.switch_to_frame(browser.find_element_by_id("ptifrmtgtframe"))
browser.find_element_by_id("DERIVED_SSS_SCR_SSS_LINK_ANCHOR4").click()
print("Switching term to Winter 2015")
browser.find_element_by_id("DERIVED_SSS_SCT_SSS_TERM_LINK").click()
browser.find_element_by_id("SSR_DUMMY_RECV1$sels$1$$0").click()
browser.find_element_by_id("DERIVED_SSS_SCT_SSR_PB_GO").click()
browser.find_element_by_id("STDNT_ENRL_SSV1_CRSE_GRADE_OFF$0").click()

# Check if new grades added
print("Counting grades listed in portal")
numgrades = 0
for element in browser.find_elements_by_class_name("PABOLDTEXT"):
    grade = element.text.strip()
    if grade != '' and len(grade)<5 : numgrades += 1

print("Recovering previous gradecount from file")
gradecountfile = open('/Users/beni/dev/grade-checker/gradecount', 'r+')
prevnumgrades = int(gradecountfile.read().strip())

# If new grades added, update gradecount file and notify me

if numgrades != prevnumgrades:
    print("New grades have been posted! There are now %d grades posted. Notifying...." % numgrades)
    gradecountfile.seek(0)
    gradecountfile.write(str(numgrades))
    gradecountfile.truncate()

    message = browser.find_elements_by_class_name("PSLEVEL1GRID")[0].text
    send_email(message)
else:
    print("There are still only %d grades posted" % numgrades)
# Clean up
print("Done!")
browser.quit()
