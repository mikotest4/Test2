from pyrogram import Client, filters
from pyrogram.types import Message
from helper.database import db
from config import Config

# Check if user is premium or admin
async def is_premium_or_admin(user_id):
    if user_id == Config.ADMIN:
        return True
    return await db.is_premium_user(user_id)

@Client.on_message(filters.command("crf_480p") & filters.private)
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
        await message.reply_text(
            f"**Current 480p CRF:** `{current_crf}`\n\n"
            f"**Usage:** `/crf_480p value`\n\n"
            f"**Example:** `/crf_480p 25`\n\n"
            f"**Range:** 0-51 (lower = better quality, higher file size)\n"
            f"**Recommended:** 23-30",
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
        await message.reply_text(
            f"✅ **480p CRF set to:** `{crf_value}`\n\n"
            f"This will be used for all 480p compressions.",
            quote=True
        )
        
    except ValueError:
        await message.reply_text(
            "❌ **Invalid value!**\n\n"
            "Please provide a numeric CRF value (0-51)",
            quote=True
        )

@Client.on_message(filters.command("crf_720p") & filters.private)
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
        await message.reply_text(
            f"**Current 720p CRF:** `{current_crf}`\n\n"
            f"**Usage:** `/crf_720p value`\n\n"
            f"**Example:** `/crf_720p 24`\n\n"
            f"**Range:** 0-51 (lower = better quality, higher file size)\n"
            f"**Recommended:** 23-28",
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
        await message.reply_text(
            f"✅ **720p CRF set to:** `{crf_value}`\n\n"
            f"This will be used for all 720p compressions.",
            quote=True
        )
        
    except ValueError:
        await message.reply_text(
            "❌ **Invalid value!**\n\n"
            "Please provide a numeric CRF value (0-51)",
            quote=True
        )

@Client.on_message(filters.command("crf_1080p") & filters.private)
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
        await message.reply_text(
            f"**Current 1080p CRF:** `{current_crf}`\n\n"
            f"**Usage:** `/crf_1080p value`\n\n"
            f"**Example:** `/crf_1080p 22`\n\n"
            f"**Range:** 0-51 (lower = better quality, higher file size)\n"
            f"**Recommended:** 20-26",
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
        await message.reply_text(
            f"✅ **1080p CRF set to:** `{crf_value}`\n\n"
            f"This will be used for all 1080p compressions.",
            quote=True
        )
        
    except ValueError:
        await message.reply_text(
            "❌ **Invalid value!**\n\n"
            "Please provide a numeric CRF value (0-51)",
            quote=True
        )

@Client.on_message(filters.command("crf_4k") & filters.private)
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
        await message.reply_text(
            f"**Current 4K CRF:** `{current_crf}`\n\n"
            f"**Usage:** `/crf_4k value`\n\n"
            f"**Example:** `/crf_4k 20`\n\n"
            f"**Range:** 0-51 (lower = better quality, higher file size)\n"
            f"**Recommended:** 18-24",
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
        await message.reply_text(
            f"✅ **4K CRF set to:** `{crf_value}`\n\n"
            f"This will be used for all 4K compressions.",
            quote=True
        )
        
    except ValueError:
        await message.reply_text(
            "❌ **Invalid value!**\n\n"
            "Please provide a numeric CRF value (0-51)",
            quote=True
        )

@Client.on_message(filters.command("vcodec") & filters.private)
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
    
    valid_codecs = ['libx264', 'libx265', 'libvpx-vp9', 'libaom-av1', 'h264_nvenc', 'hevc_nvenc']
    
    if len(message.command) != 2:
        current_codec = await db.get_encoding_setting(user_id, 'vcodec')
        codec_list = '\n'.join([f"• `{codec}`" for codec in valid_codecs])
        await message.reply_text(
            f"**Current Video Codec:** `{current_codec}`\n\n"
            f"**Usage:** `/vcodec codec_name`\n\n"
            f"**Example:** `/vcodec libx265`\n\n"
            f"**Available Codecs:**\n{codec_list}\n\n"
            f"**Note:** libx265 = better compression, libx264 = faster encoding",
            quote=True
        )
        return
    
    codec = message.command[1].lower()
    if codec not in valid_codecs:
        codec_list = '\n'.join([f"• `{codec}`" for codec in valid_codecs])
        await message.reply_text(
            f"❌ **Invalid codec!**\n\n"
            f"**Available Codecs:**\n{codec_list}",
            quote=True
        )
        return
    
    await db.set_encoding_settings(user_id, 'vcodec', codec)
    await message.reply_text(
        f"✅ **Video Codec set to:** `{codec}`\n\n"
        f"This will be used for all video compressions.",
        quote=True
    )

@Client.on_message(filters.command("preset") & filters.private)
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
    
    valid_presets = ['ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow']
    
    if len(message.command) != 2:
        current_preset = await db.get_encoding_setting(user_id, 'preset')
        preset_list = '\n'.join([f"• `{preset}`" for preset in valid_presets])
        await message.reply_text(
            f"**Current Preset:** `{current_preset}`\n\n"
            f"**Usage:** `/preset preset_name`\n\n"
            f"**Example:** `/preset fast`\n\n"
            f"**Available Presets:**\n{preset_list}\n\n"
            f"**Note:** faster = quicker encoding, slower = better compression",
            quote=True
        )
        return
    
    preset = message.command[1].lower()
    if preset not in valid_presets:
        preset_list = '\n'.join([f"• `{preset}`" for preset in valid_presets])
        await message.reply_text(
            f"❌ **Invalid preset!**\n\n"
            f"**Available Presets:**\n{preset_list}",
            quote=True
        )
        return
    
    await db.set_encoding_settings(user_id, 'preset', preset)
    await message.reply_text(
        f"✅ **Encoding Preset set to:** `{preset}`\n\n"
        f"This will be used for all video compressions.",
        quote=True
    )

@Client.on_message(filters.command("encoding_settings") & filters.private)
async def view_encoding_settings(bot: Client, message: Message):
    user_id = message.from_user.id
    
    if not await is_premium_or_admin(user_id):
        await message.reply_text(
            "❌ **Premium Feature!**\n\n"
            "This feature is only available for premium users and admins.\n"
            "Contact admin to get premium access!",
            quote=True
        )
        return
    
    settings = await db.get_encoding_settings(user_id)
    
    settings_text = (
        f"⚙️ **Your Encoding Settings:**\n\n"
        f"**CRF Values:**\n"
        f"• 480p: `{settings['crf_480p']}`\n"
        f"• 720p: `{settings['crf_720p']}`\n"
        f"• 1080p: `{settings['crf_1080p']}`\n"
        f"• 4K: `{settings['crf_4k']}`\n\n"
        f"**Video Codec:** `{settings['vcodec']}`\n"
        f"**Preset:** `{settings['preset']}`\n\n"
        f"**Commands to modify:**\n"
        f"• `/crf_480p value` - Set 480p CRF\n"
        f"• `/crf_720p value` - Set 720p CRF\n"
        f"• `/crf_1080p value` - Set 1080p CRF\n"
        f"• `/crf_4k value` - Set 4K CRF\n"
        f"• `/vcodec codec` - Set video codec\n"
        f"• `/preset preset` - Set encoding preset"
    )
    
    await message.reply_text(settings_text, quote=True)

@Client.on_message(filters.command("reset_encoding") & filters.private)
async def reset_encoding_settings(bot: Client, message: Message):
    user_id = message.from_user.id
    
    if not await is_premium_or_admin(user_id):
        await message.reply_text(
            "❌ **Premium Feature!**\n\n"
            "This feature is only available for premium users and admins.\n"
            "Contact admin to get premium access!",
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
    
    await message.reply_text(
        f"✅ **Encoding settings reset to defaults:**\n\n"
        f"• 480p CRF: `28`\n"
        f"• 720p CRF: `26`\n"
        f"• 1080p CRF: `24`\n"
        f"• 4K CRF: `22`\n"
        f"• Video Codec: `libx264`\n"
        f"• Preset: `veryfast`",
        quote=True
    )
