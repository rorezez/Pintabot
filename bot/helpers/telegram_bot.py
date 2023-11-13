from __future__ import annotations
from helpers.openAI_helper import OpenAIHelper
from telegram import BotCommand
from telegram import Update, constants
from telegram.ext import ContextTypes, ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext, Application
from utils import message_text, split_into_chunks_nostream , wrap_with_indicator, error_handler
import logging




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
        self.last_message = {}

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
    
    async def prompt(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handles the user's prompt and sends the response.
        """
        if not await self.check_allowed(update, context):
            user_id = update.effective_user.id  # Mengambil user ID dari pengguna yang mengirim pesan
            admin_chat_id = "5595856929"  # Ganti dengan Chat ID admin yang sebenarnya
            await context.bot.send_message(chat_id=admin_chat_id, text=f"User baru dengan ID: {user_id}")
            return
        logging.info(
            f'Pesan baru dari user {update.message.from_user.name} (id: {update.message.from_user.id})')
        chat_id = update.effective_chat.id
        prompt = f"{message_text(update.message)}"
        self.last_message[chat_id] = prompt
        try:
            async def _reply():
                #ambil response dari openai
                response= await self.openai.get_chat_response(chat_id=chat_id, query=prompt)
                # Split into chunks of 4096 characters (Telegram's message limit)
                chunks = split_into_chunks_nostream(response)

                for chunk in enumerate(chunks):
                    try:
                        await update.effective_message.reply_text(
                            text=chunk,
                            parse_mode=constants.ParseMode.MARKDOWN
                        )
                    except Exception:
                        try:
                            await update.effective_message.reply_text(text=chunk)
                        except Exception as exception:
                            raise exception

            await wrap_with_indicator(update, context, _reply, constants.ChatAction.TYPING)

        except Exception as e:
            logging.exception(e)
            await update.effective_message.reply_text(
                text="Maaf, terjadi kesalahan saat memproses permintaan anda. Silahkan coba lagi nanti.",
                parse_mode=constants.ParseMode.MARKDOWN
            )
    
    async def post_init(self, application: Application) -> None:
            """
            Post initialization hook for the bot.
            """
            await application.bot.set_my_commands(self.group_commands)
            await application.bot.set_my_commands(self.commands)

    def run(self):
        """
        Runs the bot indefinitely until the user presses Ctrl+C
        """
        application = ApplicationBuilder() \
            .token(self.config['token']) \
            .proxy_url(self.config['proxy']) \
            .get_updates_proxy_url(self.config['proxy']) \
            .post_init(self.post_init) \
            .concurrent_updates(True) \
            .build()

        application.add_handler(CommandHandler('help', self.help))
        application.add_handler(CommandHandler('start', self.help))
        application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self.prompt))

        application.add_error_handler(error_handler)

        application.run_polling()