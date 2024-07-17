import ast
from openai import OpenAI


def generate_chat_response(messages, model="gpt-4o"):
    print('Calling llm')
    client = OpenAI()
    completions = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
        response_format={"type": "json_object"}
    )
    print('llm responded')
    return ast.literal_eval(completions.choices[0].message.content)


if __name__ == "__main__":
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the World Series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Can you tell me more about the team in a json format?"}
    ]
    response = generate_chat_response(messages)
    print(response)
