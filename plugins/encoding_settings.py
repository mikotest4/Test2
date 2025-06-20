from pyrogram import Client, filters
from pyrogram.types import Message
from helper.database import db
from config import Config

# Check if user is premium or admin
async def is_premium_or_admin(user_id):
    if user_id == Config.ADMIN:
        return True
    return await db.is_premium_user(user_id)

@Client.on_message(filters.command("crf_480p") & (filters.private | filters.group))
async def set_crf_480p(bot: Client, message: Message):
    user_id = message.from_user.id
    
    if not await is_premium_or_admin(user_id):
        await message.reply_text(
            "**ᴘʀᴇᴍɪᴜᴍ ғᴇᴀᴛᴜʀᴇ!**\n\n"
            "ᴛʜɪs ғᴇᴀᴛᴜʀᴇ ɪs ᴏɴʟʏ ᴀᴠᴀɪʟᴀʙʟᴇ ғᴏʀ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀs ᴀɴᴅ ᴀᴅᴍɪɴs.\n"
            "ᴄᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴ ᴛᴏ ɢᴇᴛ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇss!",
            quote=True
        )
        return
    
    if len(message.command) != 2:
        current_crf = await db.get_encoding_setting(user_id, 'crf_480p')
        chat_type = "ɢʀᴏᴜᴘ" if message.chat.type in ['supergroup', 'group'] else "ᴘʀɪᴠᴀᴛᴇ"
        await message.reply_text(
            f"**ᴄᴜʀʀᴇɴᴛ 480ᴘ ᴄʀғ:** `{current_crf}`\n\n"
            f"**ᴜsᴀɢᴇ:** `/crf_480p ᴠᴀʟᴜᴇ`\n\n"
            f"**ᴇxᴀᴍᴘʟᴇ:** `/crf_480p 25`\n\n"
            f"**ʀᴀɴɢᴇ:** 0-51 (ʟᴏᴡᴇʀ = ʙᴇᴛᴛᴇʀ ǫᴜᴀʟɪᴛʏ, ʜɪɢʜᴇʀ ғɪʟᴇ sɪᴢᴇ)\n"
            f"**ʀᴇᴄᴏᴍᴍᴇɴᴅᴇᴅ:** 23-30\n\n"
            f"**ᴄʜᴀᴛ ᴛʏᴘᴇ:** {chat_type}",
            quote=True
        )
        return
    
    try:
        crf_value = int(message.command[1])
        if not 0 <= crf_value <= 51:
            await message.reply_text(
                "**ɪɴᴠᴀʟɪᴅ ᴄʀғ ᴠᴀʟᴜᴇ!**\n\n"
                "ᴄʀғ ᴍᴜsᴛ ʙᴇ ʙᴇᴛᴡᴇᴇɴ 0-51",
                quote=True
            )
            return
        
        await db.set_encoding_settings(user_id, 'crf_480p', crf_value)
        chat_info = f" ɪɴ {message.chat.title}" if message.chat.type in ['supergroup', 'group'] else ""
        await message.reply_text(
            f"**480ᴘ ᴄʀғ sᴇᴛ ᴛᴏ:** `{crf_value}`{chat_info}\n\n"
            f"ᴛʜɪs ᴡɪʟʟ ʙᴇ ᴜsᴇᴅ ғᴏʀ ᴀʟʟ ʏᴏᴜʀ 480ᴘ ᴄᴏᴍᴘʀᴇssɪᴏɴs.",
            quote=True
        )
        
    except ValueError:
        await message.reply_text(
            "**ɪɴᴠᴀʟɪᴅ ᴠᴀʟᴜᴇ!**\n\n"
            "ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ɴᴜᴍᴇʀɪᴄ ᴄʀғ ᴠᴀʟᴜᴇ (0-51)",
            quote=True
        )

