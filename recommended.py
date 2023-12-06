from openai import OpenAI
from dotenv import load_dotenv
import os




load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def load_data(filename: str):

    print(f"\033[1;32m [+] \033[0mLoading data from {filename}")
    
    with open(f"./data/avaliacoes-{filename}.txt", 'r') as file:
        return file.read()
    

def analyze_product(product: str):

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
            "role": "user",
            "content": ""
            }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )


def main(products: list[str]):

    for product in range(len(products)):
        print(f"\033[1;32m [+] \033[0mAnalyzing product: {product}")
        load_data(products[product])



if __name__ == '__main__':

    products = [
        'Mixer de sucos e vitaminas',
        'Tabuleiro de xadrez de madeira',
        'Tapete de yoga'
    ]

    main(products)