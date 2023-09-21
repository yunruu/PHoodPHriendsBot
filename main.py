import os
from dotenv import load_dotenv
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level= logging.INFO 
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    keyboard = [
        [
            InlineKeyboardButton("Start New Order", callback_data='start_new_order'),          
        ],
        [
            InlineKeyboardButton("Join Existing Order", callback_data='join_existing_order'),
            InlineKeyboardButton("View Past Orders", callback_data='view_past_orders'),
        ],
        [
            InlineKeyboardButton("Help", callback_data='help'),
            InlineKeyboardButton("Exit", callback_data='exit'),
        ]
    ]
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=f"Hi {update.effective_user.name}! I'm {os.environ.get('BOT_NAME')}!, a bot that helps manage your food orders and connect with like minded foodies.\n"
        + "To get started, type /help to see what I can do for you or click on one of the buttons below."
        , reply_markup=InlineKeyboardMarkup(keyboard)
    )
    
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    await query.edit_message_text(text=f"Selected option: {query.data}")

    
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=f"Here is a list of commands to help get you start right away with ordering food!"
    )
    
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.environ.get('BOT_TOKEN')).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))
    application.add_handler(CallbackQueryHandler(button))
    
    application.run_polling()