@Client.on_message(filters.command("crf_720p") & (filters.private | filters.group))
async def set_crf_720p(bot: Client, message: Message):
    user_id = message.from_user.id
    
    if not await is_premium_or_admin(user_id):
        await message.reply_text(
            "**ᴘʀᴇᴍɪᴜᴍ ғᴇᴀᴛᴜʀᴇ!**\n\n"
            "ᴛʜɪs ғᴇᴀᴛᴜʀᴇ ɪs ᴏɴʟʏ ᴀᴠᴀɪʟᴀʙʟᴇ ғᴏʀ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀs ᴀɴᴅ ᴀᴅᴍɪɴs.\n"
            "ᴄᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴ ᴛᴏ ɢᴇᴛ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇss!",
            quote=True
        )
        return
    
    if len(message.command) != 2:
        current_crf = await db.get_encoding_setting(user_id, 'crf_720p')
        chat_type = "ɢʀᴏᴜᴘ" if message.chat.type in ['supergroup', 'group'] else "ᴘʀɪᴠᴀᴛᴇ"
        await message.reply_text(
            f"**ᴄᴜʀʀᴇɴᴛ 720ᴘ ᴄʀғ:** `{current_crf}`\n\n"
            f"**ᴜsᴀɢᴇ:** `/crf_720p ᴠᴀʟᴜᴇ`\n\n"
            f"**ᴇxᴀᴍᴘʟᴇ:** `/crf_720p 24`\n\n"
            f"**ʀᴀɴɢᴇ:** 0-51 (ʟᴏᴡᴇʀ = ʙᴇᴛᴛᴇʀ ǫᴜᴀʟɪᴛʏ, ʜɪɢʜᴇʀ ғɪʟᴇ sɪᴢᴇ)\n"
            f"**ʀᴇᴄᴏᴍᴍᴇɴᴅᴇᴅ:** 23-28\n\n"
            f"**ᴄʜᴀᴛ ᴛʏᴘᴇ:** {chat_type}",
            quote=True
        )
        return
    
    try:
        crf_value = int(message.command[1])
        if not 0 <= crf_value <= 51:
            await message.reply_text(
                "**ɪɴᴠᴀʟɪᴅ ᴄʀғ ᴠᴀʟᴜᴇ!**\n\n"
                "ᴄʀғ ᴍᴜsᴛ ʙᴇ ʙᴇᴛᴡᴇᴇɴ 0-51",
                quote=True
            )
            return
        
        await db.set_encoding_settings(user_id, 'crf_720p', crf_value)
        chat_info = f" ɪɴ {message.chat.title}" if message.chat.type in ['supergroup', 'group'] else ""
        await message.reply_text(
            f"**720ᴘ ᴄʀғ sᴇᴛ ᴛᴏ:** `{crf_value}`{chat_info}\n\n"
            f"ᴛʜɪs ᴡɪʟʟ ʙᴇ ᴜsᴇᴅ ғᴏʀ ᴀʟʟ ʏᴏᴜʀ 720ᴘ ᴄᴏᴍᴘʀᴇssɪᴏɴs.",
            quote=True
        )
        
    except ValueError:
        await message.reply_text(
            "**ɪɴᴠᴀʟɪᴅ ᴠᴀʟᴜᴇ!**\n\n"
            "ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ɴᴜᴍᴇʀɪᴄ ᴄʀғ ᴠᴀʟᴜᴇ (0-51)",
            quote=True
        )

