from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import Application, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters

class TelegramUtils:
    @staticmethod
    async def send_image(bot_token, chat_id, image_path):
        app = Application.builder().token(bot_token).build()

        # Abre el archivo de la imagen en modo binario.
        with open(image_path, 'rb') as image_file:
            # Usa 'await' para esperar que la operación asíncrona de enviar la foto se complete.
            await app.bot.send_photo(chat_id=chat_id, photo=image_file)