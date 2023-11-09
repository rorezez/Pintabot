import logging
import os
from dotenv import load_dotenv
from helpers.telegram_helper import TelegramHelper
from helpers.openAI_helper import OpenAIHelper


def main():
    # Read .env file
    load_dotenv()

    # Setup logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)

    # Check if the required environment variables are set
    required_values = ['TELEGRAM_BOT_TOKEN', 'OPENAI_API_KEY']
    missing_values = [value for value in required_values if os.environ.get(value) is None]
    if len(missing_values) > 0:
        logging.error(f'The following environment values are missing in your .env: {", ".join(missing_values)}')
        exit(1)
    # Setup configurations
    openai_config = {
        'api_key': 'YOUR_OPENAI_API_KEY',
        'show_usage': 'false',
        'stream': 'true',
        'proxy': None,
        'assistant_prompt': 'You are a helpful assistant.',
        'max_tokens': 4093,
        'n_choices': 1,
        'temperature': 1.0,
        'image_size': '512x512',
        'model': 'gpt-3.5-turbo',
        'enable_functions': 'true',
        'functions_max_consecutive_calls': 10,
        'presence_penalty': 0.0,
        'frequency_penalty': 0.0,
        'bot_language': 'en',
        'show_plugins_used': 'false',
        'whisper_prompt': '',
    }
    telegram_config = {
        'token': 'YOUR_TELEGRAM_BOT_TOKEN',
        'admin_user_ids': '-',
        'allowed_user_ids': '*',
        'enable_quoting': 'true',
        'enable_transcription': 'true',
        'stream': 'true',
        'proxy': None,
        'voice_reply_transcript': 'false',
        'voice_reply_prompts': '',
        'ignore_group_transcriptions': 'true',
        'group_trigger_keyword': '',
        'token_price': 0.002,
        'image_prices': [0.016, 0.018, 0.02],
    }
    openai_helper = OpenAIHelper(config=openai_config)
    telegram_bot = TelegramHelper(config=telegram_config, openai=openai_helper)
    telegram_bot.run()
    if __name__ == '__main__':
        main()
