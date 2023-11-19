import openai
import time
import logging
import pprint
class OpenAIHelper:
    def __init__(self, config: dict):
        openai.api_key = config['api_key']
        self.client = openai.Client(api_key=openai.api_key)  # Corrected client initialization
        self.config = config
        self.thread_mapping = {}
        self.assistant = None  # Changed to None, since only one assistant is handled
        self.current_message = {}

    # create assistant
    def get_or_create_assistant(self, name: str, model: str = "gpt-4-1106-preview"):
        print(f"get_or_create_assistant({name}, {model})")

        # Retrieve the list of existing assistants
        assistants = self.client.beta.assistants.list().data

        # Check if an assistant with the given name already exists
        for assistant in assistants:
            if assistant.name == name:
                self.assistant = assistant
                # update model if different
                if assistant.model != model:
                    print(f"Updating assistant model from {assistant.model} to {model}")
                    self.client.beta.assistants.update(
                        assistant_id=assistant.id, model=model
                    )
                break
        else:  # If no assistant was found with the name, create a new one
            self.assistant = self.client.beta.assistants.create(
                model=model,
                name=name,
                instructions="You are a personal assistant. Answer every question with emoji only.",
                tools=[{"type": "code_interpreter"}]
            )
        return self.assistant.id

    # create thread
    def create_thread(self, chat_id: int):
        if chat_id not in self.thread_mapping:
            print(f"create_thread({chat_id})")
            thread = self.client.beta.threads.create()
            self.thread_mapping[chat_id] = thread.id
        return self.thread_mapping[chat_id]

    # get message from assistant
    async def get_message_from_assistant(self, chat_id: int, prompt: str):
        
        run_id = await self.run_assistant(chat_id=chat_id, query=prompt, assistant_id=self.assistant.id)

        while True:
            time.sleep(5)  # Wait for 5 seconds
            thread_id = self.thread_mapping.get(chat_id)
            # Retrieve the run status
            run_status = self.client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id) 
            # If run is completed, get messages
            if run_status.status == 'completed':
                messages = self.client.beta.threads.messages.list(thread_id=thread_id)
                self.current_message[chat_id] = messages.data  # Corrected to store the messages data
                return messages.data

    # run assistant
    async def run_assistant(self, chat_id: int, query: str, assistant_id: str = None):
        if not query:
            raise ValueError("Query must not be empty")
        if not assistant_id:
            raise ValueError("Assistant ID must not be empty")

        thread_id = self.thread_mapping.get(chat_id)
        if not thread_id:
            thread_id = self.create_thread(chat_id)  # Create a new thread if thread ID is not found

        self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=query,
        )
        run = self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
        ) 
        return run.id
