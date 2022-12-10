from pymongo import MongoClient
import requests
import random
import os
import re
from re import IGNORECASE, escape, search
from telegram import TelegramError, Update
from telegram.error import BadRequest
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, CallbackQueryHandler
import telegram.ext as tg
import re
import asyncio

from typing import Union, List, Dict, Callable, Generator, Any
import itertools
from collections.abc import Iterable
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from cachetools import TTLCache
from telegram import Chat, ChatMember, ParseMode, Update, TelegramError, User
from functools import wraps
from config import BOT_ID, BOT_TOKEN, AI_API_KEY, AI_ID

BOT_TOKEN = BOT_TOKEN
BOT_ID = BOT_ID


AI_API_KEY = AI_API_KEY
AI_BID = AI_ID
USERS_GROUP = 11


updater = tg.Updater(BOT_TOKEN, workers=32, use_context=True)
dispatcher = updater.dispatcher


def start(update: Update, _) -> None:
    chat = update.effective_chat
    msg = update.effective_message
    keyb = []
    keyb.append([InlineKeyboardButton(text="Add me ➕", url="http://t.me/MrsNiaBot?startgroup=true")])
    msg.reply_text("Heya\nI'm Nia\nI can help you to active your Chat", reply_markup=InlineKeyboardMarkup(keyb))


def log_user(update: Update, context: CallbackContext):
   chat = update.effective_chat
   message = update.effective_message
   try:
       if (
           message.text.startswith("!")
           or message.text.startswith("/")
           or message.text.startswith("?")
           or message.text.startswith("#")
       ):
           return
   except Exception:
       pass
   if not message.reply_to_message:
           r = requests.get(f"http://api.brainshop.ai/get?bid={AI_BID}&uid={message.from_user.id}&key={AI_API_KEY}&msg={message.text}")
           hey = r.json()["cnt"]
           message.reply_sticker(f"{hey}")
   if message.reply_to_message:                   
       if message.reply_to_message.from_user.id == BOT_ID:                    
               r = requests.get(f"http://api.brainshop.ai/get?bid={AI_BID}&uid={message.from_user.id}&key={AI_API_KEY}&msg={message.text}")
               hey = r.json()["cnt"]
               message.reply_sticker(f"{hey}")

START = CommandHandler(["start", "ping"], start)


USER_HANDLER = MessageHandler(
    Filters.all, log_user, run_async=True
)
dispatcher.add_handler(USER_HANDLER, USERS_GROUP)
dispatcher.add_handler(START)

print("INFO: BOTTING YOUR CLIENT")
updater.start_polling()
