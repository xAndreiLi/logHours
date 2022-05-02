# logHours
ASU TAS tool to log 8 days of shifts across 2 weeks.

Uses Selenium to log in to ASU, request Duo Authentication, and submit shift hours.

Inputs to the script are
  ASU ID
  Password
  Date of First Monday to be logged
  Start and End Time

Tool logs Mon-Thurs for two weeks starting from given Monday Date.
The shift times are the same for every shift.
