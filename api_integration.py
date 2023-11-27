import openai, os
from dotenv import load_dotenv

load_dotenv()


openai.api_key = os.getenv("OPENAI_API_KEY")
response = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    messages = [
        {
            "role": "system", 
            "content": "Make random products names without description according with the user request"
         
        },
        {
            "role": "user",
            "content": "Make 5 products"
        }
    ]
)

print(response)