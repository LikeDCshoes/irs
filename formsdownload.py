from irs import download_form


form_name = None
while not form_name:
    form_name = input('Type form name (for example: Form W-2):')

year_from = None
while not year_from:
    try:
        year_from = int(input('Type year from (for example: 2018):'))
    except ValueError:
        continue

year_to = None
while not year_to:
    try:
        year_to = int(input('Type year to (for example: 2020):'))
    except ValueError:
        continue

downloaded = download_form(form_name, year_from=year_from, year_to=year_to)
print('Downloaded %s files for form "%s" (%s - %s).' % (downloaded, form_name, year_from, year_to))
