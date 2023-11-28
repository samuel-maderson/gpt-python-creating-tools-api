# This code is for v1 of the openai package: pypi.org/project/openai
import openai
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")    
prompt_system = """
    You're a product categorization
    When you receive a user request you've to should between these categories below
    ### Categories
        Beauty
        Sports
        Finantial
        Others
    ### Question
        Category of Basketball?
    ### Output
        Sports

"""
response = openai.ChatCompletion.create(
    
    messages = [
        {
            "role": "system",
            "content": prompt_system
        },
        {
            "role": "user",
            "content": "Brush Teeth"
        }
    ],

    model="gpt-3.5-turbo",
    temperature=1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    n=5
)

for i in range(0,5):
    print(response.choices[i].message.content, end="\n-------------------\n")