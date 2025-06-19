import asyncio
import shutil
import humanize
import time
from time import sleep
from config import Config
from script import Txt
from helper.database import db
from helper_func import is_user_verified, create_verification_link, get_exp_time
from pyrogram.errors import FloodWait
from pyrogram import Client, filters, enums
from .check_user_status import handle_user_status
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

@Client.on_message((filters.private | filters.group))
async def _(bot: Client, cmd: Message):
    await handle_user_status(bot, cmd)

@Client.on_message((filters.private | filters.group) & filters.command('start'))
async def Handle_StartMsg(bot: Client, msg: Message):
    user_id = msg.from_user.id
    
    # Handle verification callback
    if len(msg.text) > 7 and "verify_" in msg.text:
        try:
            _, token = msg.text.split("verify_", 1)
            verify_status = await db.get_verify_status(user_id)
            
            if verify_status['verify_token'] != token:
                return await msg.reply_text(
                    "❌ **Invalid Token**\n\n"
                    "Your verification token is invalid or expired.\n"
                    "Please send a file to get a new verification link.",
                    quote=True
                )
            
            # Mark as verified
            await db.update_verify_status(user_id, is_verified=True, verified_time=time.time())
            
            return await msg.reply_text(
                f"✅ **Verification Successful!**\n\n"
                f"Your token has been verified and is valid for **{get_exp_time(Config.VERIFY_EXPIRE)}**.\n\n"
                f"🎬 You can now send video files to encode them!",
                quote=True
            )
        except Exception as e:
            print(f"Verification error: {e}")
            pass

    Snowdev = await msg.reply_text(text='**Please Wait...**', reply_to_message_id=msg.id)

    if msg.chat.type == enums.ChatType.SUPERGROUP and not await db.is_user_exist(msg.from_user.id):
        botusername = await bot.get_me()
        btn = [
            [InlineKeyboardButton(text='⚡ BOT PM', url=f'https://t.me/{botusername.username}')],
            [InlineKeyboardButton('💝 movies ', url='https://t.me/aapna_Movies')],
            [InlineKeyboardButton(text='💻 Dᴇᴠᴇʟᴏᴘᴇʀ', url='https://t.me/+6LwHBLWZc3IyMTU1')]
        ]
        await Snowdev.edit(text=Txt.GROUP_START_MSG.format(msg.from_user.mention), reply_markup=InlineKeyboardMarkup(btn))
    else:
        btn = [
            [InlineKeyboardButton(text='❗ Hᴇʟᴘ', callback_data='help'), InlineKeyboardButton(text='🌨️ Aʙᴏᴜᴛ', callback_data='about')],
            [InlineKeyboardButton('💝 movies ', url='https://t.me/aapna_Movies')],
            [InlineKeyboardButton(text='📢 Uᴘᴅᴀᴛᴇs', url='https://t.me/+6LwHBLWZc3IyMTU1'), InlineKeyboardButton(text='💻 Dᴇᴠᴇʟᴏᴘᴇʀ', url='https://t.me/+6LwHBLWZc3IyMTU1')]
        ]

        if Config.START_PIC:
            await Snowdev.delete()
            await msg.reply_photo(photo=Config.START_PIC, caption=Txt.PRIVATE_START_MSG.format(msg.from_user.mention), reply_markup=InlineKeyboardMarkup(btn), reply_to_message_id=msg.id)
        else:
            await Snowdev.delete()
            await msg.reply_text(text=Txt.PRIVATE_START_MSG.format(msg.from_user.mention), reply_markup=InlineKeyboardMarkup(btn), reply_to_message_id=msg.id)

