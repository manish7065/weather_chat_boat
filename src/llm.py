import requests
import json
import os
import requests
from src.prompts import system_instruction

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GPT_MODEL = 'gpt-3.5-turbo-0613' #new model for function calling abilities




def chat_completion_request(messages, functions=None, function_call=None, model=GPT_MODEL):
    headers = {
        'Content_Type': 'application/Json',
        'Authorization': 'Bearer ' + OPENAI_API_KEY,
    }
    json_data ={
        "model":model,
        "messages":messages
    }
    if functions is not None:
        json_data.update({"functions":functions})
    if function_call is not None:
        json_data.update({"fuction_call":function_call})

    try:
        response=requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers = headers,
            json = json_data
        )
        return response
    except Exception as e:
        print(f"\n>>>Unable to generate ChatCompletion response")
        print(f"\n>>> Exception: {e}")
        raise e


messages=[] #Empty the messages list to avoid previous stored data
messages.append({'role':'system',"content":system_instruction})
user_message = "Hi, there."
messages.append({'role': 'user', 'content': user_message})

functions = [
    {
        "name":"get_current_weather", # Name of the function
        "description":"This weather function will fetch the current weather report",
        'parameters':{
            "type":"object",
            'properties':{ # 1st arguement
                'location':{ #arguement name
                    'type':'string', #arguement type
                    'description':'The city and state, eg- new Delgi, Bengluru' # description of a function with example
                }
            },
            'required':['location'] # required requirement i.e ist arg is required for this function
        }
    }
]

# Calling the chatgpt api response by passing the message and function
chat_reasponse = chat_completion_request(messages,functions)

# Extracting the message
assistant_message = chat_reasponse.json()['choices'][0]['message']
# print(f"\nAssistant Message: \n{assistant_message}") 


messages.append(assistant_message)

user_message = "I want to know the weather at Bengaluru."
messages.append({'role':'user','content':user_message})
chat_reasponse = chat_completion_request(messages,functions)


# print(f"\nComplete Chat Response: \n{chat_reasponse.json()}")
assistant_message=chat_reasponse.json()['choices'][0]['message']
print(f"\nAssistant Message: \n{assistant_message}")

