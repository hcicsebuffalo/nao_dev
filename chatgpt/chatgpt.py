#! /home/sougato97/miniconda3/envs/nao_env/bin/python3
# -*- encoding: UTF-8 -*-

# shebang path added at top

import openai  
import json

openai.api_key="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"


#Take user input for the question
question=input("Enter your question: ")


completion=openai.Completion.create(engine="text-davinci-003",prompt=question,max_tokens=1000)
response=completion.choices[0]['text']


# write to a json file 
sorted_output=json.dumps(response)
with open('json_file.json', "w") as outfile:
    outfile.write(sorted_output)


# print("number1")