@Client.on_message(filters.command("crf_1080p") & (filters.private | filters.group))
async def set_crf_1080p(bot: Client, message: Message):
    user_id = message.from_user.id
    
    if not await is_premium_or_admin(user_id):
        await message.reply_text(
            "**ᴘʀᴇᴍɪᴜᴍ ғᴇᴀᴛᴜʀᴇ!**\n\n"
            "ᴛʜɪs ғᴇᴀᴛᴜʀᴇ ɪs ᴏɴʟʏ ᴀᴠᴀɪʟᴀʙʟᴇ ғᴏʀ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀs ᴀɴᴅ ᴀᴅᴍɪɴs.\n"
            "ᴄᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴ ᴛᴏ ɢᴇᴛ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇss!",
            quote=True
        )
        return
    
    if len(message.command) != 2:
        current_crf = await db.get_encoding_setting(user_id, 'crf_1080p')
        chat_type = "ɢʀᴏᴜᴘ" if message.chat.type in ['supergroup', 'group'] else "ᴘʀɪᴠᴀᴛᴇ"
        await message.reply_text(
            f"**ᴄᴜʀʀᴇɴᴛ 1080ᴘ ᴄʀғ:** `{current_crf}`\n\n"
            f"**ᴜsᴀɢᴇ:** `/crf_1080p ᴠᴀʟᴜᴇ`\n\n"
            f"**ᴇxᴀᴍᴘʟᴇ:** `/crf_1080p 22`\n\n"
            f"**ʀᴀɴɢᴇ:** 0-51 (ʟᴏᴡᴇʀ = ʙᴇᴛᴛᴇʀ ǫᴜᴀʟɪᴛʏ, ʜɪɢʜᴇʀ ғɪʟᴇ sɪᴢᴇ)\n"
            f"**ʀᴇᴄᴏᴍᴍᴇɴᴅᴇᴅ:** 20-26\n\n"
            f"**ᴄʜᴀᴛ ᴛʏᴘᴇ:** {chat_type}",
            quote=True
        )
        return
    
    try:
        crf_value = int(message.command[1])
        if not 0 <= crf_value <= 51:
            await message.reply_text(
                "**ɪɴᴠᴀʟɪᴅ ᴄʀғ ᴠᴀʟᴜᴇ!**\n\n"
                "ᴄʀғ ᴍᴜsᴛ ʙᴇ ʙᴇᴛᴡᴇᴇɴ 0-51",
                quote=True
            )
            return
        
        await db.set_encoding_settings(user_id, 'crf_1080p', crf_value)
        chat_info = f" ɪɴ {message.chat.title}" if message.chat.type in ['supergroup', 'group'] else ""
        await message.reply_text(
            f"**1080ᴘ ᴄʀғ sᴇᴛ ᴛᴏ:** `{crf_value}`{chat_info}\n\n"
            f"ᴛʜɪs ᴡɪʟʟ ʙᴇ ᴜsᴇᴅ ғᴏʀ ᴀʟʟ ʏᴏᴜʀ 1080ᴘ ᴄᴏᴍᴘʀᴇssɪᴏɴs.",
            quote=True
        )
        
    except ValueError:
        await message.reply_text(
            "**ɪɴᴠᴀʟɪᴅ ᴠᴀʟᴜᴇ!**\n\n"
            "ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ɴᴜᴍᴇʀɪᴄ ᴄʀғ ᴠᴀʟᴜᴇ (0-51)",
            quote=True
        )

