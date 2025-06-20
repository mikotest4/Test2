from config import Config
import traceback
from helper.database import db
from pyrogram.types import Message
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
import os
import sys
import time
import asyncio
import logging
import datetime


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def parse_time_duration(duration_str, unit):
    """Parse duration string and unit to seconds"""
    try:
        duration = int(duration_str)
        if unit.lower() in ['d', 'day', 'days']:
            return duration * 24 * 60 * 60
        elif unit.lower() in ['h', 'hour', 'hours']:
            return duration * 60 * 60
        elif unit.lower() in ['m', 'min', 'minute', 'minutes']:
            return duration * 60
        elif unit.lower() in ['s', 'sec', 'second', 'seconds']:
            return duration
        else:
            return None
    except ValueError:
        return None

def format_premium_expiry(timestamp):
    """Format premium expiry timestamp to readable format"""
    if timestamp == 0:
        return "Never"
    
    expiry_time = datetime.datetime.fromtimestamp(timestamp)
    current_time = datetime.datetime.now()
    
    if expiry_time <= current_time:
        return "Expired"
    
    time_left = expiry_time - current_time
    days = time_left.days
    hours, remainder = divmod(time_left.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    
    if days > 0:
        return f"{days} days, {hours} hours"
    elif hours > 0:
        return f"{hours} hours, {minutes} minutes"
    else:
        return f"{minutes} minutes"

@Client.on_message(filters.command("addpremium") & filters.user(Config.ADMIN))
async def add_premium_user(bot: Client, message: Message):
    if len(message.command) < 4:
        await message.reply_text(
            "**Usage:** `/addpremium user_id duration unit`\n\n"
            "**Examples:**\n"
            "• `/addpremium 1234567 30 d` - 30 days\n"
            "• `/addpremium 1234567 12 h` - 12 hours\n"
            "• `/addpremium 1234567 30 min` - 30 minutes\n\n"
            "**Supported units:** d/day/days, h/hour/hours, m/min/minute/minutes",
            quote=True
        )
        return

    try:
        user_id = int(message.command[1])
        duration_str = message.command[2]
        unit = message.command[3]
        
        duration_seconds = parse_time_duration(duration_str, unit)
        
        if duration_seconds is None:
            await message.reply_text(
                "❌ **Invalid duration or unit!**\n\n"
                "**Supported units:** d/day/days, h/hour/hours, m/min/minute/minutes",
                quote=True
            )
            return

        # Add premium user
        await db.add_premium_user(user_id, duration_seconds, message.from_user.id)
        
        # Calculate expiry time
        expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=duration_seconds)
        expiry_str = expiry_time.strftime("%Y-%m-%d %I:%M:%S %p IST")
        
        # Send success message
        success_text = (
            f"✅ **User `{user_id}` added as a premium user for {duration_str} {unit}.**\n"
            f"**Expiration Time:** `{expiry_str}`"
        )
        
        await message.reply_text(success_text, quote=True)
        
        # Notify the user
        try:
            await bot.send_message(
                user_id,
                f"🎉 **Congratulations! You have been granted Premium Access for {duration_str} {unit}!**\n\n"
                f"**Benefits: 1 :- No verification required. 2 :- Direct file encoding"
                f"**Expires:** `{expiry_str}`"
            )
        except Exception as e:
            await message.reply_text(f"✅ Premium added but couldn't notify user: {str(e)}", quote=True)
            
    except ValueError:
        await message.reply_text("❌ **Invalid user ID! Please provide a valid numeric user ID.**", quote=True)
    except Exception as e:
        await message.reply_text(f"❌ **Error:** {str(e)}", quote=True)

@Client.on_message(filters.command("revpremium") & filters.user(Config.ADMIN))
async def remove_premium_user(bot: Client, message: Message):
    if len(message.command) != 2:
        await message.reply_text(
            "**Usage:** `/revpremium user_id`\n\n"
            "**Example:** `/revpremium 1234567`",
            quote=True
        )
        return

    try:
        user_id = int(message.command[1])
        
        # Check if user is premium first
        premium_status = await db.get_premium_status(user_id)
        
        if not premium_status['is_premium']:
            await message.reply_text(f"❌ **User `{user_id}` is not a premium user.**", quote=True)
            return
        
        # Remove premium
        await db.remove_premium_user(user_id)
        
        await message.reply_text(f"✅ **Premium access removed from user `{user_id}`.**", quote=True)
        
        # Notify the user
        try:
            await bot.send_message(
                user_id,
                "📢 **Premium Access Removed**\n\n"
                "Your premium access has been revoked by an administrator.\n"
                "You will now need to complete verification to use the bot."
            )
        except Exception as e:
            await message.reply_text(f"✅ Premium removed but couldn't notify user: {str(e)}", quote=True)
            
    except ValueError:
        await message.reply_text("❌ **Invalid user ID! Please provide a valid numeric user ID.**", quote=True)
    except Exception as e:
        await message.reply_text(f"❌ **Error:** {str(e)}", quote=True)

