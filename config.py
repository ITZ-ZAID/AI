from os import getenv

BOT_TOKEN = getenv("BOT_TOKEN", "")
MONGO_URL = getenv("MONGO_URL", "")
AI_API_KEY = getenv("AI_API_KEY", "")
AI_ID = int(getenv("AI_ID", ""))
