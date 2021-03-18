Python version: 3.9.2
Extra libraries: lxml, requests

For this challenge I created some utility module named "irs.py". There are base classes
and functions for working with IRS remote base. It helps to solve mentioned tasks and
makes possible to extend functionality.

For checking first task, you can run "formsinfo.py" file. This script handles user
input data (form numbers splitted by commas) and return JSON data into console.

For checking second task, you can run "formsdownload.py" file. This script also
handles users input data (form number, range of years) and downloads files to
subdirectory near script.

I used library "lxml" for the first time, so I would be glad to get some feedback on the solution I provided.

Thank you for your time.