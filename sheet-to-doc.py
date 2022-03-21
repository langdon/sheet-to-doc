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
args = vars(ap.parse_args())

sheet_fn = test_file(args["sheet_fn"])
output_fn = args["output_fn"]

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
    Project Name: {{ project.name }}
    {% for q_label, answers in project.questions.items() %}
        Question: {{ q_label }}
        {% for email, answer in answers.items() %}
            Email: {{ email }}
            Feedback: {{ answer }}
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
output = tm.render(feedback=tmp_feedback)

with open(output_fn, "w") as output_file:
    output_file.write(output)

#    print(tabulate(row, headers='keys', tablefmt='psql'))
    #print(row)
exit()

#    if not feedback[row["Project Name"]]:
#        feedback[row["Project Name"]] = {}
#    project = feedback[row["Project Name"]]

#form_by_project = form_csv.groupby(by="Project Name")
#print(form_by_project.)

#print(tabulate(form_by_project, headers='keys', tablefmt='psql'))

#for project in form_by_project["Project Name"]:
#    print(tabulate(project, headers='keys', tablefmt='psql'))
#    print(type(project))
#    exit()


# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', 1000)
# pd.set_option('display.colheader_justify', 'center')
# pd.set_option('display.precision', 3)

# display(df)

# with open(sheet_fn) as csvfile:
#     reader = csv.DictReader(csvfile, delimiter=",", quotechar='"')
#     num_col = len(next(reader))
#     for row in reader:
#         if not feedback[row["Project Name"]]:
#             feedback[row["Project Name"]] = {}
#         project = feedback[row["Project Name"]]
#         for i in range(3, num_cols+1):
#             if not project[row[i]]

#         confirmed_talk = Canonical_Talk.to_canonical_talk(row)
#         if confirmed_talk['confirmed']:
#             print("Confirmed talk: has {}:\"{}\" been scheduled? ".format(confirmed_talk.id, confirmed_talk.title), end='')
#             #look for the talk in scheduled by id
#             try:
#                 talk = scheduled_talks[confirmed_talk.id]
#                 #talk = get_talk(scheduled_talks, row["ID"])
#                 if talk.title.strip() != confirmed_talk.title.strip():
#                     print(" -- Talk ID Mismatch: Confirmed Talk ID: {}, Title: '{}'; Accepted Talk Title: '{}'"
#                         .format(confirmed_talk.id, confirmed_talk.title, talk.title))
#                     problems.append(confirmed_talk)
#                 else:
#                     all_set[confirmed_talk.id] = {"scheduled" : talk, "confirmed" : confirmed_talk}
#                     print("Yes: {}-{}".format(talk.start, talk.end))
#                     scheduled_talks.pop(confirmed_talk.id)
#             except (StopIteration, KeyError) as e:
#                 try:
#                     #talk not found by id, check for it by title
#                     talk = get_talk(scheduled_talks, confirmed_talk.title, "Title")
#                     all_set[talk.id] = {"scheduled" : talk, "confirmed" : confirmed_talk}
#                     print("Yes: {}-{}".format(talk.start, talk.end))
#                     scheduled_talks.pop(talk.id)
#                 except (StopIteration, KeyError) as e:
#                     #ok not found at all, let's report it
#                     problems.append(confirmed_talk)
#                     print(" -- Talk confirmed but not scheduled: Confirmed Talk ID: {}, Title: '{}'"
#                         .format(confirmed_talk.id, confirmed_talk.title))



# link_sets = {}
# with open(urls_fn) as csvfile:
#     reader = csv.DictReader(csvfile)
#     tmp = list(reader)
#     for row in tmp:
#         link_sets[row["name"]] = row

# talks = Canonical_Talk.load_canonical_talks(sched_talks_fn)
# speakers = Canonical_Speaker.load_canonical_speakers(sched_speakers_fn)
# talks_speakers = {}

