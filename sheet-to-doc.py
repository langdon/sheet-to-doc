#!/usr/bin/env python
"""
You can use this script to generate a file consolidating a spreadsheet
"""

import csv
import pprint
from datetime import datetime
import argparse
import os.path
import re
import collections
import random
import numpy as np
import pandas as pd
from tabulate import tabulate
from jinja2 import Template

def test_file(fn):
    if not os.path.isfile(fn):
        print("{0} does not exist.".format(fn))
        exit()
    return fn

pp = pprint.PrettyPrinter(indent=4)

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True, dest="sheet_fn",
	help="csv file with form submissions")
ap.add_argument("-o", "--output", required=True, dest="output_fn",
	help="doc with form submissions consolidated")
ap.add_argument("-p", "--remove-pii", required=False, dest="pii", action='store_true',
	help="remove pii from output")
args = vars(ap.parse_args())

sheet_fn = test_file(args["sheet_fn"])
output_fn = args["output_fn"]
pii = args["pii"]

feedback = {}
form_csv = pd.read_csv(sheet_fn)

for index, row in form_csv.iterrows():
    if row["Project Name"] not in feedback:
        feedback[row["Project Name"]] = {"name": row["Project Name"], \
            "questions": {} }

    questions = feedback[row["Project Name"]]["questions"]
    for label, data in row[3:len(row)].items():
        if label not in questions:
            questions[label]= {}
        item = questions[label]
        item[row["Email Address"]] = str(data).replace("\n", " ")

#pp.pprint(feedback)

output_template = '''
{% for project in feedback %}
# {{ project.name -}}
    {% for q_label, answers in project.questions.items() %}
## Question: {{ q_label -}}
        {% for email, answer in answers.items() %}
* **{{ email }}**: {{ answer -}}
        {% endfor %}
    {% endfor %}
{%- endfor %}
'''

output_template_pii = '''
{% for project in feedback %}
# {{ project.name -}}
    {% for q_label, answers in project.questions.items() %}
## Question: {{ q_label -}}
        {% for email, answer in answers.items() %}
* {{ answer -}}
        {% endfor %}
    {% endfor %}
{%- endfor %}
'''

#output_template = '''
#{% for project in feedback -%}
#    Project Name: {{ project.name }}
#{%- endfor %}
#'''
tmp_feedback = feedback.values()

tm = Template(output_template)
if pii:
    tm = Template(output_template_pii)
output = tm.render(feedback=tmp_feedback)

with open(output_fn, "w") as output_file:
    output_file.write(output)
