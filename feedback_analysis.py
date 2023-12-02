import sys, os
import openai, tiktoken
from dotenv import load_dotenv



def load_data(filename: str):

    with open(filename, 'r') as f:
        data = f.read()
        return data



def save_data(filename: str, data: str):

    with open(filename, 'w') as f:
        f.write(data)



def analyze_data(prompt_system: str, prompt_user: str, product_name: str):

    load_dotenv()
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    model = 'gpt-3.5-turbo'
    expected_value = 2048
    codifier = tiktoken.encoding_for_model(model)
    tokens_count = len(codifier.encode(data))

    if tokens_count >= 4096 - expected_value:
        model = 'gpt-3.5-turbo-16k'


    response = openai.ChatCompletion.create(

        model = 'gpt-3.5-turbo',
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

        temperature=1,
        max_tokens=expected_value,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    save_data(f"./data/reviews-{product_name}.txt", response.choices[0].message.content)

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print('Usage: python3 main.py <filename>')
        sys.exit(1)
    data = sys.argv[1]
    product_name = data.split('-')[1]
    product_name = product_name.split('.')[0]

    prompt_user = load_data(data)
    prompt_system = f"""
        You are a product review sentiment researcher.
        Write a paragraph of up to 50 words summarizing the reviews and then give the general feeling for the product.
        Also identify 3 strengths and 3 weaknesses identified from the assessments.

        #### Output format
        Product's name:

        Review summary:

        General feeling:

        Strong points:
        
        Weaknesses:
    """
    analyze_data(prompt_system, prompt_user, product_name)
