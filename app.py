import openai
import os,sys

from src.utils import get_current_weather
from src.llm import messages,functions,chat_completion_request
from src.prompts import conv_prompt
import chainlit as cl

import json






def execute_function_call(assistant_message):
    if assistant_message.get('function_call').get('name') == "get_current_weather":
        location = json.loads(assistant_message.get('function_call').get('arguments'))['location']
        results = get_current_weather(location)
    else:
        results = f"Error: function {assistant_message['function_call']['name']} dosent exist."
    return results

def get_natural_response(content,message):
    convert_prompt = conv_prompt.replace("<query>", message).replace("<api_result>", content)
    messages.append({"role": "user", "content": convert_prompt})
    convert_prompt_response = chat_completion_request(messages=messages)
    print(f"\n>>>> recieved message: {convert_prompt_response.json()}")
    new_assistant_message = convert_prompt_response.json()["choices"][0]["message"]
    messages.append(new_assistant_message)
    updated_content = new_assistant_message["content"]
    print(f"\n>>>> natural response: \n{updated_content}")
    return updated_content

@cl.on_message
async def main(message: str):
    # Your custom logic goes here...
    messages.append({'role':'user',"comtent":message})
    
    # Calling the chatgpt api response by passing the message and function
    chat_response = chat_completion_request(messages=message)
    print(f"\nChat_response: \n{chat_response}")


    # Extracting the message
    assistant_message = chat_response.json()['choices'][0]['message']
    print(f"\nAssistant Message: \n{assistant_message}") 

    if assistant_message.get('function_call'):
        result=execute_function_call(assistant_message=assistant_message)
        print(f"\nResult obtained fron executiion of functional call: \n{result}")
        content = json.dumps(result)
        content = get_natural_response(content=content,message=message)

    else:
        message.append(assistant_message)
        content = assistant_message['content']
        print(f"\nresult obtained: \n{content}")

    print(f"\n Chat Response: {content}")


    # Send a response back to the user
    await cl.Message(
        content=content
    ).send()