# #people are missed because ben (talk) vs benjamin (speaker)
# for talk_id, talk in talks.items():
#     talk_speaker = None
#     for speaker in speakers.values():
#         if speaker.name.lower() in talk.speakers.lower():
#             if talk_speaker is not None:
#                 talk_speaker[talk_id]["speakers"].append(speaker)
#                 print("talk already had speaker")
#             #i probably don't need this, we should find all speakers in one pass
#             elif talk_id in talks_speakers.keys():
#                 talk_speaker = talks_speakers[talk_id]
#                 talk_speaker["speakers"].append(speaker)
#                 print("talk already inserted")
#             else:
#                talk_speaker = {talk_id: {"speakers": [speaker], "talk": talk}}
#             #no break so we go through all possible speakers (1+ per talk)
#     if talk_speaker is not None:
#         talk_speaker[talk_id].update({"links": link_sets[talk.title]})
#         talks_speakers.update(talk_speaker)

#     print(talk_speaker)

# tweet_templates = []
# with open(text_fn) as file:
#     tweet_templates = file.readlines()

# tweets = {}
# num_templates = len(tweet_templates) - 1
# for talk_speaker in talks_speakers.values():
#     pos = random.randint(0, num_templates)
#     repl = {}
#     speakers = talk_speaker["speakers"]
#     talk = talk_speaker["talk"]
#     link = talk_speaker["links"]["longlink"]

#     speaker_names = talk.speakers
#     handles = []
#     for speaker in speakers:
#         if "twitter.com" in speaker.url.lower():
#             handles.append("@" + speaker.url.rsplit('/', 1)[-1])
#             #speaker_names = speaker_names.replace(speaker.name, speaker.name + " (@" + handle +")")
# #        elif speaker.url:
# #            speaker_names = speaker_names.replace(speaker.name, speaker.name + " (" + speaker.url +")")
#     speaker_names = re.sub('\s*;\s*', " and ", speaker_names)

#     repl.update({"NAME": speaker_names})
#     repl.update({"URL": link})
#     repl.update({"TITLE": talk.title})
#     repl.update({"DATE": talk.start.strftime("%b. %d")})

#     tweet_orig = tweet_templates[pos].format(**repl).strip()
#     tweet = tweet_orig
#     if len(handles) > 0:
#         tweet = tweet_orig + " /cc " + ' '.join(handles)
#     #if we are going over the length limit, drop the name decorators
#     if len(tweet) > 220:
#         tweet = tweet_orig
# #        speaker_names = re.sub('\s*;\s*', " and ", speaker_names)
# #        repl.update({"NAME": speaker_names})

#     #this could be wrong based on luck
#     lead_speaker = speakers[0]
#     tweet_row = {"date": datetime.now(), "tweet": tweet, "url": link,
#         "char_count": len(tweet), "image_url": lead_speaker.image_url}
#     tweets.update({talk.id: tweet_row})
#     print(tweet)

# _hootsuite_fields = ["date", "tweet", "url", "char_count", "image_url"]

# with open(output_fn, 'w') as csvfile:
#     out_writer = csv.DictWriter(
#         csvfile, fieldnames=_hootsuite_fields, quoting=csv.QUOTE_ALL)
#     out_writer.writeheader()
#     for tweet in tweets.values():
#         out_writer.writerow(tweet)

# print("done")
# #pp.pprint(speakers)
# #pp.pprint(talks)


# # for talk_id, talk in talks.items():
# #     for speaker in speakers.values():
# #         if speaker.name.lower() in talk.speakers.lower():
# #             tmp = {speaker_id: {"speaker": speaker, "talks": [talk]}}
# #             if speaker_id in speakers_talks.keys():
# #                 tmp = speakers_talks[speaker_id]
# #                 tmp["talks"].append(talk)
# #                 print("speaker already inserted")
# #             speakers_talks.update(tmp)
# #             print(tmp)