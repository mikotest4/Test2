import asyncio
import math, time
from . import *
from datetime import datetime as dt
import sys
import shutil
import signal
import os
from pathlib import Path
from datetime import datetime
import psutil
from pytz import timezone
from config import Config
from script import Txt
from pyrogram import enums
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto

# Progress Message Templates
DOWNLOAD_PROGRESS = """
**ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ**

{filename}

{current} ᴏᴜᴛ ᴏғ {total}
[{progress_bar}] {percentage}%

**sᴘᴇᴇᴅ:** {speed}
**ᴇᴛᴀ:** {eta}
**ᴇʟᴀᴘsᴇᴅ:** {elapsed}
"""

UPLOAD_PROGRESS = """
**ᴜᴘʟᴏᴀᴅɪɴɢ**

{filename}

{current} ᴏᴜᴛ ᴏғ {total}
[{progress_bar}] {percentage}%

**sᴘᴇᴇᴅ:** {speed}
**ᴇᴛᴀ:** {eta}
**ᴇʟᴀᴘsᴇᴅ:** {elapsed}
"""

QUEUE = []

async def progress_for_pyrogram(current, total, ud_type, message, start):
    now = time.time()
    diff = now - start
    
    # Optimize update interval based on file size to prevent FloodWait
    if total > 500 * 1024 * 1024:  # Files larger than 500MB
        update_interval = 10.0
    elif total > 100 * 1024 * 1024:  # Files larger than 100MB
        update_interval = 8.0
    else:
        update_interval = 5.0  # Reduced from 2.0 to prevent FloodWait
    
    if round(diff % update_interval) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff)
        time_to_completion = round((total - current) / speed) if speed > 0 else 0
        
        filled_length = int(percentage / 5)
        progress_bar = "●" * filled_length + "○" * (20 - filled_length)
        
        if "download" in ud_type.lower():
            template = DOWNLOAD_PROGRESS
        else:
            template = UPLOAD_PROGRESS
        
        progress_text = template.format(
            filename=ud_type.replace("Downloading", "").replace("Uploading", "").strip(),
            current=humanbytes(current),
            total=humanbytes(total),
            progress_bar=progress_bar,
            percentage=f"{percentage:.2f}",
            speed=f"{humanbytes(speed)}/s",
            eta=f"{time_to_completion}s",
            elapsed=f"{elapsed_time}s"
        )
        
        # Enhanced FloodWait handling with retry mechanism
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                await message.edit(
                    text=progress_text,
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton("ᴄᴀɴᴄᴇʟ", callback_data=f"close-{message.from_user.id}")
                    ]])
                )
                break  # Success, exit retry loop
                
            except FloodWait as e:
                print(f"FloodWait in progress update: Sleeping for {e.value} seconds")
                await asyncio.sleep(e.value)
                retry_count += 1
                if retry_count >= max_retries:
                    print(f"Max retries reached for progress update, skipping...")
                    break
                    
            except Exception as e:
                print(f"Progress update error: {e}")
                break  # Don't retry for other errors

def humanbytes(size):    
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'ʙ'

def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "ᴅ, ") if days else "") + \
        ((str(hours) + "ʜ, ") if hours else "") + \
        ((str(minutes) + "ᴍ, ") if minutes else "") + \
        ((str(seconds) + "ꜱ, ") if seconds else "") + \
        ((str(milliseconds) + "ᴍꜱ, ") if milliseconds else "")
    return tmp[:-2] 

def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60      
    return "%d:%02d:%02d" % (hour, minutes, seconds)

def ts(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + "d, ") if days else "")
        + ((str(hours) + "h, ") if hours else "")
        + ((str(minutes) + "m, ") if minutes else "")
        + ((str(seconds) + "s, ") if seconds else "")
        + ((str(milliseconds) + "ms, ") if milliseconds else "")
    )
    return tmp[:-2]

async def send_log(b, u):
    if Config.LOG_CHANNEL is not None:
        try:
            botusername = await b.get_me()
            curr = datetime.now(timezone("Asia/Kolkata"))
            date = curr.strftime('%d %B, %Y')
            time = curr.strftime('%I:%M:%S %p')
            await b.send_message(
                Config.LOG_CHANNEL,
                f"**ɴᴇᴡ ᴜsᴇʀ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ**\n\nᴜsᴇʀ: {u.mention}\nɪᴅ: `{u.id}`\nᴜsᴇʀɴᴀᴍᴇ: @{u.username}\n\nᴅᴀᴛᴇ: {date}\nᴛɪᴍᴇ: {time}\n\nʙʏ: @{botusername.username}"
            )
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except Exception as e:
            print(f"Error sending log: {e}")
        
def Filename(filename, mime_type):
    if filename.split('.')[-1] in ['mkv', 'mp4', 'mp3', 'mov']:
        return filename
    else:
        if mime_type.split('/')[1] in ['pdf', 'mkv', 'mp4', 'mp3']:
            return f"{filename}.{mime_type.split('/')[1]}"
        elif mime_type.split('/')[0] == "audio":
            return f"{filename}.mp3"
        else:
            return f"{filename}.mkv"
            
