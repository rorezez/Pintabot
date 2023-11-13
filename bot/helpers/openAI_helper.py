import openai

class OpenAIHelper:
    def __init__(self, config: dict):
        openai.api_key = config['api_key']
        self.config = config
        self.thread_mapping = {}
        self.client = openai.Client()
        thread = self.client.beta.threads.create()

# create assistant
# create thread
# run assistant
#
#
#