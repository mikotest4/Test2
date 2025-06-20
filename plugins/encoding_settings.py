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
            "❌ **Premium Feature!**\n\n"
            "This feature is only available for premium users and admins.\n"
            "Contact admin to get premium access!",
            quote=True
        )
        return
    
    if len(message.command) != 2:
        current_crf = await db.get_encoding_setting(user_id, 'crf_480p')
        chat_type = "group" if message.chat.type in ['supergroup', 'group'] else "private"
        await message.reply_text(
            f"**Current 480p CRF:** `{current_crf}`\n\n"
            f"**Usage:** `/crf_480p value`\n\n"
            f"**Example:** `/crf_480p 25`\n\n"
            f"**Range:** 0-51 (lower = better quality, higher file size)\n"
            f"**Recommended:** 23-30\n\n"
            f"**Chat Type:** {chat_type}",
            quote=True
        )
        return
    
    try:
        crf_value = int(message.command[1])
        if not 0 <= crf_value <= 51:
            await message.reply_text(
                "❌ **Invalid CRF value!**\n\n"
                "CRF must be between 0-51",
                quote=True
            )
            return
        
        await db.set_encoding_settings(user_id, 'crf_480p', crf_value)
        chat_info = f" in {message.chat.title}" if message.chat.type in ['supergroup', 'group'] else ""
        await message.reply_text(
            f"✅ **480p CRF set to:** `{crf_value}`{chat_info}\n\n"
            f"This will be used for all your 480p compressions.",
            quote=True
        )
        
    except ValueError:
        await message.reply_text(
            "❌ **Invalid value!**\n\n"
            "Please provide a numeric CRF value (0-51)",
            quote=True
        )

@Client.on_message(filters.command("crf_720p") & (filters.private | filters.group))
async def set_crf_720p(bot: Client, message: Message):
    user_id = message.from_user.id
    
    if not await is_premium_or_admin(user_id):
        await message.reply_text(
            "❌ **Premium Feature!**\n\n"
            "This feature is only available for premium users and admins.\n"
            "Contact admin to get premium access!",
            quote=True
        )
        return
    
    if len(message.command) != 2:
        current_crf = await db.get_encoding_setting(user_id, 'crf_720p')
        chat_type = "group" if message.chat.type in ['supergroup', 'group'] else "private"
        await message.reply_text(
            f"**Current 720p CRF:** `{current_crf}`\n\n"
            f"**Usage:** `/crf_720p value`\n\n"
            f"**Example:** `/crf_720p 24`\n\n"
            f"**Range:** 0-51 (lower = better quality, higher file size)\n"
            f"**Recommended:** 23-28\n\n"
            f"**Chat Type:** {chat_type}",
            quote=True
        )
        return
    
    try:
        crf_value = int(message.command[1])
        if not 0 <= crf_value <= 51:
            await message.reply_text(
                "❌ **Invalid CRF value!**\n\n"
                "CRF must be between 0-51",
                quote=True
            )
            return
        
        await db.set_encoding_settings(user_id, 'crf_720p', crf_value)
        chat_info = f" in {message.chat.title}" if message.chat.type in ['supergroup', 'group'] else ""
        await message.reply_text(
            f"✅ **720p CRF set to:** `{crf_value}`{chat_info}\n\n"
            f"This will be used for all your 720p compressions.",
            quote=True
        )
        
    except ValueError:
        await message.reply_text(
            "❌ **Invalid value!**\n\n"
            "Please provide a numeric CRF value (0-51)",
            quote=True
        )

@Client.on_message(filters.command("crf_1080p") & (filters.private | filters.group))
async def set_crf_1080p(bot: Client, message: Message):
    user_id = message.from_user.id
    
    if not await is_premium_or_admin(user_id):
        await message.reply_text(
            "❌ **Premium Feature!**\n\n"
            "This feature is only available for premium users and admins.\n"
            "Contact admin to get premium access!",
            quote=True
        )
        return
    
    if len(message.command) != 2:
        current_crf = await db.get_encoding_setting(user_id, 'crf_1080p')
        chat_type = "group" if message.chat.type in ['supergroup', 'group'] else "private"
        await message.reply_text(
            f"**Current 1080p CRF:** `{current_crf}`\n\n"
            f"**Usage:** `/crf_1080p value`\n\n"
            f"**Example:** `/crf_1080p 22`\n\n"
            f"**Range:** 0-51 (lower = better quality, higher file size)\n"
            f"**Recommended:** 20-26\n\n"
            f"**Chat Type:** {chat_type}",
            quote=True
        )
        return
    
    try:
        crf_value = int(message.command[1])
        if not 0 <= crf_value <= 51:
            await message.reply_text(
                "❌ **Invalid CRF value!**\n\n"
                "CRF must be between 0-51",
                quote=True
            )
            return
        
        await db.set_encoding_settings(user_id, 'crf_1080p', crf_value)
        chat_info = f" in {message.chat.title}" if message.chat.type in ['supergroup', 'group'] else ""
        await message.reply_text(
            f"✅ **1080p CRF set to:** `{crf_value}`{chat_info}\n\n"
            f"This will be used for all your 1080p compressions.",
            quote=True
        )
        
    except ValueError:
        await message.reply_text(
            "❌ **Invalid value!**\n\n"
            "Please provide a numeric CRF value (0-51)",
            quote=True
        )

