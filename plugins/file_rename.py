import asyncio
from pyrogram import Client, filters, enums
from pyrogram.enums import MessageMediaType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

from helper.utils import progress_for_pyrogram, convert, humanbytes
from helper.database import db
from PIL import Image
import os
import time


@Client.on_callback_query(filters.regex('rename'))
async def rename(bot, update):
    user_id = update.data.split('-')[1]
    
    if int(user_id) not in [update.from_user.id, 0]:
            return await update.answer(f"ʜᴇʏ {update.from_user.first_name}\nᴛʜɪs ɪs ɴᴏᴛ ʏᴏᴜʀ ғɪʟᴇ ʏᴏᴜ ᴄᴀɴ'ᴛ ᴅᴏ ᴀɴʏ ᴏᴘᴇʀᴀᴛɪᴏɴ", show_alert=True)

    date = update.message.date
    await update.message.delete()
    await update.message.reply_text("**ᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ɴᴇᴡ ғɪʟᴇɴᴀᴍᴇ...**", reply_to_message_id=update.message.reply_to_message.id, reply_markup=ForceReply(True))

@Client.on_message((filters.private | filters.group) & filters.reply)
async def refunc(client, message):
    reply_message = message.reply_to_message
    if (reply_message.reply_markup) and isinstance(reply_message.reply_markup, ForceReply):
        new_name = message.text
        await message.delete()
        msg = await client.get_messages(message.chat.id, reply_message.id)
        file = msg.reply_to_message
        media = getattr(file, file.media.value)
        if not "." in new_name:
            if "." in media.file_name:
                extn = media.file_name.rsplit('.', 1)[-1]
            else:
                extn = "mkv"
            new_name = new_name + "." + extn
        await reply_message.delete()

        button = [[InlineKeyboardButton(
            "ᴅᴏᴄᴜᴍᴇɴᴛ", callback_data="upload_document")]]
        if file.media in [MessageMediaType.VIDEO, MessageMediaType.DOCUMENT]:
            button.append([InlineKeyboardButton(
                "ᴠɪᴅᴇᴏ", callback_data="upload_video")])
        elif file.media == MessageMediaType.AUDIO:
            button.append([InlineKeyboardButton(
                "ᴀᴜᴅɪᴏ", callback_data="upload_audio")])
        await message.reply_text(
            text=f"**sᴇʟᴇᴄᴛ ᴛʜᴇ ᴏᴜᴛᴘᴜᴛ ғɪʟᴇ ᴛʏᴘᴇ**\n**• ғɪʟᴇ ɴᴀᴍᴇ :-**`{new_name}`",
            reply_to_message_id=file.id,
            reply_markup=InlineKeyboardMarkup(button)
        )


@Client.on_callback_query(filters.regex("upload"))
async def doc(bot, update):
    
    if not os.path.isdir("Metadata"):
        os.mkdir("Metadata")

    new_name = update.message.text
    new_filename = new_name.split(":-")[1]
    file_path = f"Renames/{new_filename}"
    metadata_path = f"Metadata/{new_filename}"
    file = update.message.reply_to_message
    print(file_path)

    ms = await update.message.edit("**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...**\n**ᴛʀʏɪɴɢ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ....**")
    try:
        dl = await bot.download_media(message=file, file_name=file_path, progress=progress_for_pyrogram, progress_args=("\n**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...**\n\n**ᴅᴏᴡɴʟᴏᴀᴅ sᴛᴀʀᴛᴇᴅ....**", ms, time.time()))
    except Exception as e:
        return await ms.edit(e)

    duration = 0
    try:
        metadata = extractMetadata(createParser(file_path))
        if metadata.has("duration"):
            duration = metadata.get('duration').seconds
    except:
        pass
    ph_path = None
    user_id = update.from_user.id
    media = getattr(file, file.media.value)
    c_caption = await db.get_caption(user_id)
    c_thumb = await db.get_thumbnail(user_id)

    if c_caption:
        try:
            caption = c_caption.format(filename=new_filename, filesize=humanbytes(
                media.file_size), duration=convert(duration))
        except Exception as e:
            return await ms.edit(text=f"ʏᴏᴜʀ ᴄᴀᴘᴛɪᴏɴ ᴇʀʀᴏʀ ᴇxᴄᴇᴘᴛ ᴋᴇʏᴡᴏʀᴅ ᴀʀɢᴜᴍᴇɴᴛ ●> ({e})")
    else:
        caption = f"**{new_filename}**"

    if (media.thumbs or c_thumb):
        if c_thumb:
            ph_path = await bot.download_media(c_thumb)
        else:
            ph_path = await bot.download_media(media.thumbs[0].file_id)
        Image.open(ph_path).convert("RGB").save(ph_path)
        img = Image.open(ph_path)
        img.resize((320, 320))
        img.save(ph_path, "JPEG")

    await ms.edit("**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...**\n**ғᴇᴛᴄʜɪɴɢ ᴍᴇᴛᴀᴅᴀᴛᴀ....**")
    metadat = await db.get_metadata(user_id)
    
    if metadat:
        
        await ms.edit("ɪ ғᴏᴜɴᴅ ʏᴏᴜʀ ᴍᴇᴛᴀᴅᴀᴛᴀ\n\n**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...**\n**ᴀᴅᴅɪɴɢ ᴍᴇᴛᴀᴅᴀᴛᴀ ᴛᴏ ғɪʟᴇ....**")
        cmd = f"""ffmpeg -i "{dl}" {metadat} "{metadata_path}" """

        process = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
            

        stdout, stderr = await process.communicate()
        er = stderr.decode()

        try:
            if er:
                await ms.edit(str(er) + "\n\n**ᴇʀʀᴏʀ**")
        except BaseException:
            pass

    await ms.edit("ᴍᴇᴛᴀᴅᴀᴛᴀ ᴀᴅᴅᴇᴅ ᴛᴏ ᴛʜᴇ ғɪʟᴇ sᴜᴄᴄᴇssғᴜʟʟʏ\n\n**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...**\n**ᴛʀʏɪɴɢ ᴛᴏ ᴜᴘʟᴏᴀᴅɪɴɢ....**")
    type = update.data.split("_")[1]
    try:
        if type == "document":
            await bot.send_document(
                update.from_user.id,
                document=metadata_path,
                thumb=ph_path,
                caption=caption,
                progress=progress_for_pyrogram,
                progress_args=("**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...**\n**ᴜᴘʟᴏᴀᴅ sᴛᴀʀᴛᴇᴅ....**", ms, time.time()))
        elif type == "video":
            await bot.send_video(
                update.from_user.id,
                video=metadata_path,
                caption=caption,
                thumb=ph_path,
                duration=duration,
                progress=progress_for_pyrogram,
                progress_args=("**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...**\n**ᴜᴘʟᴏᴀᴅ sᴛᴀʀᴛᴇᴅ....**", ms, time.time()))
        elif type == "audio":
            await bot.send_audio(
                update.from_user.id,
                audio=metadata_path,
                caption=caption,
                thumb=ph_path,
                duration=duration,
                progress=progress_for_pyrogram,
                progress_args=("**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...**\n**ᴜᴘʟᴏᴀᴅ sᴛᴀʀᴛᴇᴅ....**", ms, time.time()))
    except Exception as e:
        os.remove(file_path)
        if ph_path:
            os.remove(ph_path)
            os.remove(metadata_path)
        return await ms.edit(f" ᴇʀʀᴏʀ {e}")
    try:
        os.remove(dl)
        os.remove(metadata_path)
        if ph_path:
            os.remove(ph_path)
    except Exception as e:
        pass

    await ms.delete()
