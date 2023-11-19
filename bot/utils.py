from __future__ import annotations
import re
import logging
import asyncio
from telegram import Message, MessageEntity, Update, constants
from telegram.ext import CallbackContext, ContextTypes

def message_text(message: Message) -> str:
    """
    Returns the text of a message, excluding any bot commands.
    """
    message_txt = message.text
    if message_txt is None:
        return ''

    for _, text in sorted(message.parse_entities([MessageEntity.BOT_COMMAND]).items(),
                          key=(lambda item: item[0].offset)):
        message_txt = message_txt.replace(text, '').strip()

    return message_txt if len(message_txt) > 0 else ''
def split_into_chunks_nostream(text: str, chunk_size: int = 4096) -> list[str]:
    """
    Splits a string into chunks of a given size, keeping Markdown code blocks intact.
    """
    chunks = []
    start = 0
    
    for match in re.finditer(r"```.*?```", text, re.DOTALL):
        code_start, code_end = match.span()
        
        # Add the text before the code block, if any
        pre_code_text = text[start:code_start]
        while len(pre_code_text) > 0:
            chunk, pre_code_text = pre_code_text[:chunk_size], pre_code_text[chunk_size:]
            chunks.append(chunk)
        
        # Add the entire code block as one chunk
        chunks.append(text[code_start:code_end])
        
        start = code_end
    
    # Add remaining chunks after the last code block
    remaining_text = text[start:]
    while len(remaining_text) > 0:
        chunk, remaining_text = remaining_text[:chunk_size], remaining_text[chunk_size:]
        chunks.append(chunk)
    
    return chunks

async def wrap_with_indicator(update: Update, context: CallbackContext, coroutine,
                              chat_action: constants.ChatAction = "", is_inline=False):
    """
    Wraps a coroutine while repeatedly sending a chat action to the user.
    """
    sticker_file_id ='CAACAgIAAxkBAAEKx4dlWdkG5vCSbxPHsnlIulfIyMZnSgAC6gADUomRI59_7GXzyEHSMwQ'
    logging.info(f"Starting wrap_with_indicator with chat_action: {chat_action}, is_inline: {is_inline}")
    message = await update.effective_chat.send_sticker(sticker=sticker_file_id)
    task = context.application.create_task(coroutine(), update=update)
    
    while not task.done():
        try:
            await asyncio.wait_for(asyncio.shield(task), 10)
        except asyncio.TimeoutError:
            logging.warning("Task took longer than 10 seconds.")
            pass
    
    # Delete the smiley emoji message
    await message.delete()
    
    logging.info("Task completed.")

async def error_handler(_: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles errors in the telegram-python-bot library.
    """
    logging.error(f'Exception while handling an update: {context.error}')