@Client.on_message(filters.command("crf_4k") & (filters.private | filters.group))
async def set_crf_4k(bot: Client, message: Message):
    user_id = message.from_user.id
    
    if not await is_premium_or_admin(user_id):
        await message.reply_text(
            "❌ **Premium Feature!**\n\n"
            "This feature is only available for premium users and admins.\n"
            "Contact admin to get premium access!",
            quote=True
        )
        return
    
    if len(message.command) != 2:
        current_crf = await db.get_encoding_setting(user_id, 'crf_4k')
        chat_type = "group" if message.chat.type in ['supergroup', 'group'] else "private"
        await message.reply_text(
            f"**Current 4K CRF:** `{current_crf}`\n\n"
            f"**Usage:** `/crf_4k value`\n\n"
            f"**Example:** `/crf_4k 18`\n\n"
            f"**Range:** 0-51 (lower = better quality, higher file size)\n"
            f"**Recommended:** 18-24\n\n"
            f"**Chat Type:** {chat_type}",
            quote=True
        )
        return
    
    try:
        crf_value = int(message.command[1])
        if not 0 <= crf_value <= 51:
            await message.reply_text(
                "❌ **Invalid CRF value!**\n\n"
                "CRF must be between 0-51",
                quote=True
            )
            return
        
        await db.set_encoding_settings(user_id, 'crf_4k', crf_value)
        chat_info = f" in {message.chat.title}" if message.chat.type in ['supergroup', 'group'] else ""
        await message.reply_text(
            f"✅ **4K CRF set to:** `{crf_value}`{chat_info}\n\n"
            f"This will be used for all your 4K compressions.",
            quote=True
        )
        
    except ValueError:
        await message.reply_text(
            "❌ **Invalid value!**\n\n"
            "Please provide a numeric CRF value (0-51)",
            quote=True
        )

@Client.on_message(filters.command("vcodec") & (filters.private | filters.group))
async def set_vcodec(bot: Client, message: Message):
    user_id = message.from_user.id
    
    if not await is_premium_or_admin(user_id):
        await message.reply_text(
            "❌ **Premium Feature!**\n\n"
            "This feature is only available for premium users and admins.\n"
            "Contact admin to get premium access!",
            quote=True
        )
        return
    
    if len(message.command) != 2:
        current_vcodec = await db.get_encoding_setting(user_id, 'vcodec')
        chat_type = "group" if message.chat.type in ['supergroup', 'group'] else "private"
        await message.reply_text(
            f"**Current Video Codec:** `{current_vcodec}`\n\n"
            f"**Usage:** `/vcodec codec_name`\n\n"
            f"**Examples:**\n"
            f"• `/vcodec libx264` - H.264 (most compatible)\n"
            f"• `/vcodec libx265` - H.265 (better compression)\n"
            f"• `/vcodec libvpx-vp9` - VP9\n\n"
            f"**Chat Type:** {chat_type}",
            quote=True
        )
        return
    
    codec = message.command[1].strip()
    valid_codecs = ['libx264', 'libx265', 'libvpx-vp9', 'libvpx', 'libav1', 'h264_nvenc', 'hevc_nvenc']
    
    if codec not in valid_codecs:
        await message.reply_text(
            f"❌ **Invalid codec!**\n\n"
            f"**Supported codecs:**\n"
            f"• `libx264` - H.264 (most compatible)\n"
            f"• `libx265` - H.265 (better compression)\n"
            f"• `libvpx-vp9` - VP9\n"
            f"• `libvpx` - VP8\n"
            f"• `libav1` - AV1\n"
            f"• `h264_nvenc` - NVIDIA H.264\n"
            f"• `hevc_nvenc` - NVIDIA H.265",
            quote=True
        )
        return
    
    await db.set_encoding_settings(user_id, 'vcodec', codec)
    chat_info = f" in {message.chat.title}" if message.chat.type in ['supergroup', 'group'] else ""
    await message.reply_text(
        f"✅ **Video codec set to:** `{codec}`{chat_info}\n\n"
        f"This will be used for all your video compressions.",
        quote=True
    )

