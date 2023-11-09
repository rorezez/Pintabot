from __future__ import annotations
from helpers.openAI_helper import OpenAIHelper
from telegram import BotCommand
from telegram import Update
from telegram.ext import ContextTypes




# Path: bot/helpers/telegram_helper.py
class TelegramHelper:
    "ini adalah class untuk telegramnya"

    def __init__(self, config: dict, openai: OpenAIHelper):
        """
        Initializes the bot with the given configuration and GPT bot object.
        :param config: A dictionary containing the bot configuration
        :param openai: OpenAIHelper object
        """
        self.config = config
        self.openai = openai
        self.commands = [
            BotCommand(command='help', description="Menampilkan pesan bantuan"),
            BotCommand(command='reset', description="Menghapus konteks percakapan saat ini"),
            BotCommand(command='stats', description="Menampilkan statistik penggunaan bot"),
            BotCommand(command='regenerate', description="Menghasilkan ulang model gpt"),
            BotCommand(command='addcontext', description='Tambahkan konteks ke dalam percakapan')
        ]
        self.disallowed_message = "Maaf anda belum terdaftar sebagai pengguna bot ini. Silahkan hubungi @{} untuk mendapatkan akses.".format(
            self.config['admin_username'])
        self.usage = {}
        self.last_message = {}
        self.inline_queries_cache = {}

    async def help(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Shows the help menu.
        """
        commands = self.commands
        commands_description = [f'/{command.command} - {command.description}' for command in commands]
        help_message = f"Selamat datang di {self.config['bot_name']}!\n\n"

        # Menambahkan daftar perintah ke help_message
        help_message += "Berikut adalah command yang bisa di gunakan:\n"
        help_message += '\n'.join(commands_description)
        help_message += "\n\nUntuk mulai menggunakan {}, silahkan ajukan pertanyaan melalui pesan text atau menggunakan pesan suara.".format(self.config['bot_name'])
        
        await update.message.reply_text(help_message, disable_web_page_preview=True)