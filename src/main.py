# Copyright 2023 Aviraj Saha
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see https://www.gnu.org/licenses/gpl-3.0.txt.
# ==============================================================================
"""# Bot Script

This module serves as the main script of the bot.

### Note: 
This should run on continuously on a server.

## Metadata
- `Author:` Aviraj Saha, Maithil Saha
- `Purpose:` This module serves as the main script of the bot.
"""
from typing import Final


# Version and other technical data
__version__ = "0.1.0-alpha"
__all__ = []


# Path alias
EVENT_LOG_PATH: Final[str] = "logs/events.log"
FEEDBACK_LOG_PATH: Final[str] = "user_messages/feedback.txt"
ENQUIRY_LOG_PATH: Final[str] = "user_messages/enquiry.txt"


# Mode variables
user_message_mode: str = (
    None  # Variable to switch between the different text handling modes. Currently "Feedback", "Enquiry" and regular mode
)


# import database_interface
from os import getenv
from datetime import datetime
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    CallbackContext,
)
from dotenv import load_dotenv
from logging import error, warning, basicConfig, WARNING, ERROR, FileHandler, getLogger


# Config for loading .env
load_dotenv(
    dotenv_path=".env"
)  # Create your own .env file the project root directory before running this script.


# Getting API token and username from .env
TOKEN: Final[str] = getenv("api_token_telegrambot")
BOT_USERNAME: Final[str] = getenv("username_telegrambot")


# Config for logging
basicConfig(
    filename=EVENT_LOG_PATH,
    filemode="a",
    format="%(name)s - %(levelname)s - %(message)s",
    level=WARNING,
)


# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    with open("bot_responses/on_start.txt", "r") as file:
        await update.message.reply_text(file.read())


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    with open("bot_responses/help.txt", "r") as file:
        await update.message.reply_text(file.read())


async def activate_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("your record is started")


async def deactivate_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    await update.message.reply_text("Your record is paused")


async def delete_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Your record is deleted")


async def my_class_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("This feature is under development")


async def contribute_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    await update.message.reply_text("This feature is under development")


async def fetchname_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("This feature is under development")


async def fetchdate_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("This feature is under development")


async def fetchrange_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    await update.message.reply_text("This feature is under development")


async def create_class_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    await update.message.reply_text("This feature is under development")


async def delete_class_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    await update.message.reply_text("This feature is under development")


async def join_class_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    await update.message.reply_text("This feature is under development")


async def leave_class_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    await update.message.reply_text("This feature is under development")


async def open_source_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    with open("bot_responses/open_source.txt", "r") as file:
        await update.message.reply_text(file.read())


async def commands_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    with open("bot_responses/commands.txt", "r") as file:
        await update.message.reply_text(file.read())

#Function to activate feedback mode to receive feedback
async def feedback_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global user_message_mode
    user_message_mode = "Feedback"
    await update.message.reply_text(
        'Please write your feedback message. You can also write "cancel" or use command /cancel to cancel. Please do not share any sensitive info like email address, usernames etc.'
    )

# Function to activate enquiry mode to receive enquiries 
async def enquiry_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global user_message_mode
    user_message_mode = "Enquiry"
    await update.message.reply_text(
        'Please state your question. You can also write "cancel" or use command /cancel to cancel. Please do not share any sensitive info like email address, usernames etc.'
        ' Our developers will get back to you within 1-3 working days. We apologize for any inconvenience caused in the meantime.'
    )


async def dev_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("This feature is under development")

# Function to serve as a global cancel to cancel /enquiry and /feedback
async def cancel_command(update: Update, context: CallbackContext) -> None:
    global user_message_mode
    if any((user_message_mode,)):
        user_message_mode = None
        await update.message.reply_text("Canceled most recent interaction.")
        return
    await update.message.reply_text("No current interaction to cancel.")


# Function to record user feedback and store it in feedback.txt in user_messages folder
async def feedback_receive(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    match str.lower(user_message):
        case "cancel":
            await update.message.reply_text(
                "Canceled feedback. Please feel free to share your thoughts and feedback on the bot so we can continue to improve and deliver best possible services."
            )
        case _:
            with open(FEEDBACK_LOG_PATH, "a") as feedback_file:
                feedback_file.write(f"\n{str(datetime.now())}: " + user_message)
            await update.message.reply_text("Thank you for your valuable feedback.")

    global user_message_mode
    user_message_mode = None
    
# Function to record user enquiries and store it in enquiry.txt in user_messages folder
async def enquiry_receive(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    match str.lower(user_message):
        case "cancel":
            await update.message.reply_text(
                "Canceled enquiry. Please feel free to reach out to us if you have any queries."
            )
        case _:
            with open(ENQUIRY_LOG_PATH, "a") as enquiry_file:
                enquiry_file.write(f"\n{str(datetime.now())}: {update.message.chat.username}: " + user_message)
            await update.message.reply_text("Your enquiry has been noted. We will get back to you soon.")

    global user_message_mode
    user_message_mode = None

# Response Manager
def handle_response(text: str) -> str:
    processed_text = text.strip().lower()

    return "Sorry, This bot is still unable to respond on messages. try typing '/' before your commands"


# Message Manager
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text: str = update.message.text
    response: str

    # Switches between feedback mode, enquiry mode and normal text mode
    match user_message_mode:
        case "Feedback":
            await feedback_receive(update, context)
            return
        case "Enquiry":
            await enquiry_receive(update, context)
            return
        case _:
            response = handle_response(text)
            warning(
                "User:{} :{}-{}".format(
                    update.message.chat.id, text, str(datetime.now())
                )
            )
            await update.message.reply_text(response)


# Error handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    error(
        "Update {} caused the following error {}-{}".format(
            update, context.error, str(datetime.now())
        )
    )


def main() -> None:
    warning("Bot is currently online-{}".format(str(datetime.now())))

    global feedback
    app = Application.builder().token(TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("activate", activate_command))
    app.add_handler(CommandHandler("deactivate", deactivate_command))
    app.add_handler(CommandHandler("delete", delete_command))
    app.add_handler(CommandHandler("my_class", my_class_command))
    app.add_handler(CommandHandler("contribute", contribute_command))
    app.add_handler(CommandHandler("fetchname", fetchname_command))
    app.add_handler(CommandHandler("fetchdate", fetchdate_command))
    app.add_handler(CommandHandler("fetchrange", fetchrange_command))
    app.add_handler(CommandHandler("create_class", create_class_command))
    app.add_handler(CommandHandler("delete_class", delete_class_command))
    app.add_handler(CommandHandler("join_class", join_class_command))
    app.add_handler(CommandHandler("leave_class", leave_class_command))
    app.add_handler(CommandHandler("open_source", open_source_command))
    app.add_handler(CommandHandler("commands", commands_command))
    app.add_handler(CommandHandler("feedback", feedback_command))
    app.add_handler(CommandHandler("enquiry", enquiry_command))
    app.add_handler(CommandHandler("dev", dev_command))
    app.add_handler(CommandHandler("cancel", cancel_command))

    # Message handlers
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Error handlers
    app.add_error_handler(error)

    # Polling
    warning("Bot is currently polling-{}".format(str(datetime.now())))
    try:
        app.run_polling(poll_interval=3)
    except:
        error("Bot is went offline-{}".format(str(datetime.now())))

    error("Bot is went offline-{}".format(str(datetime.now())))


if __name__ == "__main__":
    main()
