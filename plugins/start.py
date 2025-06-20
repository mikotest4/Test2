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
from pyrogram.errors import FloodWait, MessageNotModified
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

    try:
        Snowdev = await msg.reply_text(text='**Please Wait...**', reply_to_message_id=msg.id)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        Snowdev = await msg.reply_text(text='**Please Wait...**', reply_to_message_id=msg.id)
    except Exception as e:
        print(f"Error sending initial message: {e}")
        return

    if msg.chat.type == enums.ChatType.SUPERGROUP and not await db.is_user_exist(msg.from_user.id):
        botusername = await bot.get_me()
        btn = [
            [InlineKeyboardButton(text='⚡ BOT PM', url=f'https://t.me/{botusername.username}')],
            [InlineKeyboardButton(text='💻 Dᴇᴠᴇʟᴏᴘᴇʀ', url='https://t.me/+6LwHBLWZc3IyMTU1')]
        ]
        try:
            await Snowdev.edit(text=Txt.GROUP_START_MSG.format(msg.from_user.mention), reply_markup=InlineKeyboardMarkup(btn))
        except (FloodWait, MessageNotModified) as e:
            if isinstance(e, FloodWait):
                await asyncio.sleep(e.value)
                try:
                    await Snowdev.edit(text=Txt.GROUP_START_MSG.format(msg.from_user.mention), reply_markup=InlineKeyboardMarkup(btn))
                except MessageNotModified:
                    pass
        except Exception as e:
            print(f"Error editing group start message: {e}")
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

        try:
            if Config.START_PIC:
                await Snowdev.delete()
                await msg.reply_photo(photo=Config.START_PIC, caption=start_text, reply_markup=InlineKeyboardMarkup(btn), reply_to_message_id=msg.id)
            else:
                await Snowdev.delete()
                await msg.reply_text(text=start_text, reply_markup=InlineKeyboardMarkup(btn), reply_to_message_id=msg.id)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                if Config.START_PIC:
                    await Snowdev.delete()
                    await msg.reply_photo(photo=Config.START_PIC, caption=start_text, reply_markup=InlineKeyboardMarkup(btn), reply_to_message_id=msg.id)
                else:
                    await Snowdev.delete()
                    await msg.reply_text(text=start_text, reply_markup=InlineKeyboardMarkup(btn), reply_to_message_id=msg.id)
            except Exception as e:
                print(f"Error after FloodWait retry: {e}")
        except Exception as e:
            print(f"Error sending start message: {e}")

