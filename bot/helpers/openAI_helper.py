import openai

class OpenAIHelper:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key

    def generate_response(self, prompt):
        try:
            response = openai.Completion.create(
              engine="text-davinci-002",
              prompt=prompt,
              temperature=0.5,
              max_tokens=100
            )
            return response.choices[0].text.strip()
        except Exception as e:
            print(f"Error: {e}")
            return None