#Get Json
#convert it to a python Dictionary
#add what you want to that dictionary
#convert it back to json
#Write it to the Json file(messages.json)

import json

NEW_DATA_KEY = "BOTUSERNAME" #Write Key Here
NEW_DATA_VALUE = """@habtemaryam26bot""" #Write Value Here
# When changing the holidays please make sure that you spell the key as holidays and copy the value as plain text (don't include links)

with open('messages.json', 'r') as r:
    data = json.load(r)

data[NEW_DATA_KEY] = NEW_DATA_VALUE

with open('messages.json', 'w') as w:
    json.dump(data, w)

print('SuccessFully Updated:', NEW_DATA_KEY)