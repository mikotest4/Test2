import asyncio
import shutil
import humanize
import time
import datetime
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
                f"🎬 You can now send video files to encode them in groups!",
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
            [InlineKeyboardButton(text='💻 Dᴇᴠᴇʟᴏᴘᴇʀ', url='https://t.me/+6LwHBLWZc3IyMTU1')]
        ]
        await Snowdev.edit(text=Txt.GROUP_START_MSG.format(msg.from_user.mention), reply_markup=InlineKeyboardMarkup(btn))
    else:
        # Check if user is premium and show premium indicator
        is_premium = await db.is_premium_user(user_id)
        is_admin = user_id == Config.ADMIN
        
        if is_admin:
            status_text = "👨‍💼 **ADMIN USER** - Full Access Everywhere"
        elif is_premium:
            status_text = "👑 **PREMIUM USER** - Group Access (No Verification)"
        else:
            status_text = "👤 **REGULAR USER** - Group Access (Verification Required)"
        
        btn = [
            [InlineKeyboardButton(text='❗ Hᴇʟᴘ', callback_data='help'), InlineKeyboardButton(text='🌨️ Aʙᴏᴜᴛ', callback_data='about')],
            [InlineKeyboardButton(text='📢 Uᴘᴅᴀᴛᴇs', url='https://t.me/+6LwHBLWZc3IyMTU1'), InlineKeyboardButton(text='💻 Dᴇᴠᴇʟᴏᴘᴇʀ', url='https://t.me/+6LwHBLWZc3IyMTU1')]
        ]

        start_text = f"{status_text}\n\n{Txt.PRIVATE_START_MSG.format(msg.from_user.mention)}"

        if Config.START_PIC:
            await Snowdev.delete()
            await msg.reply_photo(photo=Config.START_PIC, caption=start_text, reply_markup=InlineKeyboardMarkup(btn), reply_to_message_id=msg.id)
        else:
            await Snowdev.delete()
            await msg.reply_text(text=start_text, reply_markup=InlineKeyboardMarkup(btn), reply_to_message_id=msg.id)

@Client.on_message((filters.private | filters.group) & (filters.document | filters.audio | filters.video))
async def Files_Option(bot: Client, message: Message):
    user_id = message.from_user.id
    chat_type = message.chat.type
    
    SnowDev = await message.reply_text(text='**Please Wait**', reply_to_message_id=message.id)

    # Check if user is admin
    is_admin = user_id == Config.ADMIN
    is_premium = await db.is_premium_user(user_id)
    is_in_group = chat_type in [enums.ChatType.SUPERGROUP, enums.ChatType.GROUP]

    # New restriction logic - Only admin can encode in DM
    if not is_admin and not is_in_group:
        access_level = "👑 Premium User" if is_premium else "👤 Regular User"
        
        return await SnowDev.edit(
            f"🚫 **DM Encoding Restricted**\n\n"
            f"**Your Access Level:** {access_level}\n"
            f"**Current Location:** 📱 Private Chat\n\n"
            f"**Only Admin can encode in DM.**\n"
            f"**All other users must use groups for encoding.**\n\n"
            f"**How to encode:**\n"
            f"• Add me to a group\n"
            f"• Give me admin permissions\n"
            f"• Send your file in the group\n\n"
            f"**Want DM access?** Only available for Bot Admin."
        )

    if message.chat.type == enums.ChatType.SUPERGROUP and not await db.is_user_exist(message.from_user.id):
        botusername = await bot.get_me()
        btn = [
            [InlineKeyboardButton(text='⚡ BOT PM', url=f'https://t.me/{botusername.username}')],
            [InlineKeyboardButton(text='💻 Dᴇᴠᴇʟᴏᴘᴇʀ', url='https://t.me/+6LwHBLWZc3IyMTU1')]
        ]
        return await SnowDev.edit(text=Txt.GROUP_START_MSG.format(message.from_user.mention), reply_markup=InlineKeyboardMarkup(btn))

    # Verification check - Admin bypass, Premium bypass, Regular users need verification
    if not is_admin and not is_premium:
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
                        f"You need to verify yourself before encoding videos in groups.\n\n"
                        f"⏱️ **Token Validity:** {get_exp_time(Config.VERIFY_EXPIRE)}\n\n"
                        f"**How to verify:**\n"
                        f"1. Click '🔗 ᴠᴇʀɪғʏ ɴᴏᴡ' button\n"
                        f"2. Complete the verification process\n"
                        f"3. Return to bot and send /start\n"
                        f"4. Send your file again\n\n"
                        f"**Note:** This helps support the bot through ads.\n\n"
                        f"💡 **Get premium to skip verification!**"
                    ),
                    reply_markup=InlineKeyboardMarkup(btn)
                )
            except Exception as e:
                print(f"Verification link creation failed: {e}")
                return await SnowDev.edit("❌ Failed to create verification link. Please try again later.")
        
    file = getattr(message, message.media.value)
    filename = file.file_name
    filesize = humanize.naturalsize(file.file_size)
    
    # Enhanced access level display
    if is_admin:
        access_level = "👨‍💼 Admin (Full Access)"
    elif is_premium:
        access_level = "👑 Premium (No Verification)"
    else:
        access_level = "👤 Regular (Verification Required)"
        
    location = "💬 Group Chat" if is_in_group else "📱 Private Chat"
    
    try:
        file_info = f"**📁 File Information**\n\n**File Name:** `{filename}`\n**File Size:** `{filesize}`\n\n**👤 Access Level:** {access_level}\n**📍 Location:** {location}"
        
        btn = [[InlineKeyboardButton("📂 What do you want to do with this file?", callback_data="option")]]
        
        await SnowDev.edit(text=file_info, reply_markup=InlineKeyboardMarkup(btn))

    except Exception as e:
        print(f"Error in Files_Option: {e}")
        await SnowDev.edit("❌ An error occurred while processing your file.")
