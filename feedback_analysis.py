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



def analyze_data(prompt_system: str, product_name: list[str]):

    load_dotenv()
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    model = 'gpt-3.5-turbo'
    expected_value = 2048

    for product in range(len(product_name)):
        data = load_data(f"./data/avaliacoes-{product_name[product]}.txt")    
        codifier = tiktoken.encoding_for_model(model)
        tokens_count = len(codifier.encode(data))

        prompt_user = data
        
        if tokens_count >= 4096 - expected_value:
            model = 'gpt-3.5-turbo-16k'


        print(f"Analyzing product: {product_name[product]}")
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

        save_data(f"./data/reviews-{product_name[product]}.txt", response.choices[0].message.content)
        print(f"Product: {product_name[product]} conclued with success!")


if __name__ == '__main__':

    product_name = [
        "Tapete de yoga", 
        "Tabuleiro de xadrez de madeira", 
        "Mixer de sucos e vitaminas"
    ]
    
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
    analyze_data(prompt_system, product_name)