async def CANT_CONFIG_GROUP_MSG(client, message):
    try:
        botusername = await client.get_me()
        btn = [
            [InlineKeyboardButton(text='ʙᴏᴛ ᴘᴍ', url=f'https://t.me/{botusername.username}')]
        ]
        ms = await message.reply_text(text="sᴏʀʀʏ ʏᴏᴜ ᴄᴀɴ'ᴛ ᴄᴏɴғɪɢ ʏᴏᴜʀ sᴇᴛᴛɪɴɢs\n\nғɪʀsᴛ sᴛᴀʀᴛ ᴍᴇ ɪɴ ᴘʀɪᴠᴀᴛᴇ ᴛʜᴇɴ ʏᴏᴜ ᴄᴀɴ ᴜsᴇ ᴍʏ ғᴇᴀᴛᴜʀᴇs ɪɴ ɢʀᴏᴜᴘ", reply_to_message_id = message.id, reply_markup=InlineKeyboardMarkup(btn))
        await asyncio.sleep(10)
        await ms.delete()
    except FloodWait as e:
        await asyncio.sleep(e.value)
    except Exception as e:
        print(f"Error in CANT_CONFIG_GROUP_MSG: {e}")

async def Compress_Stats(e, userid):
    if int(userid) not in [e.from_user.id, 0]:
        return await e.answer(f"ʜᴇʏ {e.from_user.first_name}\nʏᴏᴜ ᴄᴀɴ'ᴛ sᴇᴇ sᴛᴀᴛᴜs ᴀs ᴛʜɪs ɪs ɴᴏᴛ ʏᴏᴜʀ ғɪʟᴇ", show_alert=True)
    
    inp = f"ffmpeg/{e.from_user.id}/{os.listdir(f'ffmpeg/{e.from_user.id}')[0]}"
    outp = f"encode/{e.from_user.id}/{os.listdir(f'encode/{e.from_user.id}')[0]}"
    try:
        ot = humanbytes(int((Path(outp).stat().st_size)))
        ov = humanbytes(int(Path(inp).stat().st_size))
        processing_file_name = inp.replace(f"ffmpeg/{userid}/", "").replace(f"_", " ")
        
        btn = [
            [InlineKeyboardButton(f"sᴋɪᴘ", callback_data=f"skip-{userid}")],
            [InlineKeyboardButton(f"ᴄʟᴏsᴇ", callback_data="close")]
        ]
        
        processing_msg = f"""
**ᴄᴜʀʀᴇɴᴛ sᴛᴀᴛᴜs**

**ᴘʀᴏᴄᴇssɪɴɢ ғɪʟᴇ :** `{processing_file_name}`

**ᴄᴏᴍᴘʀᴇssᴇᴅ sɪᴢᴇ :** `{ot}`
**ᴏʀɪɢɪɴᴀʟ sɪᴢᴇ :** `{ov}`

**ɴᴏᴛᴇ:** ᴘʀᴏᴄᴇssɪɴɢ ᴄᴀɴ ᴛᴀᴋᴇ ᴛɪᴍᴇ ᴀᴄᴄᴏʀᴅɪɴɢ ᴛᴏ ʏᴏᴜʀ ᴠɪᴅᴇᴏ sɪᴢᴇ ᴀɴᴅ ᴇɴᴄᴏᴅɪɴɢ sᴇᴛᴛɪɴɢs
"""
        
        try:
            await e.message.edit(text=processing_msg, reply_markup=InlineKeyboardMarkup(btn))
        except FloodWait as f:
            await asyncio.sleep(f.value)
            await e.message.edit(text=processing_msg, reply_markup=InlineKeyboardMarkup(btn))
        except Exception as er:
            print(f"Error in Compress_Stats: {er}")
            
    except Exception as e:
        print(f"Error in Compress_Stats: {e}")

async def skip(e, userid):
    if int(userid) not in [e.from_user.id, 0]:
        return await e.answer(f"ʜᴇʏ {e.from_user.first_name}\nʏᴏᴜ ᴄᴀɴ'ᴛ sᴋɪᴘ ᴀs ᴛʜɪs ɪs ɴᴏᴛ ʏᴏᴜʀ ғɪʟᴇ", show_alert=True)
    
    try:
        shutil.rmtree(f"ffmpeg/{userid}")
        shutil.rmtree(f"encode/{userid}")
        QUEUE.remove(userid)
        await e.message.edit("**sᴋɪᴘᴘᴇᴅ ✓**")
    except Exception as er:
        await e.message.edit(f"**ᴇʀʀᴏʀ:** {er}")

async def CompressVideo(message, filename, userid, filename2, ffmpeg_cmnd):
    try:
        # FFmpeg compression with enhanced error handling
        process = await asyncio.create_subprocess_shell(
            ffmpeg_cmnd, 
            stdout=asyncio.subprocess.PIPE, 
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            error_msg = stderr.decode()
            await message.edit(f"**ᴇɴᴄᴏᴅɪɴɢ ғᴀɪʟᴇᴅ**\n\n`{error_msg}`")
            return False
            
        return True
        
    except Exception as e:
        await message.edit(f"**ᴇʀʀᴏʀ ɪɴ ᴠɪᴅᴇᴏ ᴄᴏᴍᴘʀᴇssɪᴏɴ:** {e}")
        return False

# FloodWait decorator for functions that might encounter rate limits
def handle_flood_wait(func):
    async def wrapper(*args, **kwargs):
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                return await func(*args, **kwargs)
            except FloodWait as e:
                print(f"FloodWait in {func.__name__}: Sleeping for {e.value} seconds")
                await asyncio.sleep(e.value)
                retry_count += 1
                if retry_count >= max_retries:
                    print(f"Max retries exceeded for {func.__name__}")
                    raise e
            except Exception as e:
                print(f"Error in {func.__name__}: {e}")
                raise e
        
        return None
    
    return wrapper
