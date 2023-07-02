#!/bin/bash

echo [$(date)]: "start"
echo [$(date)]: "Creating conda env with python 3.9"
conda create --name chat_env python=3.9 -y
echo [$(date)]: "activate chat_env"
conda activate chat_env

# Checking if chat_env has been activated or not

env_name="chat_env"

env_list=$(conda env list)

if [[ $env_list == *"$env_name"* ]]; then
    echo "The '$env_name' has been activated, so packages will be installed."
    echo [$(date)]: "installing the requirements"
    pip install -r requirements.txt
else
    echo "The '$env_name' has not been activated. Please activate it manually and then install the packages using 'pip install -r requirements.txt'."
fi
echo [$(date)]: 'END'
