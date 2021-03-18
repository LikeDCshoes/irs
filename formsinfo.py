from irs import get_form
import json


form_names = []
while not form_names:
    form_names = input('Type form names separated by commas (for example: Form W-2, Form 1095-C):')
    form_names = set(filter(None, map(str.strip, form_names.split(','))))


forms = list(filter(None, [get_form(form_name) for form_name in form_names]))

output = [
    {
        'form_number': form.number,
        'form_title': form.title,
        'min_year': form.get_min_year(),
        'max_year': form.get_max_year()
    }
    for form in forms
]

print(json.dumps(output, indent=4))
