import openai
import json
import os

openai_key = "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"
#"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"
question= "Hello, How are you"

openai.api_key=openai_key
# question=input("Enter your question: ")
completion=openai.Completion.create(engine="text-davinci-003",prompt=question,max_tokens=1000)
response=completion.choices[0]['text']


# socket_connect(response)
#writing the output to a json file
sorted_output=json.dumps(response)

print(sorted_output)