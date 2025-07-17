import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait, RPCError

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
BOT_TOKEN = os.environ["BOT_TOKEN"]
SOURCE_CHAT_ID = int(os.environ["SOURCE_CHAT_ID"])
DEST_CHAT_ID = int(os.environ["DEST_CHAT_ID"])

app = Client("forward_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def safe_forward(message: Message):
    retries = 5
    for attempt in range(retries):
        try:
            if message.media:
                await message.copy(chat_id=DEST_CHAT_ID, caption="")
                print(f"✅ Forwarded media ID: {message.message_id}")
                return True
        except FloodWait as e:
            print(f"⏳ FloodWait: sleeping for {e.value} seconds.")
            await asyncio.sleep(e.value)
        except RPCError as e:
            print(f"⚠️ RPC Error: {e}. Retrying ({attempt+1}/{retries})...")
            await asyncio.sleep(3)
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
    return False

@app.on_message(filters.chat(SOURCE_CHAT_ID))
async def handle_message(client, message: Message):
    await safe_forward(message)

app.run()
