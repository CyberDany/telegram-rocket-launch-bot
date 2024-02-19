from telegram.ext import Application

class TelegramUtils:
    @staticmethod
    async def send_image(bot_token: str, chat_id: int, image_path: str):
        """
        Sends an image to a Telegram chat asynchronously.

        Initializes a bot with the given token, opens the image from `image_path`, and sends it to `chat_id`.

        Parameters:
        - bot_token (str): Telegram bot token.
        - chat_id (int): Target chat ID.
        - image_path (str): Path to the image file.
        """
        app = Application.builder().token(bot_token).build()

        with open(image_path, 'rb') as image_file:
            await app.bot.send_photo(chat_id=chat_id, photo=image_file)