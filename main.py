from pymongo import MongoClient
import requests
import random
import os
import re
from re import IGNORECASE, escape, search
from telegram import Update
from telegram.error import TelegramError
from telegram.error import BadRequest
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, CommandHandler, filters as Filters, MessageHandler, CallbackQueryHandler
import telegram.ext as tg
import re
from telegram.ext import Application
import asyncio
from typing import Union, List, Dict, Callable, Generator, Any
import itertools
from collections.abc import Iterable
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton

from telegram import Chat, ChatMember, Update, User
from functools import wraps

from config import MONGO_URL, BOT_TOKEN, AI_API_KEY, AI_ID

BOT_TOKEN = BOT_TOKEN
MONGO_URL = MONGO_URL

AI_API_KEY = AI_API_KEY
AI_BID = AI_ID
USERS_GROUP = 11


application = Application.builder().token(BOT_TOKEN).build()
asyncio.get_event_loop().run_until_complete(application.bot.initialize())
BOT_ID = application.bot.id



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message
    keyb = []
    keyb.append([InlineKeyboardButton(text="ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ➕", url=f"http://t.me/{context.bot.username}?startgroup=true")])
    await msg.reply_text(f"ʜᴇʏᴀ\nɪ'ᴍ {context.bot.first_name}\nɪ ᴄᴀɴ ʜᴇʟᴘ ʏᴏᴜ ᴛᴏ ᴀᴄᴛɪᴠᴇ ʏᴏᴜʀ ᴄʜᴀᴛ", reply_markup=InlineKeyboardMarkup(keyb))


async def log_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
   chat = update.effective_chat
   message = update.effective_message
   try:
       if (
           message.text.startswith("!")
           or message.text.startswith("/")
           or message.text.startswith("?")
           or message.text.startswith("@")
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
           await message.reply_sticker(f"{hey}")
       if not Yo == "sticker":
           await message.reply_text(f"{hey}")
   if message.reply_to_message:                   
       if message.reply_to_message.from_user.id == BOT_ID:                    
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
               await message.reply_sticker(f"{hey}")
           if not Yo == "sticker":
               await message.reply_text(f"{hey}")
       if not message.reply_to_message.from_user.id == BOT_ID:          
           if message.sticker:
               is_chat = chatai.find_one({"chat":chat.id, "word": message.reply_to_message.text, "id": message.sticker.file_unique_id})
               if not is_chat:
                   chatai.insert_one({"chat":chat.id, "word": message.reply_to_message.text, "text": message.sticker.file_id, "check": "sticker", "id": message.sticker.file_unique_id})
           if message.text:                 
               is_chat = chatai.find_one({"chat":chat.id, "word": message.reply_to_message.text, "text": message.text})                 
               if not is_chat:
                   chatai.insert_one({"chat":chat.id, "word": message.reply_to_message.text, "text": message.text, "check": "none"})


START = CommandHandler(["start", "ping"], start, block=False)


USER_HANDLER = MessageHandler(
    Filters.ALL, log_user, block=False
)
application.add_handler(USER_HANDLER, USERS_GROUP)
application.add_handler(START)

print("INFO: BOTTING YOUR CLIENT")
application.run_polling()
