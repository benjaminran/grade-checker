# grade-checker
A Python script to check if new grades have been posted on my student portal yet

## Overview
This Python 3 script uses Selenium WebDriver (running PhantomJS) and requires a file named "gradecount" in the script's directory to store the number of grades posted between executions. When new grades are posted, the script sends me a notification email. The script is intended to be scheduled as a cron job with output redirected into log files.
