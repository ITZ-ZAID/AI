from os import getenv

BOT_TOKEN = getenv("BOT_TOKEN", "")
MONGO_URL = getenv("MONGO_URL", "")
BOT_ID = getenv("BOT_ID", "")#token first 10 digits
AI_API_KEY = getenv("AI_API_KEY", "")
AI_ID = int(getenv("AI_ID", ""))