@Client.on_message(filters.command("crf_4k") & (filters.private | filters.group))
async def set_crf_4k(bot: Client, message: Message):
    user_id = message.from_user.id
    
    if not await is_premium_or_admin(user_id):
        await message.reply_text(
            "**ᴘʀᴇᴍɪᴜᴍ ғᴇᴀᴛᴜʀᴇ!**\n\n"
            "ᴛʜɪs ғᴇᴀᴛᴜʀᴇ ɪs ᴏɴʟʏ ᴀᴠᴀɪʟᴀʙʟᴇ ғᴏʀ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀs ᴀɴᴅ ᴀᴅᴍɪɴs.\n"
            "ᴄᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴ ᴛᴏ ɢᴇᴛ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇss!",
            quote=True
        )
        return
    
    if len(message.command) != 2:
        current_crf = await db.get_encoding_setting(user_id, 'crf_4k')
        chat_type = "ɢʀᴏᴜᴘ" if message.chat.type in ['supergroup', 'group'] else "ᴘʀɪᴠᴀᴛᴇ"
        await message.reply_text(
            f"**ᴄᴜʀʀᴇɴᴛ 4ᴋ ᴄʀғ:** `{current_crf}`\n\n"
            f"**ᴜsᴀɢᴇ:** `/crf_4k ᴠᴀʟᴜᴇ`\n\n"
            f"**ᴇxᴀᴍᴘʟᴇ:** `/crf_4k 18`\n\n"
            f"**ʀᴀɴɢᴇ:** 0-51 (ʟᴏᴡᴇʀ = ʙᴇᴛᴛᴇʀ ǫᴜᴀʟɪᴛʏ, ʜɪɢʜᴇʀ ғɪʟᴇ sɪᴢᴇ)\n"
            f"**ʀᴇᴄᴏᴍᴍᴇɴᴅᴇᴅ:** 18-24\n\n"
            f"**ᴄʜᴀᴛ ᴛʏᴘᴇ:** {chat_type}",
            quote=True
        )
        return
    
    try:
        crf_value = int(message.command[1])
        if not 0 <= crf_value <= 51:
            await message.reply_text(
                "**ɪɴᴠᴀʟɪᴅ ᴄʀғ ᴠᴀʟᴜᴇ!**\n\n"
                "ᴄʀғ ᴍᴜsᴛ ʙᴇ ʙᴇᴛᴡᴇᴇɴ 0-51",
                quote=True
            )
            return
        
        await db.set_encoding_settings(user_id, 'crf_4k', crf_value)
        chat_info = f" ɪɴ {message.chat.title}" if message.chat.type in ['supergroup', 'group'] else ""
        await message.reply_text(
            f"**4ᴋ ᴄʀғ sᴇᴛ ᴛᴏ:** `{crf_value}`{chat_info}\n\n"
            f"ᴛʜɪs ᴡɪʟʟ ʙᴇ ᴜsᴇᴅ ғᴏʀ ᴀʟʟ ʏᴏᴜʀ 4ᴋ ᴄᴏᴍᴘʀᴇssɪᴏɴs.",
            quote=True
        )
        
    except ValueError:
        await message.reply_text(
            "**ɪɴᴠᴀʟɪᴅ ᴠᴀʟᴜᴇ!**\n\n"
            "ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ɴᴜᴍᴇʀɪᴄ ᴄʀғ ᴠᴀʟᴜᴇ (0-51)",
            quote=True
        )

