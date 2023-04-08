import openai
import json
import os

openai_key = os.environ["OPENAI_API_KEY"]

question= "Hello, How are you"

#this is the api key
openai.api_key=openai_key
# question=input("Enter your question: ")
completion=openai.Completion.create(engine="text-davinci-003",prompt=question,max_tokens=1000)
response=completion.choices[0]['text']


# socket_connect(response)
#writing the output to a json file
sorted_output=json.dumps(response)

print(sorted_output)