@Client.on_message((filters.private | filters.group) & (filters.document | filters.audio | filters.video) & ~filters.sticker & ~filters.animation)
async def Files_Option(bot: Client, message: Message):
    user_id = message.from_user.id
    chat_type = message.chat.type
    
    # Check if it's a group and bot should reply
    is_in_group = chat_type in [enums.ChatType.SUPERGROUP, enums.ChatType.GROUP]
    
    try:
        if is_in_group:
            # In group: Reply to the message
            SnowDev = await message.reply_text(text='**🤖 Bot Detected File - Processing...**', reply_to_message_id=message.id)
        else:
            # In DM: Send normal message
            SnowDev = await message.reply_text(text='**Please Wait**', reply_to_message_id=message.id)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        if is_in_group:
            SnowDev = await message.reply_text(text='**🤖 Bot Detected File - Processing...**', reply_to_message_id=message.id)
        else:
            SnowDev = await message.reply_text(text='**Please Wait**', reply_to_message_id=message.id)
    except Exception as e:
        print(f"Error sending file detection message: {e}")
        return

    # Check if user is admin
    is_admin = user_id == Config.ADMIN
    is_premium = await db.is_premium_user(user_id)

    # New restriction logic - Only admin can encode in DM
    if not is_admin and not is_in_group:
        access_level = "👑 Premium User" if is_premium else "👤 Regular User"
        
        restriction_text = (
            f"**ʏᴏᴜ ᴄᴀɴ'ᴛ ᴜsᴇ ᴍᴇ ɪɴ ᴅᴍ ʏᴏᴜ ᴄᴀɴ ᴜsᴇ ᴍᴇ ʜᴇʀᴇ ᴊᴏɪɴ ᴀɴᴅ ᴜsᴇ :- **")
        
        try:
            return await SnowDev.edit(restriction_text)
        except (FloodWait, MessageNotModified) as e:
            if isinstance(e, FloodWait):
                await asyncio.sleep(e.value)
                try:
                    return await SnowDev.edit(restriction_text)
                except MessageNotModified:
                    return
        except Exception as e:
            print(f"Error editing restriction message: {e}")
            return

    if message.chat.type == enums.ChatType.SUPERGROUP and not await db.is_user_exist(message.from_user.id):
        botusername = await bot.get_me()
        btn = [
            [InlineKeyboardButton(text='⚡ BOT PM', url=f'https://t.me/{botusername.username}')],
            [InlineKeyboardButton(text='💻 Dᴇᴠᴇʟᴏᴘᴇʀ', url='https://t.me/+6LwHBLWZc3IyMTU1')]
        ]
        try:
            return await SnowDev.edit(text=Txt.GROUP_START_MSG.format(message.from_user.mention), reply_markup=InlineKeyboardMarkup(btn))
        except (FloodWait, MessageNotModified) as e:
            if isinstance(e, FloodWait):
                await asyncio.sleep(e.value)
                try:
                    return await SnowDev.edit(text=Txt.GROUP_START_MSG.format(message.from_user.mention), reply_markup=InlineKeyboardMarkup(btn))
                except MessageNotModified:
                    return
        except Exception as e:
            print(f"Error editing group message: {e}")
            return

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
                
                verification_text = (
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
                )
                
                try:
                    return await SnowDev.edit(
                        text=verification_text,
                        reply_markup=InlineKeyboardMarkup(btn)
                    )
                except (FloodWait, MessageNotModified) as e:
                    if isinstance(e, FloodWait):
                        await asyncio.sleep(e.value)
                        try:
                            return await SnowDev.edit(
                                text=verification_text,
                                reply_markup=InlineKeyboardMarkup(btn)
                            )
                        except MessageNotModified:
                            return
                except Exception as e:
                    print(f"Error editing verification message: {e}")
                    return
            except Exception as e:
                print(f"Verification link creation failed: {e}")
                try:
                    return await SnowDev.edit("❌ Failed to create verification link. Please try again later.")
                except (FloodWait, MessageNotModified) as e:
                    if isinstance(e, FloodWait):
                        await asyncio.sleep(e.value)
                        try:
                            return await SnowDev.edit("❌ Failed to create verification link. Please try again later.")
                        except MessageNotModified:
                            return
                except Exception as e:
                    print(f"Error editing error message: {e}")
                    return
        
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
        # Different message format for groups vs DMs
        if is_in_group:
            file_info = f"**🤖 File Detected & Ready for Processing**\n\n**📁 File Name:** `{filename}`\n**📊 File Size:** `{filesize}`\n\n**👤 User:** {message.from_user.mention}\n**🏷️ Access Level:** {access_level}\n**📍 Location:** {location}"
        else:
            file_info = f"**📁 File Information**\n\n**File Name:** `{filename}`\n**File Size:** `{filesize}`\n\n**👤 Access Level:** {access_level}\n**📍 Location:** {location}"
        
        btn = [[InlineKeyboardButton("📂 What do you want to do with this file?", callback_data="option")]]
        
        try:
            await SnowDev.edit(text=file_info, reply_markup=InlineKeyboardMarkup(btn))
        except (FloodWait, MessageNotModified) as e:
            if isinstance(e, FloodWait):
                await asyncio.sleep(e.value)
                try:
                    await SnowDev.edit(text=file_info, reply_markup=InlineKeyboardMarkup(btn))
                except MessageNotModified:
                    pass
        except Exception as e:
            print(f"Error editing file info message: {e}")

    except Exception as e:
        print(f"Error in Files_Option: {e}")
        try:
            await SnowDev.edit("❌ An error occurred while processing your file.")
        except (FloodWait, MessageNotModified) as e:
            if isinstance(e, FloodWait):
                await asyncio.sleep(e.value)
                try:
                    await SnowDev.edit("❌ An error occurred while processing your file.")
                except MessageNotModified:
                    pass
        except Exception as e:
            print(f"Error editing error message: {e}")