@Client.on_message(filters.command("vcodec") & (filters.private | filters.group))
async def set_vcodec(bot: Client, message: Message):
    user_id = message.from_user.id
    
    if not await is_premium_or_admin(user_id):
        await message.reply_text(
            "**ᴘʀᴇᴍɪᴜᴍ ғᴇᴀᴛᴜʀᴇ!**\n\n"
            "ᴛʜɪs ғᴇᴀᴛᴜʀᴇ ɪs ᴏɴʟʏ ᴀᴠᴀɪʟᴀʙʟᴇ ғᴏʀ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀs ᴀɴᴅ ᴀᴅᴍɪɴs.\n"
            "ᴄᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴ ᴛᴏ ɢᴇᴛ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇss!",
            quote=True
        )
        return
    
    if len(message.command) != 2:
        current_vcodec = await db.get_encoding_setting(user_id, 'vcodec')
        chat_type = "ɢʀᴏᴜᴘ" if message.chat.type in ['supergroup', 'group'] else "ᴘʀɪᴠᴀᴛᴇ"
        await message.reply_text(
            f"**ᴄᴜʀʀᴇɴᴛ ᴠɪᴅᴇᴏ ᴄᴏᴅᴇᴄ:** `{current_vcodec}`\n\n"
            f"**ᴜsᴀɢᴇ:** `/vcodec ᴄᴏᴅᴇᴄ_ɴᴀᴍᴇ`\n\n"
            f"**ᴇxᴀᴍᴘʟᴇs:**\n"
            f"• `/vcodec libx264` - ʜ.264 (ᴍᴏsᴛ ᴄᴏᴍᴘᴀᴛɪʙʟᴇ)\n"
            f"• `/vcodec libx265` - ʜ.265 (ʙᴇᴛᴛᴇʀ ᴄᴏᴍᴘʀᴇssɪᴏɴ)\n"
            f"• `/vcodec libvpx-vp9` - ᴠᴘ9\n\n"
            f"**ᴄʜᴀᴛ ᴛʏᴘᴇ:** {chat_type}",
            quote=True
        )
        return
    
    codec = message.command[1].strip()
    valid_codecs = ['libx264', 'libx265', 'libvpx-vp9', 'libvpx', 'libav1', 'h264_nvenc', 'hevc_nvenc']
    
    if codec not in valid_codecs:
        await message.reply_text(
            f"**ɪɴᴠᴀʟɪᴅ ᴄᴏᴅᴇᴄ!**\n\n"
            f"**sᴜᴘᴘᴏʀᴛᴇᴅ ᴄᴏᴅᴇᴄs:**\n"
            f"• `libx264` - ʜ.264 (ᴍᴏsᴛ ᴄᴏᴍᴘᴀᴛɪʙʟᴇ)\n"
            f"• `libx265` - ʜ.265 (ʙᴇᴛᴛᴇʀ ᴄᴏᴍᴘʀᴇssɪᴏɴ)\n"
            f"• `libvpx-vp9` - ᴠᴘ9\n"
            f"• `libvpx` - ᴠᴘ8\n"
            f"• `libav1` - ᴀᴠ1\n"
            f"• `h264_nvenc` - ɴᴠɪᴅɪᴀ ʜ.264\n"
            f"• `hevc_nvenc` - ɴᴠɪᴅɪᴀ ʜ.265",
            quote=True
        )
        return
    
    await db.set_encoding_settings(user_id, 'vcodec', codec)
    chat_info = f" ɪɴ {message.chat.title}" if message.chat.type in ['supergroup', 'group'] else ""
    await message.reply_text(
        f"**ᴠɪᴅᴇᴏ ᴄᴏᴅᴇᴄ sᴇᴛ ᴛᴏ:** `{codec}`{chat_info}\n\n"
        f"ᴛʜɪs ᴡɪʟʟ ʙᴇ ᴜsᴇᴅ ғᴏʀ ᴀʟʟ ʏᴏᴜʀ ᴠɪᴅᴇᴏ ᴄᴏᴍᴘʀᴇssɪᴏɴs.",
        quote=True
    )

