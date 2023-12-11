from dotenv import load_dotenv
import openai, os
import json
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')





def load_data(filename: str):

    try:
        print(f"\033[1;32m[+] \033[0mLoading data from {filename}")
        
        with open(filename, 'r') as file:
            return file.read()
    except IOError as e:
        print(f"\033[1;31m[-] \033[0mError loading data from {filename}: {e}")





def save_data(filename: str, data: str):

    try:
        print(f"\033[1;32m[+] \033[0mSaving data to {filename}")

        with open(f'./data/mail-{filename}.txt', 'w') as file:
            file.write(data)
    except IOError as e:
        print(f"\033[1;31m[-] \033[0mError saving data to {filename}: {e}")





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
        )

        return response.choices[0].message.content
    
    except openai.error.APIConnectionError as e:
        print(f"\033[1;31m[-] \033[0mError connecting to OpenAI API: {e}")
    except Exception as e:
        print(f"\033[1;31m[-] \033[0mError analyzing profiles: {e}")





def recommend_products(profile: str, products_list: str):

    prompt_system = f"""
        You are a product recommender.
          Consider the following profile: {profile}
          We recommend 3 products from the list of valid products that are suitable for the profile provided.
        
          #### List of products valid for recommendation
          {products_list}
        
          Use English Language
          The output should only be the name of the products recommended in bullet points, like this:

          - product1
          - product2
          - product3

          as I said, don't say at the beginning, "Based on product" or "I recommend", just tell me the 3 product.
          also output the product in english language.
    """

    response = openai.ChatCompletion.create(

        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": prompt_system
            }
        ],
    )
    
    return response.choices[0].message.content





def write_mail(recommendations: str):

    print("\033[1;32m[+]\033[0m Writing recommendation mail")
    prompt_system = f"""
        Write an email recommending the following products to a customer:
            
        {recommendations}

        The email must have a maximum of 3 paragraphs.
        The tone should be friendly, informal and relaxed.
        Treat the customer as someone close and known.
    """

    response = openai.ChatCompletion.create(

        model="gpt-3.5-turbo-16k",
        messages=[
            {
                "role": "system",
                "content": prompt_system
            }
        ],
    )
    
    return response.choices[0].message.content





if __name__ == '__main__':

    purchased_list = load_data('./data/lista_de_compras_10_clientes.csv')
    product_list = load_data('./data/lista_de_produtos.txt')
    print("\033[1;32m[+] \033[0mAnalyzing...")
    profiles = json.loads(analyze_profiles(purchased_list))

    for client in profiles['clients']:
        print(f"\033[1;32m[+] \033[0mRunning on client: {client['name']}\033[0m")
        recommendations = response = recommend_products(client['profile'], product_list)
        print(f"\033[1;32m[+] \033[0mFinished on client: {client['name']}")
        print(f"{recommendations}")
        mail_data = write_mail(recommendations)
        save_data(client['name'], mail_data)
