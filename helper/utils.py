import asyncio
import math
import time
import sys
import shutil
import signal
import os
from pathlib import Path
from datetime import datetime
import psutil
from pytz import timezone
from pyrogram import enums
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from config import Config
from script import Txt

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

{current} �ᴏᴜᴛ ᴏғ {total}
[{progress_bar}] {percentage}%

**sᴘᴇᴇᴅ:** {speed}
**ᴇᴛᴀ:** {eta}
**ᴇʟᴀᴘsᴇᴅ:** {elapsed}
"""

MAX_RETRIES = 5
INITIAL_DELAY = 10
MAX_FILE_SIZE = 2 * 1024 * 1024 * 1024  # 2GB

QUEUE = []

async def progress_for_pyrogram(current, total, ud_type, message, start):
    now = time.time()
    diff = now - start
    if round(diff % 2.00) == 0 or current == total:
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
        
        try:
            await message.edit(
                text=progress_text,
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("ᴄᴀɴᴄᴇʟ", callback_data=f"close-{message.from_user.id}")
                ]])
            )
        except:
            pass

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
        botusername = await b.get_me()
        curr = datetime.now(timezone("Asia/Kolkata"))
        date = curr.strftime('%d %B, %Y')
        time = curr.strftime('%I:%M:%S %p')
        await b.send_message(
            Config.LOG_CHANNEL,
            f"**ɴᴇᴡ ᴜsᴇʀ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ**\n\nᴜsᴇʀ: {u.mention}\nɪᴅ: `{u.id}`\nᴜsᴇʀɴᴀᴍᴇ: @{u.username}\n\nᴅᴀᴛᴇ: {date}\nᴛɪᴍᴇ: {time}\n\nʙʏ: @{botusername.username}"
        )
        
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
    botusername = await client.get_me()
    btn = [
        [InlineKeyboardButton(text='ʙᴏᴛ ᴘᴍ', url=f'https://t.me/{botusername.username}')]
    ]
    ms = await message.reply_text(text="sᴏʀʀʏ ʏᴏᴜ ᴄᴀɴ'ᴛ ᴄᴏɴғɪɢ ʏᴏᴜʀ sᴇᴛᴛɪɴɢs\n\nғɪʀsᴛ sᴛᴀʀᴛ ᴍᴇ ɪɴ ᴘʀɪᴠᴀᴛᴇ ᴛʜᴇɴ ʏᴏᴜ ᴄᴀɴ ᴜsᴇ ᴍʏ ғᴇᴀᴛᴜʀᴇs ɪɴ ɢʀᴏᴜᴘ", reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(btn))
    await asyncio.sleep(10)
    await ms.delete()

async def Compress_Stats(e, userid):
    if int(userid) not in [e.from_user.id, 0]:
        return await e.answer(f"ʜᴇʏ {e.from_user.first_name}\nʏᴏᴜ ᴄᴀɴ'ᴛ sᴇᴇ sᴛᴀᴛᴜs ᴀs ᴛʜɪs ɪs ɴᴏᴛ ʏᴏᴜʀ ғɪʟᴇ", show_alert=True)
    
    inp = f"ffmpeg/{e.from_user.id}/{os.listdir(f'ffmpeg/{e.from_user.id}')[0]}"
    outp = f"encode/{e.from_user.id}/{os.listdir(f'encode/{e.from_user.id}')[0]}"
    try:
        ot = humanbytes(int((Path(outp).stat().st_size)))
        ov = humanbytes(int(Path(inp).stat().st_size))
        processing_file_name = inp.replace(f"ffmpeg/{userid}/", "").replace(f"_", " ")
        ans = f"ᴘʀᴏᴄᴇssɪɴɢ ᴍᴇᴅɪᴀ: {processing_file_name}\n\nᴅᴏᴡɴʟᴏᴀᴅᴇᴅ: {ov}\n\nᴄᴏᴍᴘʀᴇssᴇᴅ: {ot}"
        await e.answer(ans, cache_time=0, show_alert=True)
    except Exception as er:
        print(er)
        await e.answer("sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ.\nsᴇɴᴅ ᴍᴇᴅɪᴀ ᴀɢᴀɪɴ.", cache_time=0, alert=True)

async def skip(e, userid):
    if int(userid) not in [e.from_user.id, 0]:
        return await e.answer(f"ʜᴇʏ {e.from_user.first_name}\nʏᴏᴜ ᴄᴀɴ'ᴛ ᴄᴀɴᴄᴇʟ ᴛʜᴇ ᴘʀᴏᴄᴇss ᴀs ʏᴏᴜ ᴅɪᴅɴ'ᴛ sᴛᴀʀᴛ ɪᴛ", show_alert=True)
    try:
        await e.message.delete()
        os.system(f"rm -rf ffmpeg/{userid}*")
        os.system(f"rm -rf encode/{userid}*")
        for proc in psutil.process_iter():
            processName = proc.name()
            processID = proc.pid
            print(processName, ' - ', processID)
            if processName == "ffmpeg":
                os.kill(processID, signal.SIGKILL)
    except Exception as e:
        pass
    try:
        shutil.rmtree(f'ffmpeg/{userid}')
        shutil.rmtree(f'encode/{userid}')
    except Exception as e:
        pass
    
    return

async def safe_send_document(bot, chat_id, document, thumb, caption, progress_args):
    for attempt in range(MAX_RETRIES):
        try:
            await bot.send_document(
                chat_id=chat_id,
                document=document,
                thumb=thumb,
                caption=caption,
                progress=progress_for_pyrogram,
                progress_args=progress_args
            )
            return True
        except FloodWait as e:
            wait_time = e.value + 5
            if attempt < MAX_RETRIES - 1:
                await progress_args[0].edit(
                    f"🚦 Flood wait triggered. Waiting {wait_time} seconds before retrying...\n\nAttempt {attempt + 1}/{MAX_RETRIES}"
                )
                await asyncio.sleep(wait_time)
            else:
                raise
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                await asyncio.sleep(INITIAL_DELAY * (attempt + 1))
            else:
                raise
    return False

async def CompressVideo(bot, query, ffmpegcode, c_thumb):
    UID = query.from_user.id
    ms = await query.message.edit('ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...\n\n**ғᴇᴛᴄʜɪɴɢ ǫᴜᴇᴜᴇ**')
    
    if os.path.isdir(f'ffmpeg/{UID}') and os.path.isdir(f'encode/{UID}'):
        return await ms.edit("**ʏᴏᴜ ᴄᴀɴ ᴄᴏᴍᴘʀᴇss ᴏɴʟʏ ᴏɴᴇ ғɪʟᴇ ᴀᴛ ᴀ ᴛɪᴍᴇ\n\nᴀs ᴛʜɪs ʜᴇʟᴘs ʀᴇᴅᴜᴄᴇ sᴇʀᴠᴇʀ ʟᴏᴀᴅ**")

    try:
        media = query.message.reply_to_message
        file = getattr(media, media.media.value)
        
        # Check file size
        if file.file_size > MAX_FILE_SIZE:
            return await ms.edit(f"⚠️ File size exceeds maximum limit of {humanbytes(MAX_FILE_SIZE)}")
        
        filename = Filename(filename=str(file.file_name), mime_type=str(file.mime_type))
        Download_DIR = f"ffmpeg/{UID}"
        Output_DIR = f"encode/{UID}"
        File_Path = f"ffmpeg/{UID}/{filename}"
        Output_Path = f"encode/{UID}/{filename}"
        
        await ms.edit('**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...**\n**ᴛʀʏɪɴɢ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ....**')
        s = datetime.now()
        
        try:
            if not os.path.isdir(Download_DIR) and not os.path.isdir(Output_DIR):
                os.makedirs(Download_DIR)
                os.makedirs(Output_DIR)

                dl = await bot.download_media(
                    message=file,
                    file_name=File_Path,
                    progress=progress_for_pyrogram,
                    progress_args=("\n**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...**\n\n**ᴅᴏᴡɴʟᴏᴀᴅ sᴛᴀʀᴛᴇᴅ....**", ms, time.time())
                )
        except Exception as e:
            return await ms.edit(f"Download error: {str(e)}")
        
        es = datetime.now()
        dtime = ts(int((es - s).seconds) * 1000)

        await ms.edit(
            "**ᴄᴏᴍᴘʀᴇssɪɴɢ...**",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='sᴛᴀᴛs', callback_data=f'stats-{UID}')],
                [InlineKeyboardButton(text='ᴄᴀɴᴄᴇʟ', callback_data=f'skip-{UID}')]
            ])
        )
        
        cmd = f"""ffmpeg -i "{dl}" {ffmpegcode} "{Output_Path}" -y"""
        
        try:
            process = await asyncio.create_subprocess_shell(
                cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            er = stderr.decode()
            
            if er:
                await ms.edit(f"FFmpeg Error:\n\n{str(er)}")
                shutil.rmtree(f"ffmpeg/{UID}")
                shutil.rmtree(f"encode/{UID}")
                return
        except Exception as e:
            await ms.edit(f"FFmpeg Process Error: {str(e)}")
            shutil.rmtree(f"ffmpeg/{UID}")
            shutil.rmtree(f"encode/{UID}")
            return
        
        ees = datetime.now()
        
        if (file.thumbs or c_thumb):
            try:
                if c_thumb:
                    ph_path = await bot.download_media(c_thumb)
                else:
                    ph_path = await bot.download_media(file.thumbs[0].file_id)
            except Exception as e:
                ph_path = None
                print(f"Thumbnail error: {e}")
        else:
            ph_path = None

        org = int(Path(File_Path).stat().st_size)
        com = int((Path(Output_Path).stat().st_size))
        pe = 100 - ((com / org) * 100)
        per = str(f"{pe:.2f}") + "%"
        eees = datetime.now()
        x = dtime
        xx = ts(int((ees - es).seconds) * 1000)
        xxx = ts(int((eees - ees).seconds) * 1000)
        
        await ms.edit("**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...**\n**ᴛʀʏɪɴɢ ᴛᴏ ᴜᴘʟᴏᴀᴅɪɴɢ....**")
        
        try:
            success = await safe_send_document(
                bot=bot,
                chat_id=UID,
                document=Output_Path,
                thumb=ph_path,
                caption=Config.caption.format(filename, humanbytes(org), humanbytes(com), per, x, xx, xxx),
                progress_args=("**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...**\n**ᴜᴘʟᴏᴀᴅ sᴛᴀʀᴛᴇᴅ....**", ms, time.time())
            )
            
            if not success:
                await ms.edit("Failed to upload after multiple attempts. Please try again later.")
                return
                
        except Exception as e:
            await ms.edit(f"Upload error: {str(e)}")
            return

        if query.message.chat.type == enums.ChatType.SUPERGROUP:
            botusername = await bot.get_me()
            await ms.edit(
                f"ʜᴇʏ {query.from_user.mention},\n\nɪ ʜᴀᴠᴇ sᴇɴᴅ ᴄᴏᴍᴘʀᴇssᴇᴅ ғɪʟᴇ ᴛᴏ ʏᴏᴜʀ ᴘᴍ",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(text="ʙᴏᴛ ᴘᴍ", url=f'https://t.me/{botusername.username}')]
                ])
            )
        else:
            await ms.delete()

        try:
            shutil.rmtree(f"ffmpeg/{UID}")
            shutil.rmtree(f"encode/{UID}")
            if ph_path and os.path.exists(ph_path):
                os.remove(ph_path)
        except Exception as e:
            print(f"Cleanup error: {e}")

    except Exception as e:
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        await ms.edit(f"❌ An error occurred: {str(e)}")
        try:
            shutil.rmtree(f"ffmpeg/{UID}")
            shutil.rmtree(f"encode/{UID}")
        except:
            pass
