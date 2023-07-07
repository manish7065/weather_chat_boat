import os,sys
from src.prompts import system_instruction
import requests

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GPT_MODEL = "gpt-3.5-turbo-0613"

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

messages = [{'role':'system','content':system_instruction}]