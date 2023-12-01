# This code is for v1 of the openai package: pypi.org/project/openai
import openai
from dotenv import load_dotenv
import os, sys, tiktoken

load_dotenv()




def load_data(input_file: str):
    
    with open(input_file, "r") as f:
        data = f.read()
        return data


def products_categorizer(prompt_system: str, prompt_user: str):

    
    openai.api_key = os.getenv("OPENAI_API_KEY") 
    model = "gpt-3.5-turbo"
    expected_value = 2048
    codifier = tiktoken.encoding_for_model(model)   
    
    tokens_count = len(codifier.encode(prompt_user))
    print(f"Tokens count: {tokens_count}")


    if tokens_count >= 4096 - expected_value:
        model = "gpt-3.5-turbo-16k"

    response = openai.ChatCompletion.create(
        
        messages = [
            {
                "role": "system",
                "content": prompt_system
            },
            {
                "role": "user",
                "content": prompt_user
            }
        ],

        model=model,
        temperature=1,
        max_tokens=expected_value,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    print(response.choices[0].message.content)


if __name__ == "__main__":

    if len(sys.argv) < 2:
        raise Exception("No data provided\nEx: python api_integration.py data.txt")
    
    data = sys.argv[1]
    prompt_system = f"""
        Identify the purchase profile for each client below.

        The format of the output should be and also in English language:

        Client - describe the client's purchase profile in 3 words
    """
    prompt_user = load_data(data)

    try:
        products_categorizer(prompt_system, prompt_user)
        
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(e)
        sys.exit(0)