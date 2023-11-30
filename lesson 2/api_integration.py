# This code is for v1 of the openai package: pypi.org/project/openai
import openai
from dotenv import load_dotenv
import os

load_dotenv()

def products_categorizer(product_name: str, product_categories: str):

    openai.api_key = os.getenv("OPENAI_API_KEY")    
    prompt_system = f"""
        You're a product categorizer.
        You must choose a category from the list below:
        If the categories provided aren't valid categories, respond with "I can't help you with that"
        ##### List of valid categories
        {product_categories}
        ##### Example
        tennis ball
        sports

    """
    response = openai.ChatCompletion.create(
        
        messages = [
            {
                "role": "system",
                "content": prompt_system
            },
            {
                "role": "user",
                "content": product_name
            }
        ],

        model="gpt-3.5-turbo",
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    print(response.choices[0].message.content)


while True:
    try:
        product_name = input("Product name: ")
        product_categories = input("Product categories: ")

        products_categorizer(product_name, product_categories)
        
    except KeyboardInterrupt:
        print("Exiting...")
        break
    except Exception as e:
        print(e)
        break