@Client.on_message(filters.command("preset") & (filters.private | filters.group))
async def set_preset(bot: Client, message: Message):
    user_id = message.from_user.id
    
    if not await is_premium_or_admin(user_id):
        await message.reply_text(
            "**ᴘʀᴇᴍɪᴜᴍ ғᴇᴀᴛᴜʀᴇ!**\n\n"
            "ᴛʜɪs ғᴇᴀᴛᴜʀᴇ ɪs ᴏɴʟʏ ᴀᴠᴀɪʟᴀʙʟᴇ ғᴏʀ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀs ᴀɴᴅ ᴀᴅᴍɪɴs.\n"
            "ᴄᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴ ᴛᴏ ɢᴇᴛ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇss!",
            quote=True
        )
        return
    
    if len(message.command) != 2:
        current_preset = await db.get_encoding_setting(user_id, 'preset')
        chat_type = "ɢʀᴏᴜᴘ" if message.chat.type in ['supergroup', 'group'] else "ᴘʀɪᴠᴀᴛᴇ"
        await message.reply_text(
            f"**ᴄᴜʀʀᴇɴᴛ ᴘʀᴇsᴇᴛ:** `{current_preset}`\n\n"
            f"**ᴜsᴀɢᴇ:** `/preset ᴘʀᴇsᴇᴛ_ɴᴀᴍᴇ`\n\n"
            f"**ᴇxᴀᴍᴘʟᴇs:**\n"
            f"• `/preset ultrafast` - ғᴀsᴛᴇsᴛ ᴇɴᴄᴏᴅɪɴɢ\n"
            f"• `/preset fast` - ғᴀsᴛ ᴇɴᴄᴏᴅɪɴɢ\n"
            f"• `/preset medium` - ʙᴀʟᴀɴᴄᴇᴅ\n"
            f"• `/preset slow` - ʙᴇᴛᴛᴇʀ ǫᴜᴀʟɪᴛʏ\n"
            f"• `/preset veryslow` - ʙᴇsᴛ ǫᴜᴀʟɪᴛʏ\n\n"
            f"**ᴄʜᴀᴛ ᴛʏᴘᴇ:** {chat_type}",
            quote=True
        )
        return
    
    preset = message.command[1].strip()
    valid_presets = ['ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow']
    
    if preset not in valid_presets:
        await message.reply_text(
            f"**ɪɴᴠᴀʟɪᴅ ᴘʀᴇsᴇᴛ!**\n\n"
            f"**sᴜᴘᴘᴏʀᴛᴇᴅ ᴘʀᴇsᴇᴛs:**\n"
            f"• `ultrafast` - ғᴀsᴛᴇsᴛ ᴇɴᴄᴏᴅɪɴɢ\n"
            f"• `superfast` - ᴠᴇʀʏ ғᴀsᴛ\n"
            f"• `veryfast` - ғᴀsᴛ\n"
            f"• `faster` - ғᴀsᴛᴇʀ\n"
            f"• `fast` - ғᴀsᴛ\n"
            f"• `medium` - ʙᴀʟᴀɴᴄᴇᴅ (ᴅᴇғᴀᴜʟᴛ)\n"
            f"• `slow` - ʙᴇᴛᴛᴇʀ ǫᴜᴀʟɪᴛʏ\n"
            f"• `slower` - ᴍᴜᴄʜ ʙᴇᴛᴛᴇʀ ǫᴜᴀʟɪᴛʏ\n"
            f"• `veryslow` - ʙᴇsᴛ ǫᴜᴀʟɪᴛʏ",
            quote=True
        )
        return
    
    await db.set_encoding_settings(user_id, 'preset', preset)
    chat_info = f" ɪɴ {message.chat.title}" if message.chat.type in ['supergroup', 'group'] else ""
    await message.reply_text(
        f"**ᴘʀᴇsᴇᴛ sᴇᴛ ᴛᴏ:** `{preset}`{chat_info}\n\n"
        f"ᴛʜɪs ᴡɪʟʟ ʙᴇ ᴜsᴇᴅ ғᴏʀ ᴀʟʟ ʏᴏᴜʀ ᴠɪᴅᴇᴏ ᴄᴏᴍᴘʀᴇssɪᴏɴs.",
        quote=True
    )

@Client.on_message(filters.command("encoding_settings") & (filters.private | filters.group))
async def view_encoding_settings(bot: Client, message: Message):
    user_id = message.from_user.id
    
    if not await is_premium_or_admin(user_id):
        await message.reply_text(
            "**ᴘʀᴇᴍɪᴜᴍ ғᴇᴀᴛᴜʀᴇ!**\n\n"
            "ᴛʜɪs ғᴇᴀᴛᴜʀᴇ ɪs ᴏɴʟʏ ᴀᴠᴀɪʟᴀʙʟᴇ ғᴏʀ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀs ᴀɴᴅ ᴀᴅᴍɪɴs.",
            quote=True
        )
        return
    
    settings = await db.get_encoding_settings(user_id)
    chat_info = f" ɪɴ {message.chat.title}" if message.chat.type in ['supergroup', 'group'] else ""
    
    settings_text = f"**ʏᴏᴜʀ ᴄᴜʀʀᴇɴᴛ ᴇɴᴄᴏᴅɪɴɢ sᴇᴛᴛɪɴɢs{chat_info}:**\n\n"
    settings_text += f"**480ᴘ ᴄʀғ:** `{settings.get('crf_480p', 28)}`\n"
    settings_text += f"**720ᴘ ᴄʀғ:** `{settings.get('crf_720p', 26)}`\n"  
    settings_text += f"**1080ᴘ ᴄʀғ:** `{settings.get('crf_1080p', 24)}`\n"
    settings_text += f"**4ᴋ ᴄʀғ:** `{settings.get('crf_4k', 22)}`\n"
    settings_text += f"**ᴠɪᴅᴇᴏ ᴄᴏᴅᴇᴄ:** `{settings.get('vcodec', 'libx264')}`\n"
    settings_text += f"**ᴘʀᴇsᴇᴛ:** `{settings.get('preset', 'veryfast')}`\n\n"
    settings_text += "**ɴᴏᴛᴇ:** ʟᴏᴡᴇʀ ᴄʀғ = ʙᴇᴛᴛᴇʀ ǫᴜᴀʟɪᴛʏ, ʜɪɢʜᴇʀ ғɪʟᴇ sɪᴢᴇ"
    
    await message.reply_text(settings_text, quote=True)

