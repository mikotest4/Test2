from pyrogram import (
    Client,
    __version__
)
from pyrogram.raw.all import layer
from config import Config
import logging
from datetime import datetime
import logging.config, os
from pytz import timezone
from aiohttp import web
from plugins.web_support import web_server
import pyromod
import asyncio
from helper.database import db

logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)



class Bot (Client):

    def __init__(self):
        super().__init__(
            name="SnowEncoderBot",
            in_memory=True,
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            plugins={'root': 'plugins'}
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username
        
        # Check and remove expired premium users
        try:
            expired_count = await db.check_and_remove_expired_premium()
            if expired_count > 0:
                logging.info(f"Removed {expired_count} expired premium users")
        except Exception as e:
            logging.error(f"Error checking expired premium users: {e}")
        
        # Start periodic premium expiry check (every 6 hours)
        asyncio.create_task(self.periodic_premium_check())
        
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, Config.PORT).start()
        logging.info(f"✅ {me.first_name} with for Pyrogram v{__version__} (Layer {layer}) started on {me.username}. ✅")


        await self.send_message(Config.ADMIN, f"**__{me.first_name}  Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️__**")

        if Config.LOG_CHANNEL:
            try:
                curr = datetime.now(timezone("Asia/Kolkata"))
                date = curr.strftime('%d %B, %Y')
                time = curr.strftime('%I:%M:%S %p')
                await self.send_message(Config.LOG_CHANNEL, f"**__{me.mention} Iꜱ Rᴇsᴛᴀʀᴛᴇᴅ !!**\n\n📅 Dᴀᴛᴇ : `{date}`\n⏰ Tɪᴍᴇ : `{time}`\n🌐 Tɪᴍᴇᴢᴏɴᴇ : `Asia/Kolkata`\n\n🉐 Vᴇʀsɪᴏɴ : `v{__version__} (Layer {layer})`</b>")
            except:
                print("Pʟᴇᴀꜱᴇ Mᴀᴋᴇ Tʜɪꜱ Iꜱ Aᴅᴍɪɴ Iɴ Yᴏᴜʀ Lᴏɢ Cʜᴀɴɴᴇʟ")

    async def periodic_premium_check(self):
        """Periodically check and remove expired premium users"""
        while True:
            try:
                await asyncio.sleep(21600)  # Wait 6 hours
                expired_count = await db.check_and_remove_expired_premium()
                if expired_count > 0:
                    logging.info(f"Periodic check: Removed {expired_count} expired premium users")
            except Exception as e:
                logging.error(f"Error in periodic premium check: {e}")

    async def stop(self, *args):
        await super().stop()
        logging.info("Bot Stopped ⛔")


bot = Bot()
bot.run()
