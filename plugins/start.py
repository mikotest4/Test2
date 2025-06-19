import asyncio
import shutil
import humanize
import time
from time import sleep
from config import Config
from script import Txt
from helper.database import db
from helper_func import is_user_verified, create_verification_link, get_exp_time, check_queue_and_process, finish_processing
from database.db_premium import is_premium_user
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
        # Check if user is premium for different welcome message
        is_premium = await is_premium_user(user_id)
        is_admin = user_id == Config.ADMIN
        
        if is_premium or is_admin:
            status_text = "👑 Admin" if is_admin else "⭐ Premium User"
            welcome_addon = f"\n\n{status_text} - Enjoy unlimited access!"
        else:
            welcome_addon = f"\n\n🆓 Free User - Upgrade to premium for unlimited access!"
        
        btn = [
            [InlineKeyboardButton(text='❗ Hᴇʟᴘ', callback_data='help'), InlineKeyboardButton(text='🌨️ Aʙᴏᴜᴛ', callback_data='about')],
            [InlineKeyboardButton('💝 movies ', url='https://t.me/aapna_Movies')],
            [InlineKeyboardButton(text='📢 Uᴘᴅᴀᴛᴇs', url='https://t.me/+6LwHBLWZc3IyMTU1'), InlineKeyboardButton(text='💻 Dᴇᴠᴇʟᴏᴘᴇʀ', url='https://t.me/+6LwHBLWZc3IyMTU1')]
        ]
        
        # Add premium-specific buttons
        if is_premium or is_admin:
            btn.insert(1, [InlineKeyboardButton("📊 Queue Status", callback_data="queue_status"), InlineKeyboardButton("💎 My Plan", callback_data="my_plan")])

        if Config.START_PIC:
            await Snowdev.delete()
            await msg.reply_photo(photo=Config.START_PIC, caption=Txt.PRIVATE_START_MSG.format(msg.from_user.mention) + welcome_addon, reply_markup=InlineKeyboardMarkup(btn), reply_to_message_id=msg.id)
        else:
            await Snowdev.delete()
            await msg.reply_text(text=Txt.PRIVATE_START_MSG.format(msg.from_user.mention) + welcome_addon, reply_markup=InlineKeyboardMarkup(btn), reply_to_message_id=msg.id)

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

    # Check if user is admin or premium (skip verification)
    is_admin = user_id == Config.ADMIN
    is_premium = await is_premium_user(user_id)
    
    if not is_admin and not is_premium:
        # Check verification status for free users
        if not await is_user_verified(user_id, db):
            try:
                botusername = (await bot.get_me()).username
                verification_link = await create_verification_link(user_id, botusername, db)
                
                btn = [
                    [InlineKeyboardButton("🔗 ᴠᴇʀɪғʏ ɴᴏᴡ", url=verification_link)],
                    [InlineKeyboardButton('📺 ᴛᴜᴛᴏʀɪᴀʟ', url=Config.TUT_VID)],
                    [InlineKeyboardButton("💎 Get Premium", callback_data="get_premium")]
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
                        f"💡 **Or upgrade to Premium** to skip verification forever!"
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
        # Check queue and processing limits
        can_process_now, queue_message = await check_queue_and_process(user_id, file, message, "encode")
        
        # Update database stats
        await db.update_queue_stats(user_id, increment_queued=True)
        
        # Prepare status message
        if is_admin:
            user_status = "👑 **Admin** - Unlimited Access"
        elif is_premium:
            user_status = f"⭐ **Premium** - Up to {Config.MAX_CONCURRENT_PREMIUM} concurrent files"
        else:
            user_status = f"🆓 **Free** - {Config.MAX_CONCURRENT_NON_PREMIUM} file at a time"
        
        text = f"""**__What do you want me to do with this file?__**

**File Name:** `{filename}`
**File Size:** `{filesize}`

**Your Status:** {user_status}
**Queue Status:** {queue_message}"""

        buttons = [
            [InlineKeyboardButton("Rᴇɴᴀᴍᴇ 📝", callback_data=f"rename-{message.from_user.id}")],
            [InlineKeyboardButton("Cᴏᴍᴘʀᴇss 🗜️", callback_data=f"compress-{message.from_user.id}")]
        ]
        
        # Add queue button for premium users
        if is_premium or is_admin:
            buttons.append([InlineKeyboardButton("📊 View Queue", callback_data=f"view_queue_{user_id}")])
        
        buttons.append([InlineKeyboardButton('💝 movies ', url='https://t.me/aapna_Movies')])
        
        await SnowDev.edit(text=text, reply_markup=InlineKeyboardMarkup(buttons))
        
    except FloodWait as e:
        floodmsg = await message.reply_text(f"**😥 Pʟᴇᴀsᴇ Wᴀɪᴛ ᴅᴏɴ'ᴛ ᴅᴏ ғʟᴏᴏᴅɪɴɢ ᴡᴀɪᴛ ғᴏʀ {e.value} Sᴇᴄᴄᴏɴᴅs**", reply_to_message_id=message.id)
        await sleep(e.value)
        await floodmsg.delete()

        # Retry after flood wait
        can_process_now, queue_message = await check_queue_and_process(user_id, file, message, "encode")
        
        if is_admin:
            user_status = "👑 **Admin** - Unlimited Access"
        elif is_premium:
            user_status = f"⭐ **Premium** - Up to {Config.MAX_CONCURRENT_PREMIUM} concurrent files"
        else:
            user_status = f"🆓 **Free** - {Config.MAX_CONCURRENT_NON_PREMIUM} file at a time"
        
        text = f"""**__What do you want me to do with this file?__**

**File Name:** `{filename}`
**File Size:** `{filesize}`

**Your Status:** {user_status}
**Queue Status:** {queue_message}"""

        buttons = [
            [InlineKeyboardButton("Rᴇɴᴀᴍᴇ 📝", callback_data=f"rename-{message.from_user.id}")],
            [InlineKeyboardButton("Cᴏᴍᴘʀᴇss 🗜️", callback_data=f"compress-{message.from_user.id}")]
        ]
        
        if is_premium or is_admin:
            buttons.append([InlineKeyboardButton("📊 View Queue", callback_data=f"view_queue_{user_id}")])
        
        buttons.append([InlineKeyboardButton('💝 movies ', url='https://t.me/aapna_Movies')])
        
        await SnowDev.edit(text=text, reply_markup=InlineKeyboardMarkup(buttons))

    except Exception as e:
        print(e)

@Client.on_message((filters.private | filters.group) & filters.command('cancel'))
async def cancel_process(bot: Client, message: Message):
    user_id = message.from_user.id
    
    try:
        # Clean up processing directories
        shutil.rmtree(f"encode/{user_id}")
        shutil.rmtree(f"ffmpeg/{user_id}")
        shutil.rmtree(f"Renames/{user_id}")
        shutil.rmtree(f"Metadata/{user_id}")
        shutil.rmtree(f"Screenshot_Generation/{user_id}")
        
        # Mark processing as finished
        await finish_processing(user_id, success=False)
        
        return await message.reply_text(text="**✅ Canceled All Ongoing Processes**\n\nAll your active processes have been stopped.")
    except BaseException:
        pass

# Add verification status command
@Client.on_message(filters.command('verify_status') & filters.private)
async def check_verify_status(bot: Client, message: Message):
    user_id = message.from_user.id
    
    # Check if user is premium or admin
    is_premium = await is_premium_user(user_id)
    is_admin = user_id == Config.ADMIN
    
    if is_premium or is_admin:
        status_text = "👑 Admin Access" if is_admin else "⭐ Premium Access"
        return await message.reply_text(
            f"✅ **{status_text}**\n\n"
            f"You have unlimited access and don't need verification.\n\n"
            f"🎬 You can encode videos without restrictions.",
            quote=True
        )
    
    verify_status = await db.get_verify_status(user_id)
    
    if verify_status['is_verified']:
        verified_time = verify_status.get('verified_time', 0)
        remaining_time = Config.VERIFY_EXPIRE - (time.time() - verified_time)
        
        if remaining_time > 0:
            await message.reply_text(
                f"✅ **Verification Status: Active**\n\n"
                f"⏱️ **Time Remaining:** {get_exp_time(int(remaining_time))}\n\n"
                f"🎬 You can encode videos without restrictions.\n\n"
                f"💡 Upgrade to premium to skip verification forever!",
                quote=True
            )
        else:
            await message.reply_text(
                f"❌ **Verification Status: Expired**\n\n"
                f"Please send a file to get a new verification link.\n\n"
                f"💡 Or upgrade to premium to skip verification forever!",
                quote=True
            )
    else:
        await message.reply_text(
            f"❌ **Verification Status: Not Verified**\n\n"
            f"Please send a file to get a verification link.\n\n"
            f"💡 Or upgrade to premium to skip verification forever!",
            quote=True
        )

# Callback handlers for inline buttons
@Client.on_callback_query(filters.regex("get_premium"))
async def get_premium_callback(client: Client, callback_query):
    await callback_query.answer()
    await callback_query.message.reply_text(
        f"💎 **Get Premium Access**\n\n"
        f"**Premium Benefits:**\n"
        f"• ✅ No verification required\n"
        f"• 🚀 Up to {Config.MAX_CONCURRENT_PREMIUM} concurrent files\n"
        f"• ⚡ Priority processing\n"
        f"• 📊 Queue management\n\n"
        f"Contact admin to purchase premium access!",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("👨‍💻 Contact Admin", url=f"t.me/{Config.ADMIN}")]
        ])
    )

@Client.on_callback_query(filters.regex("my_plan"))
async def my_plan_callback(client: Client, callback_query):
    await callback_query.answer()
    # This will trigger the /myplan command functionality
    from .premium_commands import check_plan_cmd
    # Create a mock message object to reuse the function
    await check_plan_cmd(client, callback_query.message)

@Client.on_callback_query(filters.regex("queue_status"))
async def queue_status_callback(client: Client, callback_query):
    await callback_query.answer()
    # This will trigger the /queue command functionality
    from .premium_commands import queue_cmd
    await queue_cmd(client, callback_query.message)
