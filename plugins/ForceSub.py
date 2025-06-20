from pyrogram import Client, filters, enums 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant
from config import Config
from helper.database import db

async def not_subscribed(_, client, message):
    await db.add_user(client, message)
    if not Config.AUTH_CHANNEL:
        return False
    try:             
        user = await client.get_chat_member(Config.AUTH_CHANNEL, message.from_user.id) 
        if user.status == enums.ChatMemberStatus.BANNED:
            return True 
        else:
            return False                
    except UserNotParticipant:
        pass
    return True


# Only check force sub for start command
@Client.on_message(
    (filters.private | filters.group) & 
    filters.command("start") & 
    filters.create(not_subscribed)
)
async def forces_sub_start(client, message):
    invite_link = await client.create_chat_invite_link(int(Config.AUTH_CHANNEL))
    buttons = [
        [InlineKeyboardButton(text="📢 Join Update Channel 📢", url=invite_link.invite_link) ],
    ]
    text = "**Sᴏʀʀy Yᴏᴜ'ʀᴇ Nᴏᴛ Jᴏɪɴᴇᴅ My Cʜᴀɴɴᴇʟ 😐. Sᴏ Pʟᴇᴀꜱᴇ Jᴏɪɴ Oᴜʀ Uᴩᴅᴀᴛᴇ Cʜᴀɴɴᴇʟ Tᴏ Cᴄᴏɴᴛɪɴᴜᴇ**"

    # Add photo to force sub message
    if hasattr(Config, 'FORCE_SUB_PIC') and Config.FORCE_SUB_PIC:
        return await message.reply_photo(
            photo=Config.FORCE_SUB_PIC,
            caption=text, 
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    else:
        return await message.reply_text(
            text=text, 
            reply_markup=InlineKeyboardMarkup(buttons)
        )


# Only check force sub for files (videos, audio, documents)
@Client.on_message(
    (filters.private | filters.group) & 
    (filters.document | filters.audio | filters.video) & 
    ~filters.sticker & 
    ~filters.animation & 
    filters.create(not_subscribed)
)
async def forces_sub_files(client, message):
    invite_link = await client.create_chat_invite_link(int(Config.AUTH_CHANNEL))
    buttons = [
        [InlineKeyboardButton(text="📢 Join Update Channel 📢", url=invite_link.invite_link) ],
    ]
    text = "**Sᴏʀʀy Yᴏᴜ'ʀᴇ Nᴏᴛ Jᴏɪɴᴇᴅ My Cʜᴀɴɴᴇʟ 😐. Sᴏ Pʟᴇᴀꜱᴇ Jᴏɪɴ Oᴜʀ Uᴩᴅᴀᴛᴇ Cʜᴀɴɴᴇʟ Tᴏ Cᴄᴏɴᴛɪɴᴜᴇ**"

    # Add photo to force sub message for files
    if hasattr(Config, 'FORCE_SUB_PIC') and Config.FORCE_SUB_PIC:
        return await message.reply_photo(
            photo=Config.FORCE_SUB_PIC,
            caption=text, 
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    else:
        return await message.reply_text(
            text=text, 
            reply_markup=InlineKeyboardMarkup(buttons)
        )
