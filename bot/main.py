import logging
import os
from dotenv import load_dotenv
from telegram_bot import TelegramHelper
from openAI_helper import OpenAIHelper


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
        'api_key': os.environ['OPENAI_API_KEY'],
    }
    telegram_config = {
        'token': os.environ['TELEGRAM_BOT_TOKEN'],
        'admin_user_ids': '-',
        'admin_usernames': os.environ['TELEGRAM_ADMIN_USERNAMES'],
        'allowed_user_ids': '*'
    }
    openai_helper = OpenAIHelper(config=openai_config)
    telegram_bot = TelegramHelper(config=telegram_config, openai=openai_helper)
    telegram_bot.run()

    
if __name__ == '__main__':
      main()
