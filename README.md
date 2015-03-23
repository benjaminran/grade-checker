# grade-checker
A Python script to check if my grades have been posted on my student portal yet

## Notes and Dependencies
This python script uses Selenium WebDriver and requires a file named "gradecount" in the script's directory to store the number of grades posted between executions. When new grades are posted, the script sends a notification email. The script is intended to be scheduled as a cron job.
