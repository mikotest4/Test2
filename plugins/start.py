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
                    "**ɪɴᴠᴀʟɪᴅ ᴛᴏᴋᴇɴ**\n\n"
                    "ʏᴏᴜʀ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ᴛᴏᴋᴇɴ ɪs ɪɴᴠᴀʟɪᴅ ᴏʀ ᴇxᴘɪʀᴇᴅ.\n"
                    "ᴘʟᴇᴀsᴇ sᴇɴᴅ ᴀ ғɪʟᴇ ᴛᴏ ɢᴇᴛ ᴀ ɴᴇᴡ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ʟɪɴᴋ.",
                    quote=True
                )
            
            # Mark as verified
            await db.update_verify_status(user_id, is_verified=True, verified_time=time.time())
            
            return await msg.reply_text(
                f"**ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ sᴜᴄᴄᴇssғᴜʟ!**\n"
                f"ʏᴏᴜʀ ᴛᴏᴋᴇɴ ʜᴀs ʙᴇᴇɴ ᴠᴇʀɪғɪᴇᴅ ᴀɴᴅ ɪs ᴠᴀʟɪᴅ ғᴏʀ **{get_exp_time(Config.VERIFY_EXPIRE)}**",
                quote=True
            )
        except Exception as e:
            print(f"Verification error: {e}")
            pass

    try:
        Snowdev = await msg.reply_text(text='**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...**', reply_to_message_id=msg.id)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        Snowdev = await msg.reply_text(text='**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...**', reply_to_message_id=msg.id)
    except Exception as e:
        print(f"Error sending initial message: {e}")
        return

    if msg.chat.type == enums.ChatType.SUPERGROUP and not await db.is_user_exist(msg.from_user.id):
        botusername = await bot.get_me()
        btn = [
            [InlineKeyboardButton(text='ʙᴏᴛ ᴘᴍ', url=f'https://t.me/{botusername.username}')],
            [InlineKeyboardButton(text='ᴅᴇᴠᴇʟᴏᴘᴇʀ', url='https://t.me/+6LwHBLWZc3IyMTU1')]
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
            status_text = "ᴀᴅᴍɪɴ ᴜsᴇʀ - ғᴜʟʟ ᴀᴄᴄᴇss ᴇᴠᴇʀʏᴡʜᴇʀᴇ"
        elif is_premium:
            status_text = "ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀ - ɢʀᴏᴜᴘ ᴀᴄᴄᴇss (ɴᴏ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ)"
        else:
            status_text = "ʀᴇɢᴜʟᴀʀ ᴜsᴇʀ - ɢʀᴏᴜᴘ ᴀᴄᴄᴇss (ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ʀᴇǫᴜɪʀᴇᴅ)"
        
        btn = [
            [InlineKeyboardButton(text='ʜᴇʟᴘ', callback_data='help'), InlineKeyboardButton(text='ᴀʙᴏᴜᴛ', callback_data='about')],
            [InlineKeyboardButton(text='ᴜᴘᴅᴀᴛᴇs', url='https://t.me/+6LwHBLWZc3IyMTU1'), InlineKeyboardButton(text='ᴅᴇᴠᴇʟᴏᴘᴇʀ', url='https://t.me/+6LwHBLWZc3IyMTU1')]
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
            SnowDev = await message.reply_text(text='**ʙᴏᴛ ᴅᴇᴛᴇᴄᴛᴇᴅ ғɪʟᴇ - ᴘʀᴏᴄᴇssɪɴɢ...**', reply_to_message_id=message.id)
        else:
            # In DM: Send normal message
            SnowDev = await message.reply_text(text='**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ**', reply_to_message_id=message.id)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        if is_in_group:
            SnowDev = await message.reply_text(text='**ʙᴏᴛ ᴅᴇᴛᴇᴄᴛᴇᴅ ғɪʟᴇ - ᴘʀᴏᴄᴇssɪɴɢ...**', reply_to_message_id=message.id)
        else:
            SnowDev = await message.reply_text(text='**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ**', reply_to_message_id=message.id)
    except Exception as e:
        print(f"Error sending file detection message: {e}")
        return

    # Check if user is admin
    is_admin = user_id == Config.ADMIN
    is_premium = await db.is_premium_user(user_id)

    # New restriction logic - Only admin can encode in DM
    if not is_admin and not is_in_group:
        access_level = "ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀ" if is_premium else "ʀᴇɢᴜʟᴀʀ ᴜsᴇʀ"
        
        restriction_text = (f"**ʏᴏᴜ ᴄᴀɴ'ᴛ ᴜsᴇ ᴍᴇ ɪɴ ᴅᴍ. ᴜsᴇ ᴍᴇ ʜᴇʀᴇ :-  **")
        
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
            [InlineKeyboardButton(text='ʙᴏᴛ ᴘᴍ', url=f'https://t.me/{botusername.username}')],
            [InlineKeyboardButton(text='ᴅᴇᴠᴇʟᴏᴘᴇʀ', url='https://t.me/+6LwHBLWZc3IyMTU1')]
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
                    [InlineKeyboardButton("ᴠᴇʀɪғʏ ɴᴏᴡ", url=verification_link)],
                    [InlineKeyboardButton('ᴛᴜᴛᴏʀɪᴀʟ', url=Config.TUT_VID)]
                ]
                
                verification_text = (
                    f"**ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ʀᴇǫᴜɪʀᴇᴅ**\n\n"
                    f"ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ᴠᴇʀɪғʏ ʏᴏᴜʀsᴇʟғ ʙᴇғᴏʀᴇ ᴇɴᴄᴏᴅɪɴɢ ᴠɪᴅᴇᴏs ɪɴ ɢʀᴏᴜᴘs.\n\n"
                    f"**ᴛᴏᴋᴇɴ ᴠᴀʟɪᴅɪᴛʏ:** {get_exp_time(Config.VERIFY_EXPIRE)}\n\n"
                    f"**ʜᴏᴡ ᴛᴏ ᴠᴇʀɪғʏ:**\n"
                    f"1. ᴄʟɪᴄᴋ 'ᴠᴇʀɪғʏ ɴᴏᴡ' ʙᴜᴛᴛᴏɴ\n"
                    f"2. ᴄᴏᴍᴘʟᴇᴛᴇ ᴛʜᴇ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ᴘʀᴏᴄᴇss\n"
                    f"3. ʀᴇᴛᴜʀɴ ᴛᴏ ʙᴏᴛ ᴀɴᴅ sᴇɴᴅ /start\n"
                    f"4. sᴇɴᴅ ʏᴏᴜʀ ғɪʟᴇ ᴀɢᴀɪɴ\n\n"
                    f"**ɴᴏᴛᴇ:** ᴛʜɪs ʜᴇʟᴘs sᴜᴘᴘᴏʀᴛ ᴛʜᴇ ʙᴏᴛ ᴛʜʀᴏᴜɢʜ ᴀᴅs.\n\n"
                    f"**ɢᴇᴛ ᴘʀᴇᴍɪᴜᴍ ᴛᴏ sᴋɪᴘ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ! ᴅᴍ @Yae_x_Miko**"
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
                    return await SnowDev.edit("**ғᴀɪʟᴇᴅ ᴛᴏ ᴄʀᴇᴀᴛᴇ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ʟɪɴᴋ. ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ.**")
                except (FloodWait, MessageNotModified) as e:
                    if isinstance(e, FloodWait):
                        await asyncio.sleep(e.value)
                        try:
                            return await SnowDev.edit("**ғᴀɪʟᴇᴅ ᴛᴏ ᴄʀᴇᴀᴛᴇ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ʟɪɴᴋ. ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ.**")
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
        access_level = "ᴀᴅᴍɪɴ (ғᴜʟʟ ᴀᴄᴄᴇss)"
    elif is_premium:
        access_level = "ᴘʀᴇᴍɪᴜᴍ (ɴᴏ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ)"
    else:
        access_level = "ʀᴇɢᴜʟᴀʀ (ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ʀᴇǫᴜɪʀᴇᴅ)"
        
    location = "ɢʀᴏᴜᴘ ᴄʜᴀᴛ" if is_in_group else "ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ"
    
    try:
        # Different message format for groups vs DMs
        if is_in_group:
            file_info = f"**ʙᴏᴛ ᴅᴇᴛᴇᴄᴛᴇᴅ & ʀᴇᴀᴅʏ ғᴏʀ ᴘʀᴏᴄᴇssɪɴɢ**\n\n**ғɪʟᴇ ɴᴀᴍᴇ:** `{filename}`\n**ғɪʟᴇ sɪᴢᴇ:** `{filesize}`\n\n**ᴜsᴇʀ:** {message.from_user.mention}\n**ᴀᴄᴄᴇss ʟᴇᴠᴇʟ:** {access_level}\n**ʟᴏᴄᴀᴛɪᴏɴ:** {location}"
        else:
            file_info = f"**ғɪʟᴇ ɪɴғᴏʀᴍᴀᴛɪᴏɴ**\n\n**ғɪʟᴇ ɴᴀᴍᴇ:** `{filename}`\n**ғɪʟᴇ sɪᴢᴇ:** `{filesize}`\n\n**ᴀᴄᴄᴇss ʟᴇᴠᴇʟ:** {access_level}\n**ʟᴏᴄᴀᴛɪᴏɴ:** {location}"
        
        btn = [[InlineKeyboardButton("ᴄʟɪᴄᴋ ʜᴇʀᴇ", callback_data="option")]]
        
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
            await SnowDev.edit("**ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ ᴘʀᴏᴄᴇssɪɴɢ ʏᴏᴜʀ ғɪʟᴇ.**")
        except (FloodWait, MessageNotModified) as e:
            if isinstance(e, FloodWait):
                await asyncio.sleep(e.value)
                try:
                    await SnowDev.edit("**ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ ᴘʀᴏᴄᴇssɪɴɢ ʏᴏᴜʀ ғɪʟᴇ.**")
                except MessageNotModified:
                    pass
        except Exception as e:
            print(f"Error editing error message: {e}")
