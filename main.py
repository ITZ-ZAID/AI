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
from config import MONGO_URL, BOT_TOKEN, AI_API_KEY, AI_ID

BOT_TOKEN = BOT_TOKEN
MONGO_URL = MONGO_URL

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
   chatdb = MongoClient(MONGO_URL)
   chatai = chatdb["Word"]["WordDb"]
   if not message.reply_to_message:
       K = []  
       is_chat = chatai.find({"chat":chat.id, "word": message.text})                 
       for x in is_chat:
           K.append(x['text'])
       if K:
           hey = random.choice(K)
           is_text = chatai.find_one({"chat":chat.id, "text": hey})
           Yo = is_text['check']
       else:
           r = requests.get(f"http://api.brainshop.ai/get?bid={AI_BID}&uid={message.from_user.id}&key={AI_API_KEY}&msg={message.text}")
           hey = r.json()["cnt"]
           Yo = None
       if Yo == "sticker": 
           message.reply_sticker(f"{hey}")
       if not Yo == "sticker":
           message.reply_text(f"{hey}")
   if message.reply_to_message:                   
       if message.reply_to_message.from_user.id == 5338777856:                    
           K = []  
           is_chat = chatai.find({"chat":chat.id, "word": message.text})                 
           for x in is_chat:
               K.append(x['text'])
           if K:
               hey = random.choice(K)
               is_text = chatai.find_one({"chat":chat.id, "text": hey})
               Yo = is_text['check']
           else:
               r = requests.get(f"http://api.brainshop.ai/get?bid={AI_BID}&uid={message.from_user.id}&key={AI_API_KEY}&msg={message.text}")
               hey = r.json()["cnt"]
               Yo = None
           if Yo == "sticker":
               message.reply_sticker(f"{hey}")
           if not Yo == "sticker":
               message.reply_text(f"{hey}")
       if not message.reply_to_message.from_user.id == 5338777856:          
           if message.sticker:
               is_chat = chatai.find_one({"chat":chat.id, "word": message.reply_to_message.text, "id": message.sticker.file_unique_id})
               if not is_chat:
                   chatai.insert_one({"chat":chat.id, "word": message.reply_to_message.text, "text": message.sticker.file_id, "check": "sticker", "id": message.sticker.file_unique_id})
           if message.text:                 
               is_chat = chatai.find_one({"chat":chat.id, "word": message.reply_to_message.text, "text": message.text})                 
               if not is_chat:
                   chatai.insert_one({"chat":chat.id, "word": message.reply_to_message.text, "text": message.text, "check": "none"})


START = CommandHandler(["start", "ping"], start)


USER_HANDLER = MessageHandler(
    Filters.all, log_user, run_async=True
)
dispatcher.add_handler(USER_HANDLER, USERS_GROUP)
dispatcher.add_handler(START)

print("INFO: BOTTING YOUR CLIENT")
updater.start_polling()
