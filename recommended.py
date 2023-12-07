from dotenv import load_dotenv
import openai, os
import json
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')



def load_data(filename: str):

    try:
        print(f"\033[1;32m [+] \033[0mLoading data from {filename}")
        
        with open(filename, 'r') as file:
            return file.read()
    except IOError as e:
        print(f"\033[1;31m [-] \033[0mError loading data from {filename}: {e}")


def save_data(filename: str, data: str):

    try:
        print(f"\033[1;32m [+] \033[0mSaving data to {filename}")

        with open(f'./data/review-{filename}.txt', 'w') as file:
            file.write(data)
    except IOError as e:
        print(f"\033[1;31m [-] \033[0mError saving data to {filename}: {e}")


def analyze_profiles(prompt_user: str):

    try:
        prompt_system = """
            Identity the purchase profile for each customer below.

            The output format should be in JSON:

            {
                "clients": [
                    {
                        "name": "Client name",
                        "profile": "describe the customer profile in 3 words"
                    }
                ]
            } 
        """
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
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
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )


        return response.choices[0].message.content
    
    except openai.error.APIConnectionError as e:
        print(f"\033[1;31m [-] \033[0mError connecting to OpenAI API: {e}")
    except Exception as e:
        print(f"\033[1;31m [-] \033[0mError analyzing profiles: {e}")




def recommend_products(prompt_user: str):

    prompt_system = """
        You're a products recommender.

        Based on this input:

        client name
        categories

        output with 3 products related to these categories. only say the product name with a good description of the product but at same time, try to convince the client to buy it. Moreover, before talking about the product, call the client by the name and try to be very kind and aware of what he needs.

        # For instance:
        Product: 
        Description: 

        Use English language.
    """

    response = openai.ChatCompletion.create(

        model="gpt-3.5-turbo",
        messages=[
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
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    return response.choices[0].message.content


if __name__ == '__main__':

    product_list = load_data('./data/lista_de_compras_10_clientes.csv')
    print("\033[1;32m [+] \033[0mAnalyzing...")
    processsed_data = analyze_profiles(product_list)
    json_data = json.loads(processsed_data)
    for client in json_data['clients']:
        print(f"Running on client: {client['name']}")
        response = recommend_products(f"Client: {client['name']}\nCategories: {client['profile']}")
        save_data(client['name'], response)
        
        
        