@Client.on_message(filters.command("premiumusers") & filters.user(Config.ADMIN))
async def list_premium_users(bot: Client, message: Message):
    try:
        premium_users = await db.get_all_premium_users()
        premium_count = 0
        text = "👑 **Premium Users List:**\n\n"
        
        async for user in premium_users:
            user_id = user['id']
            premium_status = user['premium_status']
            
            # Double-check if still premium (handles expiry)
            current_status = await db.get_premium_status(user_id)
            if not current_status['is_premium']:
                continue
                
            premium_count += 1
            expiry_time = premium_status['premium_expires']
            time_left = format_premium_expiry(expiry_time)
            added_by = premium_status.get('added_by', 'Unknown')
            added_on = premium_status.get('added_on', 'Unknown')
            
            text += (
                f"**{premium_count}.** `{user_id}`\n"
                f"   • **Expires:** {time_left}\n"
                f"   • **Added by:** `{added_by}`\n"
                f"   • **Added on:** {added_on[:10] if added_on != 'Unknown' else 'Unknown'}\n\n"
            )
        
        if premium_count == 0:
            text = "📭 **No premium users found.**"
        else:
            text = f"👑 **Total Premium Users:** `{premium_count}`\n\n" + text
        
        if len(text) > 4096:
            with open('premium-users.txt', 'w') as f:
                f.write(text)
            await message.reply_document('premium-users.txt', quote=True)
            os.remove('premium-users.txt')
        else:
            await message.reply_text(text, quote=True)
            
    except Exception as e:
        await message.reply_text(f"❌ **Error:** {str(e)}", quote=True)

@Client.on_message(filters.command(["stats", "status"]) & filters.user(Config.ADMIN))
async def get_stats(bot, message):
    total_users = await db.total_users_count()
    premium_users = await db.get_all_premium_users()
    premium_count = 0
    async for user in premium_users:
        if await db.is_premium_user(user['id']):
            premium_count += 1
    
    uptime = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - Config.BOT_UPTIME))
    start_t = time.time()
    st = await message.reply('**Aᴄᴄᴇꜱꜱɪɴɢ Tʜᴇ Dᴇᴛᴀɪʟꜱ.....**')
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    
    stats_text = (
        f"**--Bᴏᴛ Sᴛᴀᴛᴜꜱ--**\n\n"
        f"**⌚️ Bᴏᴛ Uᴩᴛɪᴍᴇ:** {uptime}\n"
        f"**🐌 Cᴜʀʀᴇɴᴛ Pɪɴɢ:** `{time_taken_s:.3f} ᴍꜱ`\n"
        f"**👭 Tᴏᴛᴀʟ Uꜱᴇʀꜱ:** `{total_users}`\n"
        f"**👑 Pʀᴇᴍɪᴜᴍ Uꜱᴇʀꜱ:** `{premium_count}`"
    )
    
    await st.edit(text=stats_text)

# Restart to cancell all process
@Client.on_message(filters.private & filters.command("restart") & filters.user(Config.ADMIN))
async def restart_bot(b, m):
    await m.reply_text("🔄__Rᴇꜱᴛᴀʀᴛɪɴɢ.....__")
    os.execl(sys.executable, sys.executable, *sys.argv)


@Client.on_message(filters.command("broadcast") & filters.user(Config.ADMIN) & filters.reply)
async def broadcast_handler(bot: Client, m: Message):
    await bot.send_message(Config.LOG_CHANNEL, f"{m.from_user.mention} or {m.from_user.id} Iꜱ ꜱᴛᴀʀᴛᴇᴅ ᴛʜᴇ Bʀᴏᴀᴅᴄᴀꜱᴛ......")
    all_users = await db.get_all_users()
    broadcast_msg = m.reply_to_message
    sts_msg = await m.reply_text("Bʀᴏᴀᴅᴄᴀꜱᴛ Sᴛᴀʀᴛᴇᴅ..!")
    done = 0
    failed = 0
    success = 0
    start_time = time.time()
    total_users = await db.total_users_count()
    async for user in all_users:
        sts = await send_msg(user['id'], broadcast_msg)
        if sts == 200:
            success += 1
        else:
            failed += 1
        if sts == 400:
            await db.delete_user(user['id'])
        done += 1
        if not done % 20:
            await sts_msg.edit(f"Bʀᴏᴀᴅᴄᴀꜱᴛ Iɴ Pʀᴏɢʀᴇꜱꜱ: \nTᴏᴛᴀʟ Uꜱᴇʀꜱ {total_users} \nCᴏᴍᴩʟᴇᴛᴇᴅ: {done} / {total_users}\nSᴜᴄᴄᴇꜱꜱ: {success}\nFᴀɪʟᴇᴅ: {failed}")
    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await sts_msg.edit(f"Bʀᴏᴀᴅᴄᴀꜱᴛ Cᴏᴍᴩʟᴇᴛᴇᴅ: \nCᴏᴍᴩʟᴇᴛᴇᴅ Iɴ `{completed_in}`.\n\nTᴏᴛᴀʟ Uꜱᴇʀꜱ {total_users}\nCᴏᴍᴩʟᴇᴛᴇᴅ: {done} / {total_users}\nSᴜᴄᴄᴇꜱꜱ: {success}\nFᴀɪʟᴇᴅ: {failed}")


