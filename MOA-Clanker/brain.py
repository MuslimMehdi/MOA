import ollama
class Think():
    def __init__(self, query):
        response = ollama.chat(
            model='llama3.2:3b',
            messages=[
                {'role': 'user', 'content': query },
            ],
        )
        print(response['message']['content'])