@Client.on_message((filters.private | filters.group) & (filters.document | filters.audio | filters.video))
async def Files_Option(bot: Client, message: Message):
    user_id = message.from_user.id
    
    SnowDev = await message.reply_text(text='**Please Wait**', reply_to_message_id=message.id)

    if message.chat.type == enums.ChatType.SUPERGROUP and not await db.is_user_exist(message.from_user.id):
        botusername = await bot.get_me()
        btn = [
            [InlineKeyboardButton(text='⚡ BOT PM', url=f'https://t.me/{botusername.username}')],
            [InlineKeyboardButton('💝 movies ', url='https://t.me/aapna_Movies')],
            [InlineKeyboardButton(text='💻 Dᴇᴠᴇʟᴏᴘᴇʀ', url='https://t.me/+6LwHBLWZc3IyMTU1')]
        ]
        return await SnowDev.edit(text=Txt.GROUP_START_MSG.format(message.from_user.mention), reply_markup=InlineKeyboardMarkup(btn))

    # Check if user is admin (skip verification for admins)
    if user_id != Config.ADMIN:
        # Check verification status
        if not await is_user_verified(user_id, db):
            try:
                botusername = (await bot.get_me()).username
                verification_link = await create_verification_link(user_id, botusername, db)
                
                btn = [
                    [InlineKeyboardButton("🔗 ᴠᴇʀɪғʏ ɴᴏᴡ", url=verification_link)],
                    [InlineKeyboardButton('📺 ᴛᴜᴛᴏʀɪᴀʟ', url=Config.TUT_VID)]
                ]
                
                return await SnowDev.edit(
                    text=(
                        f"🔒 **Verification Required**\n\n"
                        f"You need to verify yourself before encoding videos.\n\n"
                        f"⏱️ **Token Validity:** {get_exp_time(Config.VERIFY_EXPIRE)}\n\n"
                        f"**How to verify:**\n"
                        f"1. Click '🔗 ᴠᴇʀɪғʏ ɴᴏᴡ' button\n"
                        f"2. Complete the verification process\n"
                        f"3. Return to bot and send /start\n"
                        f"4. Send your file again\n\n"
                        f"**Note:** This helps support the bot through ads."
                    ),
                    reply_markup=InlineKeyboardMarkup(btn)
                )
            except Exception as e:
                print(f"Verification link creation failed: {e}")
                return await SnowDev.edit("❌ Failed to create verification link. Please try again later.")
        
    file = getattr(message, message.media.value)
    filename = file.file_name
    filesize = humanize.naturalsize(file.file_size)

    try:
        text = f"""**__What do you want me to do with this file.?__**\n\n**File Name** :- `{filename}`\n\n**File Size** :- `{filesize}`"""

        buttons = [
            [InlineKeyboardButton("Rᴇɴᴀᴍᴇ 📝", callback_data=f"rename-{message.from_user.id}")],
            [InlineKeyboardButton('💝 movies ', url='https://t.me/aapna_Movies')],
            [InlineKeyboardButton("Cᴏᴍᴘʀᴇss 🗜️", callback_data=f"compress-{message.from_user.id}")]
        ]
        await SnowDev.edit(text=text, reply_markup=InlineKeyboardMarkup(buttons))
        
    except FloodWait as e:
        floodmsg = await message.reply_text(f"**😥 Pʟᴇᴀsᴇ Wᴀɪᴛ ᴅᴏɴ'ᴛ ᴅᴏ ғʟᴏᴏᴅɪɴɢ ᴡᴀɪᴛ ғᴏʀ {e.value} Sᴇᴄᴄᴏɴᴅs**", reply_to_message_id=message.id)
        await sleep(e.value)
        await floodmsg.delete()

        text = f"""**__What do you want me to do with this file.?__**\n\n**File Name** :- `{filename}`\n\n**File Size** :- `{filesize}`"""
        buttons = [
            [InlineKeyboardButton("Rᴇɴᴀᴍᴇ 📝", callback_data=f"rename-{message.from_user.id}")],
            [InlineKeyboardButton('💝 movies ', url='https://t.me/aapna_Movies')],
            [InlineKeyboardButton("Cᴏᴍᴘʀᴇss 🗜️", callback_data=f"compress-{message.from_user.id}")]
        ]
        await SnowDev.edit(text=text, reply_markup=InlineKeyboardMarkup(buttons))

    except Exception as e:
        print(e)

@Client.on_message((filters.private | filters.group) & filters.command('cancel'))
async def cancel_process(bot: Client, message: Message):
    try:
        shutil.rmtree(f"encode/{message.from_user.id}")
        shutil.rmtree(f"ffmpeg/{message.from_user.id}")
        shutil.rmtree(f"Renames/{message.from_user.id}")
        shutil.rmtree(f"Metadata/{message.from_user.id}")
        shutil.rmtree(f"Screenshot_Generation/{message.from_user.id}")
        
        return await message.reply_text(text="**Canceled All On Going Processes ✅**")
    except BaseException:
        pass

# Add verification status command
@Client.on_message(filters.command('verify_status') & filters.private)
async def check_verify_status(bot: Client, message: Message):
    user_id = message.from_user.id
    verify_status = await db.get_verify_status(user_id)
    
    if verify_status['is_verified']:
        verified_time = verify_status.get('verified_time', 0)
        remaining_time = Config.VERIFY_EXPIRE - (time.time() - verified_time)
        
        if remaining_time > 0:
            await message.reply_text(
                f"✅ **Verification Status: Active**\n\n"
                f"⏱️ **Time Remaining:** {get_exp_time(int(remaining_time))}\n\n"
                f"🎬 You can encode videos without restrictions.",
                quote=True
            )
        else:
            await message.reply_text(
                f"❌ **Verification Status: Expired**\n\n"
                f"Please send a file to get a new verification link.",
                quote=True
            )
    else:
        await message.reply_text(
            f"❌ **Verification Status: Not Verified**\n\n"
            f"Please send a file to get a verification link.",
            quote=True
        )