async def send_msg(user_id, message):
    try:
        await message.forward(chat_id=int(user_id))
        return 200
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return send_msg(user_id, message)
    except InputUserDeactivated:
        logger.info(f"{user_id} : Dᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ")
        return 400
    except UserIsBlocked:
        logger.info(f"{user_id} : Bʟᴏᴄᴋᴇᴅ Tʜᴇ Bᴏᴛ")
        return 400
    except PeerIdInvalid:
        logger.info(f"{user_id} : Uꜱᴇʀ Iᴅ Iɴᴠᴀʟɪᴅ")
        return 400
    except Exception as e:
        logger.error(f"{user_id} : {e}")
        return 500


@Client.on_message(filters.private & filters.command("ban_user") & filters.user(Config.ADMIN))
async def ban(c: Client, m: Message):

    if len(m.command) == 1:
        await m.reply_text(
            f"Use this command to ban any user from the bot.\n\n"
            f"Usage:\n\n"
            f"`/ban_user user_id ban_duration ban_reason`\n\n"
            f"Eg: `/ban_user 1234567 28 You misused me.`\n"
            f"This will ban user with id `1234567` for `28` days for the reason `You misused me`.",
            quote=True
        )
        return

    try:
        user_id = int(m.command[1])
        ban_duration = int(m.command[2])
        ban_reason = ' '.join(m.command[3:])
        ban_log_text = f"Banning user {user_id} for {ban_duration} days for the reason {ban_reason}."
        try:
            await c.send_message(
                user_id,
                f"You are banned to use this bot for **{ban_duration}** day(s) for the reason __{ban_reason}__ \n\n"
                f"**Message from the admin**"
            )
            ban_log_text += '\n\nUser notified successfully!'
        except:
            traceback.print_exc()
            ban_log_text += f"\n\nUser notification failed! \n\n`{traceback.format_exc()}`"

        await db.ban_user(user_id, ban_duration, ban_reason)
        print(ban_log_text)
        await m.reply_text(
            ban_log_text,
            quote=True
        )
    except:
        traceback.print_exc()
        await m.reply_text(
            f"Error occoured! Traceback given below\n\n`{traceback.format_exc()}`",
            quote=True
        )


@Client.on_message(filters.private & filters.command("unban_user") & filters.user(Config.ADMIN))
async def unban(c: Client, m: Message):

    if len(m.command) == 1:
        await m.reply_text(
            f"Use this command to unban any user.\n\n"
            f"Usage:\n\n`/unban_user user_id`\n\n"
            f"Eg: `/unban_user 1234567`\n"
            f"This will unban user with id `1234567`.",
            quote=True
        )
        return

    try:
        user_id = int(m.command[1])
        unban_log_text = f"Unbanning user {user_id}"
        try:
            await c.send_message(
                user_id,
                f"Your ban was lifted!"
            )
            unban_log_text += '\n\nUser notified successfully!'
        except:
            traceback.print_exc()
            unban_log_text += f"\n\nUser notification failed! \n\n`{traceback.format_exc()}`"
        await db.remove_ban(user_id)
        print(unban_log_text)
        await m.reply_text(
            unban_log_text,
            quote=True
        )
    except:
        traceback.print_exc()
        await m.reply_text(
            f"Error occurred! Traceback given below\n\n`{traceback.format_exc()}`",
            quote=True
        )


@Client.on_message(filters.private & filters.command("banned_users") & filters.user(Config.ADMIN))
async def _banned_users(_, m: Message):

    all_banned_users = await db.get_all_banned_users()
    banned_usr_count = 0
    text = ''

    async for banned_user in all_banned_users:
        user_id = banned_user['id']
        ban_duration = banned_user['ban_status']['ban_duration']
        banned_on = banned_user['ban_status']['banned_on']
        ban_reason = banned_user['ban_status']['ban_reason']
        banned_usr_count += 1
        text += f"> **user_id**: `{user_id}`, **Ban Duration**: `{ban_duration}`, " \
                f"**Banned on**: `{banned_on}`, **Reason**: `{ban_reason}`\n\n"
    reply_text = f"Total banned user(s): `{banned_usr_count}`\n\n{text}"
    if len(reply_text) > 4096:
        with open('banned-users.txt', 'w') as f:
            f.write(reply_text)
        await m.reply_document('banned-users.txt', True)
        os.remove('banned-users.txt')
        return
    await m.reply_text(reply_text, True)
