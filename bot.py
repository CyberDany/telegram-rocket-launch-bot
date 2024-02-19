# Imports

import logging
import os

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import Application, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters
from dotenv import load_dotenv

from api import VideoAPIClient
from utils import Bisection, TelegramUtils, ImagesUtils

load_dotenv()

# Enviorment variables
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Global variables
VIDEO_API_BASE_URL='https://framex-dev.wadrid.net'
VIDEO_NAME = "Falcon Heavy Test Flight (Hosted Webcast)-wbSwFU6tY1c"
INITIAL_IMAGES_RANGE = [0, 61696]

# States and Keyboards
INITIAL, SEARCHING = range(2)
reply_keyboard = [["Yes", "No"],["Abort", "Restart"],]
initial_reply_keyboard = [["Ready", "Abort"],]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
initial_markup = ReplyKeyboardMarkup(initial_reply_keyboard, one_time_keyboard=True)

# Texts
START_MESSAGE = (
    "🚀 Welcome! We need your help to find the frame of the rocket launch. 🚀\n\n"
    "You'll see 16 images 🖼️ and must answer 'Yes' or 'No' to indicate if the rocket has launched. Use any timer shown to help determine.\n\n"
    "At any point, press 'Abort' or 'Restart' if needed.\n\n"
    "We'll reveal the launch frame at the end. 🖼️\n\n"
    "When you're ready, press 'Ready' to start."
)
ABORT_MESSAGE = (
    "Press /start if you want to try again \n"
    "Until next time!"
)
SHOW_IMAGE_MESSAGE = (
    "Frame: {}\n"
    "The rocket is launched?"
)
SOLUTION_MESSAGE = (
    "Frame: {}\n"
    "Here you have the exact frame of the launch!! Thanks for you colaboration !!"
)
RESTART_MESSAGE = "Let's start from the beginning"


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


def initialize_user_data(context):
    """
    Clears and initializes user data at the start of each conversation.
    This function resets the user's progress and ensures a fresh start.
    """
    context.user_data.clear()
    context.user_data["current_range"] = INITIAL_IMAGES_RANGE.copy()
    context.user_data["current_frame"] = 0


def get_chat_id(context):
    return context._chat_id

 
def get_user_response(update):
    return update.message.text


def get_range(context):
    return context.user_data["current_range"]


def set_range(context, new_range):
    context.user_data["current_range"] = new_range


def get_current_frame(context):
    return context.user_data["current_frame"]


def set_current_frame(context, frame_idx):
    context.user_data["current_frame"] = frame_idx


def get_current_frame_path(context):
    return context.user_data["current_frame_path"]


def set_current_frame_path(context, image_path):
    context.user_data["current_frame_path"] = image_path


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Start the conversation and ask user for input.
    """
    
    logger.info(f"[User: {update.effective_chat.id}] Conversation started with user.")

    await update.message.reply_text(START_MESSAGE,reply_markup=initial_markup)
    initialize_user_data(context)
    return INITIAL


async def show_first_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Displays the first image to the user by calculating the midpoint of the initial image range.
    This function is the starting point for the image search process, allowing users to identify the launch frame.
    """
     
    client = VideoAPIClient(VIDEO_API_BASE_URL)
    chat_id = get_chat_id(context)
    images_range = get_range(context)
    
    image_idx = Bisection.calculate_mid_point(images_range)
    set_current_frame(context, image_idx)
    
    frame_data = await client.get_frame(VIDEO_NAME, image_idx)
    
    image_path = ImagesUtils.save_image_and_get_path(chat_id, frame_data)
    set_current_frame_path(context, image_path)
    
    logger.info(f"[User: {update.effective_chat.id}] Showing the first image to user. Frame idx: {image_idx}.")
    await TelegramUtils.send_image(TELEGRAM_TOKEN, chat_id, image_path)

    await update.message.reply_text(
        SHOW_IMAGE_MESSAGE.format(image_idx),
        reply_markup=markup,
    )

    return SEARCHING


async def search_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Processes user responses to narrow down the search for the launch frame.
    Depending on the user's answer, it updates the search range and shows the next image.
    """
     
    client = VideoAPIClient(VIDEO_API_BASE_URL)
    
    chat_id = get_chat_id(context)
    user_response = get_user_response(update)

    images_range = get_range(context)
    first_image_idx = images_range[0]
    last_image_idx = images_range[1]
    
    if first_image_idx != last_image_idx:
        new_range, mid_frame = Bisection.update_range(user_response, images_range)
        set_current_frame(context, mid_frame)
        set_range(context, new_range)
    else:
        return await solution(update, context)
    
    current_frame = get_current_frame(context)
    frame_data = await client.get_frame(VIDEO_NAME, current_frame)
    
    image_path = ImagesUtils.save_image_and_get_path(chat_id, frame_data)
    set_current_frame_path(context, image_path)
    
    logger.info(f"[User: {update.effective_chat.id}] Showing image to user. Frame idx: {current_frame}.")
    await TelegramUtils.send_image(TELEGRAM_TOKEN, chat_id, image_path)

    await update.message.reply_text(
        SHOW_IMAGE_MESSAGE.format(current_frame),
        reply_markup=markup,
    )

    logger.info(f"[User: {update.effective_chat.id}] User responded: {get_user_response(update)}.")

    return SEARCHING


async def solution(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Displays the solution frame to the user, marking the end of the search process.
    This function is called when the search range is narrowed down to the exact launch frame.
    """

    logger.info(f"[User: {update.effective_chat.id}] Displaying solution to user.")

    chat_id = get_chat_id(context)
    filename = get_current_frame_path(context)
    current_frame = get_current_frame(context)
    
    await TelegramUtils.send_image(TELEGRAM_TOKEN, chat_id, filename)
    
    await update.message.reply_text(SOLUTION_MESSAGE.format(current_frame))

    return await abort(update, context)


async def abort(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Handles the user's request to abort the conversation, ending the interaction gracefully.
    """

    logger.info(f"[User: {update.effective_chat.id}] User aborted the conversation.")

    await update.message.reply_text(ABORT_MESSAGE,reply_markup=ReplyKeyboardRemove())
    initialize_user_data(context)
    return ConversationHandler.END


async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Allows the user to restart the conversation, resetting any progress and starting the process over.
    """
    logger.info(f"[User: {update.effective_chat.id}] User restarted the conversation.")

    initialize_user_data(context)
    await update.message.reply_text(RESTART_MESSAGE)
    return await start(update, context)


def main() -> None:
    """
    Run the bot.
    """

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            INITIAL: [
                MessageHandler(
                    filters.Regex("^Ready$"), show_first_image
                ),
                MessageHandler(
                    filters.Regex("^Abort$"), abort
                ),
            ],
            SEARCHING: [
                MessageHandler(
                    filters.Regex("^(Yes|No)$"), search_image
                ),
                 MessageHandler(
                    filters.Regex("^Abort$"), abort
                ),
                MessageHandler(
                    filters.Regex("^Restart$"), restart
                ),
            ]
        },
        fallbacks=[MessageHandler(filters.Regex("^Done$"), abort)],
    )
    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()