@Client.on_message(filters.command("reset_encoding") & (filters.private | filters.group))
async def reset_encoding_settings(bot: Client, message: Message):
    user_id = message.from_user.id
    
    if not await is_premium_or_admin(user_id):
        await message.reply_text(
            "**ᴘʀᴇᴍɪᴜᴍ ғᴇᴀᴛᴜʀᴇ!**\n\n"
            "ᴛʜɪs ғᴇᴀᴛᴜʀᴇ ɪs ᴏɴʟʏ ᴀᴠᴀɪʟᴀʙʟᴇ ғᴏʀ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀs ᴀɴᴅ ᴀᴅᴍɪɴs.",
            quote=True
        )
        return
    
    # Reset to default values
    await db.set_encoding_settings(user_id, 'crf_480p', 28)
    await db.set_encoding_settings(user_id, 'crf_720p', 26)
    await db.set_encoding_settings(user_id, 'crf_1080p', 24)
    await db.set_encoding_settings(user_id, 'crf_4k', 22)
    await db.set_encoding_settings(user_id, 'vcodec', 'libx264')
    await db.set_encoding_settings(user_id, 'preset', 'veryfast')
    
    chat_info = f" ɪɴ {message.chat.title}" if message.chat.type in ['supergroup', 'group'] else ""
    await message.reply_text(
        f"**ᴇɴᴄᴏᴅɪɴɢ sᴇᴛᴛɪɴɢs ʀᴇsᴇᴛ ᴛᴏ ᴅᴇғᴀᴜʟᴛs{chat_info}:**\n\n"
        f"**480ᴘ ᴄʀғ:** `28`\n"
        f"**720ᴘ ᴄʀғ:** `26`\n"
        f"**1080ᴘ ᴄʀғ:** `24`\n"
        f"**4ᴋ ᴄʀғ:** `22`\n"
        f"**ᴠɪᴅᴇᴏ ᴄᴏᴅᴇᴄ:** `libx264`\n"
        f"**ᴘʀᴇsᴇᴛ:** `veryfast`",
        quote=True
    )

@Client.on_message(filters.command("premium_status") & (filters.private | filters.group))
async def check_premium_status(bot: Client, message: Message):
    user_id = message.from_user.id
    
    if user_id == Config.ADMIN:
        await message.reply_text(
            "**ᴀᴅᴍɪɴ sᴛᴀᴛᴜs**\n\n"
            "ʏᴏᴜ ʜᴀᴠᴇ ғᴜʟʟ ᴀᴅᴍɪɴ ᴘʀɪᴠɪʟᴇɢᴇs ᴡɪᴛʜ ᴜɴʟɪᴍɪᴛᴇᴅ ᴀᴄᴄᴇss ᴛᴏ ᴀʟʟ ғᴇᴀᴛᴜʀᴇs.",
            quote=True
        )
        return
    
    premium_status = await db.get_premium_status(user_id)
    chat_info = f" ɪɴ {message.chat.title}" if message.ch
