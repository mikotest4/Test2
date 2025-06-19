class Txt(object):

    PRIVATE_START_MSG = """
Hɪ {},

I'ᴍ Fɪʟᴇs Eɴᴄᴏᴅᴇʀ ʙᴏᴛ ᴄᴀɴ ᴅᴏ ᴄᴏᴍᴘʀᴇss ʏᴏᴜʀ ғɪʟᴇs ɪɴ ɴᴇɢʟɪɢɪʙʟᴇ ᴡɪᴛʜᴏᴜᴛ ʟᴏss ᴏғ ǫᴜᴀʟɪᴛɪᴇs ᴊᴜsᴛ sᴇɴᴅ ᴍᴇ ᴠɪᴅᴇᴏ

**📋 Access Levels:**
• 👨‍💼 **Admin:** DM + Groups (No verification)
• 👑 **Premium:** Groups only (No verification) 
• 👤 **Regular:** Groups only (Verification required)

**💡 Note:** Only Bot Admin has DM encoding privileges.
"""
    GROUP_START_MSG = """
Hɪ {},

I'ᴍ Fɪʟᴇs Eɴᴄᴏᴅᴇʀ ʙᴏᴛ ᴄᴀɴ ᴄᴏᴍᴘʀᴇss ʏᴏᴜʀ ғɪʟᴇs ᴛᴏ ɴᴇɢʟɪɢɪʙʟᴇ sɪᴢᴇ ᴡɪᴛʜᴏᴜᴛ ʟᴏᴏsɪɴɢ ᴛʜᴇ ǫᴜᴀʟɪᴛɪᴇs ᴊᴜsᴛ sᴇɴᴅ ᴍᴇ ᴠɪᴅᴇᴏ

❗**Yᴏᴜ ʜᴀsɴ'ᴛ sᴛᴀʀᴛᴇᴅ ᴍᴇ ʏᴇᴛ ᴛᴏ ᴜsᴇ ᴍᴇ ғɪʀsᴛ sᴛᴀʀᴛ ᴍᴇ sᴏ ɪ ᴄᴀɴ ᴡᴏʀᴋ ғʟᴀᴡʟᴇssʟʏ**

**🎉 Great News:** 
• Premium users: No verification needed!
• Regular users: Quick verification required
"""
    PROGRESS_BAR = """<b>
╭━━━━❰ᴘʀᴏɢʀᴇss ʙᴀʀ❱━➣
┣⪼ 🗃️ Sɪᴢᴇ: {1} | {2}
┣⪼ ⏳️ Dᴏɴᴇ : {0}%
┣⪼ 🚀 Sᴩᴇᴇᴅ: {3}/s
┣⪼ ⏰️ Eᴛᴀ: {4}
╰━━━━━━━━━━━━━━━➣ </b>"""

    SEND_FFMPEG_CODE = """
❪ SET CUSTOM FFMPEG CODE ❫

Send me the correct ffmpeg code for more info.


☛ <a href=https://unix.stackexchange.com/questions/28803/how-can-i-reduce-a-videos-size-with-ffmpeg#:~:text=ffmpeg%20%2Di%20input.mp4%20%2Dvcodec%20libx265%20%2Dcrf%2028%20output.mp4> FOR HELP </a>

⦿ Fᴏʀᴍᴀᴛ Oɴ Hᴏᴡ Tᴏ Sᴇᴛ

☞ ffmpeg -i input.mp4 <code> -c:v libx264 -crf 23 </code> output.mp4

<code> -c:v libx264 -crf 23 </code> Tʜɪs ɪs ʏᴏᴜʀ ғғᴍᴘᴇɢ ᴄᴏᴅᴇ ✅

📥 Fᴏʀ Hᴇʟᴘ[Cᴏɴᴛ](https://t.me/+6LwHBLWZc3IyMTU1) 
"""

    SEND_METADATA ="""
❪ SET CUSTOM METADATA ❫

☞ Fᴏʀ Exᴀᴍᴘʟᴇ:-

◦ <code> -map 0 -c:s copy -c:a copy -c:v copy -metadata title="My Video" -metadata author="John Doe" -metadata:s:s title="Subtitle Title" -metadata:s:a title="Audio Title" -metadata:s:v title="Video Title" </code>

📥 Fᴏʀ Hᴇʟᴘ [Cᴏɴᴛ](https://t.me/+6LwHBLWZc3IyMTU1) 
"""

    
    HELP_MSG = """
**🎥 Basic Commands:**
➜ /set_ffmpeg - To set custom ffmpeg code
➜ /set_metadata - To set custom metadata code
➜ /set_caption - To set custom caption
➜ /del_ffmpeg - Delete the custom ffmpeg code
➜ /del_caption - Delete caption
➜ /see_ffmpeg - View custom ffmpeg code
➜ /see_metadata - View custom metadata code
➜ /see_caption - View caption 
➜ To Set Thumbnail just send photo

**📋 Access Levels & Restrictions:**
• 👨‍💼 **Admin:** DM + Groups (No verification)
• 👑 **Premium:** Groups only (No verification)
• 👤 **Regular:** Groups only (Verification required)

**❗ Important:** Only Bot Admin can encode in DM!

**👑 Premium Commands:**
➜ /crf_480p - Set CRF for 480p compression
➜ /crf_720p - Set CRF for 720p compression  
➜ /crf_1080p - Set CRF for 1080p compression
➜ /crf_4k - Set CRF for 4K compression
➜ /vcodec - Set video codec (libx264/libx265/etc)
➜ /preset - Set encoding preset (fast/slow/etc)
➜ /encoding_settings - View all encoding settings
➜ /reset_encoding - Reset to default settings
➜ /premium_status - Check premium status

**🔧 Admin Commands:**
➜ /addpremium - Add premium user
➜ /revpremium - Remove premium user
➜ /premiumusers - List premium users
➜ /stats - Bot statistics
➜ /broadcast - Broadcast message
➜ /ban_user - Ban user
➜ /unban_user - Unban user

<b>⦿ Developer:</b> <a href=https://t.me/+6LwHBLWZc3IyMTU1>꧁༺ 𝓣𝓔𝓒𝓗_𝓗𝓔𝓡𝓞 ༻꧂ ❄️</a>
"""

    ABOUT_TXT = """<b>╭───────────⍟
├🤖 ᴍy ɴᴀᴍᴇ : @{}
├👨‍💻 Pʀᴏɢʀᴀᴍᴇʀ : <a href=https://t.me/+6LwHBLWZc3IyMTU1>꧁༺ 𝓣𝓔𝓒𝓗_𝓗𝓔𝓡𝓞 ༻꧂</a>
├👑 Instagram : <a href=https://t.me/+6LwHBLWZc3IyMTU1>C-Insta</a> 
├☃️ ꜰᴏᴜɴᴅᴇʀ ᴏꜰ : <a href=https://t.me/+6LwHBLWZc3IyMTU1>K-Lᴀɴᴅ</a>
├📕 Lɪʙʀᴀʀy : <a href=https://github.com/pyrogram>Pyʀᴏɢʀᴀᴍ</a>
├✏️ Lᴀɴɢᴜᴀɢᴇ: <a href=https://www.python.org>Pyᴛʜᴏɴ 3</a>
├💾 Dᴀᴛᴀ Bᴀꜱᴇ: <a href=https://cloud.mongodb.com>Mᴏɴɢᴏ DB</a>
├🌀 ᴍʏ ꜱᴇʀᴠᴇʀ : <a href=https://t.me/+6LwHBLWZc3IyMTU1>Click ker ke dekh lo😎😋</a>
├🚫 DM Encoding : Admin Only
├👥 Group Encoding : All Users
├👑 Premium Benefits : No verification needed
╰───────────────⍟ """
