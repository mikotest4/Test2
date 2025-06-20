import os
import time
import asyncio
import sys
import humanize
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from helper.utils import Compress_Stats, skip, CompressVideo
from helper.database import db
from script import Txt
from config import Config


@Client.on_callback_query()
async def Cb_Handle(bot: Client, query: CallbackQuery):
    data = query.data

    if data == 'help':
        btn = [
            [InlineKeyboardButton('ʙᴀᴄᴋ', callback_data='home')]
        ]
        await query.message.edit(text=Txt.HELP_MSG, reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=True)

    elif data == 'home':
        user_id = query.from_user.id
        is_premium = await db.is_premium_user(user_id)
        is_admin = user_id == Config.ADMIN
        
        if is_admin:
            status_text = "ᴀᴅᴍɪɴ ᴜsᴇʀ - ғᴜʟʟ ᴀᴄᴄᴇss ᴇᴠᴇʀʏᴡʜᴇʀᴇ"
        elif is_premium:
            status_text = "ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀ - ɢʀᴏᴜᴘ ᴀᴄᴄᴇss (ɴᴏ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ)"
        else:
            status_text = "ʀᴇɢᴜʟᴀʀ ᴜsᴇʀ - ɢʀᴏᴜᴘ ᴀᴄᴄᴇss (ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ʀᴇǫᴜɪʀᴇᴅ)"
            
        btn = [
            [InlineKeyboardButton(text='ʜᴇʟᴘ', callback_data='help'), 
             InlineKeyboardButton(text='ᴀʙᴏᴜᴛ', callback_data='about')],
            [InlineKeyboardButton(text='ᴜᴘᴅᴀᴛᴇs', url='https://t.me/+ccx-5xVHyro3ZjNl'), 
             InlineKeyboardButton(text='ᴅᴇᴠᴇʟᴏᴘᴇʀ', url='https://t.me/+6LwHBLWZc3IyMTU1')]
        ]
        
        home_text = f"{status_text}\n\n{Txt.PRIVATE_START_MSG.format(query.from_user.mention)}"
        await query.message.edit(text=home_text, reply_markup=InlineKeyboardMarkup(btn))

    elif data == 'about':
        BUTN = [
            [InlineKeyboardButton(text='ʙᴀᴄᴋ', callback_data='home')]
        ]
        botuser = await bot.get_me()
        await query.message.edit(Txt.ABOUT_TXT.format(botuser.username), reply_markup=InlineKeyboardMarkup(BUTN), disable_web_page_preview=True)

    if data.startswith('stats'):
        user_id = data.split('-')[1]
        try:
            await Compress_Stats(e=query, userid=user_id)
        except Exception as e:
            print(e)

    elif data.startswith('skip'):
        user_id = data.split('-')[1]
        try:
            await skip(e=query, userid=user_id)
        except Exception as e:
            print(e)

    elif data == 'option':
        user_id = query.from_user.id
        chat_type = query.message.chat.type
        
        is_admin = user_id == Config.ADMIN
        is_premium = await db.is_premium_user(user_id)
        is_in_group = chat_type in ['supergroup', 'group']
        
        if is_admin:
            access_level = "ᴀᴅᴍɪɴ (ғᴜʟʟ ᴀᴄᴄᴇss)"
        elif is_premium:
            access_level = "ᴘʀᴇᴍɪᴜᴍ (ɴᴏ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ)"
        else:
            access_level = "ʀᴇɢᴜʟᴀʀ (ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ʀᴇǫᴜɪʀᴇᴅ)"
            
        location = "ɢʀᴏᴜᴘ ᴄʜᴀᴛ" if is_in_group else "ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ"
        
        file = getattr(query.message.reply_to_message,
                       query.message.reply_to_message.media.value)

        text = f"""**ᴡʜᴀᴛ ᴅᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴍᴇ ᴛᴏ ᴅᴏ ᴡɪᴛʜ ᴛʜɪs ғɪʟᴇ.?**

**ғɪʟᴇ ɴᴀᴍᴇ:** `{file.file_name}`
**ғɪʟᴇ sɪᴢᴇ:** `{humanize.naturalsize(file.file_size)}`

**ᴀᴄᴄᴇss ʟᴇᴠᴇʟ:** {access_level}
**ʟᴏᴄᴀᴛɪᴏɴ:** {location}

**ɴᴏᴛᴇ:** ᴏɴʟʏ ᴀᴅᴍɪɴ ᴄᴀɴ ᴇɴᴄᴏᴅᴇ ɪɴ ᴅᴍ!"""

        buttons = [[InlineKeyboardButton("ʀᴇɴᴀᴍᴇ", callback_data=f"rename-{query.from_user.id}")],
                   [InlineKeyboardButton("ᴄᴏᴍᴘʀᴇss", callback_data=f"compress-{query.from_user.id}")]]

        await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup(buttons))

    elif data == 'setffmpeg':
        try:
            ffmpeg_code = await bot.ask(text=Txt.SEND_FFMPEG_CODE, chat_id=query.from_user.id, filters=filters.text, timeout=60, disable_web_page_preview=True)
        except:
            return await query.message.reply_text("**ᴇʀʀᴏʀ!!**\n\nʀᴇǫᴜᴇsᴛ ᴛɪᴍᴇᴅ ᴏᴜᴛ.\nsᴇᴛ ʙʏ ᴜsɪɴɢ /set_ffmpeg")

        SnowDev = await query.message.reply_text(text="**sᴇᴛᴛɪɴɢ ʏᴏᴜʀ ғғᴍᴘᴇɢ ᴄᴏᴅᴇ**\n\nᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...")
        await db.set_ffmpegcode(query.from_user.id, ffmpeg_code.text)
        await SnowDev.edit("**ғғᴍᴘᴇɢ ᴄᴏᴅᴇ sᴇᴛ sᴜᴄᴄᴇssғᴜʟʟʏ**")

    elif data.startswith('compress'):
        user_id = data.split('-')[1]

        if int(user_id) not in [query.from_user.id, 0]:
            return await query.answer(f"ʜᴇʏ {query.from_user.first_name}\nᴛʜɪs ɪs ɴᴏᴛ ʏᴏᴜʀ ғɪʟᴇ ʏᴏᴜ ᴄᴀɴ'ᴛ ᴅᴏ ᴀɴʏ ᴏᴘᴇʀᴀᴛɪᴏɴ", show_alert=True)

        else:
            BTNS = [
                [InlineKeyboardButton(text='480ᴘ', callback_data='480pc'), 
                 InlineKeyboardButton(text='720ᴘ', callback_data='720pc')],
                [InlineKeyboardButton(text='1080ᴘ', callback_data='1080pc'), 
                 InlineKeyboardButton(text='4ᴋ', callback_data='2160pc')],
                [InlineKeyboardButton(text='ᴄᴜsᴛᴏᴍ ᴇɴᴄᴏᴅɪɴɢ', callback_data='custompc')],
                [InlineKeyboardButton(text='ᴄʟᴏsᴇ', callback_data='close'), 
                 InlineKeyboardButton(text='ʙᴀᴄᴋ', callback_data='option')]
            ]
            
            is_admin = query.from_user.id == Config.ADMIN
            is_premium = await db.is_premium_user(query.from_user.id)
            
            if is_admin:
                user_access = "ᴀᴅᴍɪɴ"
            elif is_premium:
                user_access = "ᴘʀᴇᴍɪᴜᴍ (ɴᴏ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ)"
            else:
                user_access = "ʀᴇɢᴜʟᴀʀ (ᴠᴇʀɪғɪᴇᴅ)"
            
            compress_text = f'**sᴇʟᴇᴄᴛ ᴛʜᴇ ᴄᴏᴍᴘʀᴇssɪᴏɴ ᴍᴇᴛʜᴏᴅ ʙᴇʟᴏᴡ**\n\n**ʏᴏᴜʀ ᴀᴄᴄᴇss:** {user_access}\n**ʟᴏᴄᴀᴛɪᴏɴ:** {"ɢʀᴏᴜᴘ" if query.message.chat.type in ["supergroup", "group"] else "ᴅᴍ"}'
            
            await query.message.edit(text=compress_text, reply_markup=InlineKeyboardMarkup(BTNS))

    elif data == '480pc':
        try:
            c_thumb = await db.get_thumbnail(query.from_user.id)
            settings = await db.get_encoding_settings(query.from_user.id)
            crf = settings['crf_480p']
            vcodec = settings['vcodec']
            preset = settings['preset']
            
            ffmpeg = f"-preset {preset} -c:v {vcodec} -s 840x480 -crf {crf} -pix_fmt yuv420p -c:a libopus -b:a 32k -c:s copy -map 0 -ac 2 -ab 32k -vbr 2 -level 3.1 -threads 5"
            await CompressVideo(bot=bot, query=query, ffmpegcode=ffmpeg, c_thumb=c_thumb)
        except Exception as e:
            print(e)

    elif data == '720pc':
        try:
            c_thumb = await db.get_thumbnail(query.from_user.id)
            settings = await db.get_encoding_settings(query.from_user.id)
            crf = settings['crf_720p']
            vcodec = settings['vcodec']
            preset = settings['preset']
            
            ffmpeg = f"-preset {preset} -c:v {vcodec} -s 1280x720 -crf {crf} -pix_fmt yuv420p -c:a libopus -b:a 32k -c:s copy -map 0 -ac 2 -ab 32k -vbr 2 -level 3.1 -threads 5"
            await CompressVideo(bot=bot, query=query, ffmpegcode=ffmpeg, c_thumb=c_thumb)
        except Exception as e:
            print(e)

    elif data == '1080pc':
        try:
            c_thumb = await db.get_thumbnail(query.from_user.id)
            settings = await db.get_encoding_settings(query.from_user.id)
            crf = settings['crf_1080p']
            vcodec = settings['vcodec']
            preset = settings['preset']
            
            ffmpeg = f"-preset {preset} -c:v {vcodec} -s 1920x1080 -crf {crf} -pix_fmt yuv420p -c:a libopus -b:a 32k -c:s copy -map 0 -ac 2 -ab 32k -vbr 2 -level 3.1 -threads 5"
            await CompressVideo(bot=bot, query=query, ffmpegcode=ffmpeg, c_thumb=c_thumb)
        except Exception as e:
            print(e)

    elif data == '2160pc':
        try:
            c_thumb = await db.get_thumbnail(query.from_user.id)
            settings = await db.get_encoding_settings(query.from_user.id)
            crf = settings['crf_4k']
            vcodec = settings['vcodec']
            preset = settings['preset']
            
            ffmpeg = f"-preset {preset} -c:v {vcodec} -s 3840x2160 -crf {crf} -pix_fmt yuv420p -c:a libopus -b:a 32k -c:s copy -map 0 -ac 2 -ab 32k -vbr 2 -level 3.1 -threads 5"
            await CompressVideo(bot=bot, query=query, ffmpegcode=ffmpeg, c_thumb=c_thumb)
        except Exception as e:
            print(e)

    elif data == 'custompc':
        try:
            ffmpeg_code = await bot.ask(text=Txt.SEND_FFMPEG_CODE, chat_id=query.from_user.id, filters=filters.text, timeout=60, disable_web_page_preview=True)
        except:
            return await query.message.edit("**ᴇʀʀᴏʀ!!**\n\nʀᴇǫᴜᴇsᴛ ᴛɪᴍᴇᴅ ᴏᴜᴛ.")

        c_thumb = await db.get_thumbnail(query.from_user.id)
        await CompressVideo(bot=bot, query=query, ffmpegcode=ffmpeg_code.text, c_thumb=c_thumb)

    elif data.startswith('close'):
        user_id = data.split('-')[1]
        if int(user_id) not in [query.from_user.id, 0]:
            return await query.answer(f"ʜᴇʏ {query.from_user.first_name}\nʏᴏᴜ ᴄᴀɴ'ᴛ ᴄʟᴏsᴇ ᴛʜɪs ᴀs ɪᴛ's ɴᴏᴛ ʏᴏᴜʀs", show_alert=True)
        try:
            await query.message.delete()
        except:
            return
