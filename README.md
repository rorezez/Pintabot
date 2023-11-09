# Chatbot Backend

This project is a backend for a chatbot that interacts with users via Telegram and uses OpenAI for processing user inputs.

## Project Structure

The project has the following structure:

```
chatbot-backend
├── src
│   ├── chatbot.py
│   ├── helpers
│   │   ├── telegram_helper.py
│   │   └── openAI_helper.py
├── requirements.txt
└── README.md
```

## Description

- `src/chatbot.py`: This is the entry point of the application. This file creates an instance of the chatbot and manages interactions with the user.

- `src/helpers/telegram_helper.py`: This file exports the `TelegramHelper` class which has methods for interacting with the Telegram API. These methods include sending and receiving messages.

- `src/helpers/openAI_helper.py`: This file exports the `OpenAIHelper` class which has methods for interacting with the OpenAI API. These methods include sending and receiving messages.

- `requirements.txt`: This is a configuration file for pip. It lists the dependencies required for the project.

## Installation

1. Clone this repository.
2. Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

## Usage

To start the chatbot, run the following command:

```bash
python src/chatbot.py
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)