@Client.on_message(filters.command("preset") & (filters.private | filters.group))
async def set_preset(bot: Client, message: Message):
    user_id = message.from_user.id
    
    if not await is_premium_or_admin(user_id):
        await message.reply_text(
            "❌ **Premium Feature!**\n\n"
            "This feature is only available for premium users and admins.\n"
            "Contact admin to get premium access!",
            quote=True
        )
        return
    
    if len(message.command) != 2:
        current_preset = await db.get_encoding_setting(user_id, 'preset')
        chat_type = "group" if message.chat.type in ['supergroup', 'group'] else "private"
        await message.reply_text(
            f"**Current Preset:** `{current_preset}`\n\n"
            f"**Usage:** `/preset preset_name`\n\n"
            f"**Examples:**\n"
            f"• `/preset ultrafast` - Fastest encoding\n"
            f"• `/preset fast` - Fast encoding\n"
            f"• `/preset medium` - Balanced\n"
            f"• `/preset slow` - Better quality\n"
            f"• `/preset veryslow` - Best quality\n\n"
            f"**Chat Type:** {chat_type}",
            quote=True
        )
        return
    
    preset = message.command[1].strip()
    valid_presets = ['ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow']
    
    if preset not in valid_presets:
        await message.reply_text(
            f"❌ **Invalid preset!**\n\n"
            f"**Supported presets:**\n"
            f"• `ultrafast` - Fastest encoding\n"
            f"• `superfast` - Very fast\n"
            f"• `veryfast` - Fast\n"
            f"• `faster` - Faster\n"
            f"• `fast` - Fast\n"
            f"• `medium` - Balanced (default)\n"
            f"• `slow` - Better quality\n"
            f"• `slower` - Much better quality\n"
            f"• `veryslow` - Best quality",
            quote=True
        )
        return
    
    await db.set_encoding_settings(user_id, 'preset', preset)
    chat_info = f" in {message.chat.title}" if message.chat.type in ['supergroup', 'group'] else ""
    await message.reply_text(
        f"✅ **Preset set to:** `{preset}`{chat_info}\n\n"
        f"This will be used for all your video compressions.",
        quote=True
    )

@Client.on_message(filters.command("encoding_settings") & (filters.private | filters.group))
async def view_encoding_settings(bot: Client, message: Message):
    user_id = message.from_user.id
    
    if not await is_premium_or_admin(user_id):
        await message.reply_text(
            "❌ **Premium Feature!**\n\n"
            "This feature is only available for premium users and admins.",
            quote=True
        )
        return
    
    settings = await db.get_encoding_settings(user_id)
    chat_info = f" in {message.chat.title}" if message.chat.type in ['supergroup', 'group'] else ""
    
    settings_text = f"**Your Current Encoding Settings{chat_info}:**\n\n"
    settings_text += f"**480p CRF:** `{settings.get('crf_480p', 28)}`\n"
    settings_text += f"**720p CRF:** `{settings.get('crf_720p', 26)}`\n"  
    settings_text += f"**1080p CRF:** `{settings.get('crf_1080p', 24)}`\n"
    settings_text += f"**4K CRF:** `{settings.get('crf_4k', 22)}`\n"
    settings_text += f"**Video Codec:** `{settings.get('vcodec', 'libx264')}`\n"
    settings_text += f"**Preset:** `{settings.get('preset', 'veryfast')}`\n\n"
    settings_text += "**Note:** Lower CRF = Better quality, Higher file size"
    
    await message.reply_text(settings_text, quote=True)

@Client.on_message(filters.command("reset_encoding") & (filters.private | filters.group))
async def reset_encoding_settings(bot: Client, message: Message):
    user_id = message.from_user.id
    
    if not await is_premium_or_admin(user_id):
        await message.reply_text(
            "❌ **Premium Feature!**\n\n"
            "This feature is only available for premium users and admins.",
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
    
    chat_info = f" in {message.chat.title}" if message.chat.type in ['supergroup', 'group'] else ""
    await message.reply_text(
        f"✅ **Encoding settings reset to defaults{chat_info}:**\n\n"
        f"**480p CRF:** `28`\n"
        f"**720p CRF:** `26`\n"
        f"**1080p CRF:** `24`\n"
        f"**4K CRF:** `22`\n"
        f"**Video Codec:** `libx264`\n"
        f"**Preset:** `veryfast`",
        quote=True
    )

@Client.on_message(filters.command("premium_status") & (filters.private | filters.group))
async def check_premium_status(bot: Client, message: Message):
    user_id = message.from_user.id
    
    if user_id == Config.ADMIN:
        await message.reply_text(
            "👨‍💼 **Admin Status**\n\n"
            "You have full admin privileges with unlimited access to all features.",
            quote=True
        )
        return
    
    premium_status = await db.get_premium_status(user_id)
    chat_info = f" in {message.chat.title}" if message.chat.type in ['supergroup', 'group'] else ""
    
    if premium_status['is_premium']:
        import datetime
        expiry_time = datetime.datetime.fromtimestamp(premium_status['premium_expires'])
        expiry_str = expiry_time.strftime("%Y-%m-%d %I:%M:%S %p")
        
        status_text = f"👑 **Premium Status{chat_info}**\n\n"
        status_text += f"**Status:** Active Premium User\n"
        status_text += f"**Expires:** {expiry_str}\n"
        status_text += f"**Benefits:**\n"
        status_text += f"• No verification required\n"
        status_text += f"• Custom encoding settings\n"
        status_text += f"• Group access to premium features\n"
        status_text += f"• Priority support"
    else:
        status_text = f"👤 **Regular User Status{chat_info}**\n\n"
        status_text += f"**Status:** Regular User\n"
        status_text += f"**Access:** Basic features only\n"
        status_text += f"**Upgrade:** Contact admin for premium access"
    
    await message.reply_text(status_text, quote=True)
