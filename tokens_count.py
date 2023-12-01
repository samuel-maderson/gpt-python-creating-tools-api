import tiktoken


codifier_model = tiktoken.encoding_for_model("gpt-3.5-turbo")
tokens_list = codifier_model.encode("Hello World")
cost = len(tokens_list)/1000 * 0.0015
print(f"Your cost is: {cost}")