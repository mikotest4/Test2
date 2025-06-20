import os, time, re

id_pattern = re.compile(r'^.\d+$') 

class Config(object):
    # pyro client config
    API_ID    = os.environ.get("API_ID", "20071888")  # ⚠️ Required
    API_HASH  = os.environ.get("API_HASH", "1c4cb9d94b23282abd9ae2a87a521b53") # ⚠️ Required
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "7540338860:AAG7oNnC9Jqw39Dcjf8KWonc0T2byWfzrJ0") # ⚠️ Required
    FORCE_SUB = os.environ.get('FORCE_SUB', '-1002669902570') # ⚠️ Required
    AUTH_CHANNEL = int(FORCE_SUB) if FORCE_SUB and id_pattern.search(FORCE_SUB) else None
   
    # database config
    DB_URL  = os.environ.get("DB_URL", "mongodb+srv://rani828719:sVyRWZOrUzIWNfHp@cluster0.zodktob.mongodb.net/?retryWrites=true&w=majority")  # ⚠️ Required
    DB_NAME  = os.environ.get("DB_NAME","SnowEncoderBot") 

    # Other Configs 
    ADMIN = int(os.environ.get("ADMIN", "7970350353")) # ⚠️ Required
    LOG_CHANNEL = int(os.environ.get('LOG_CHANNEL', '-1002669902570')) # ⚠️ Required
    BOT_UPTIME = BOT_UPTIME  = time.time()
    START_PIC = os.environ.get("START_PIC", "https://graph.org/file/15e82d7e665eccc8bd9c5.jpg")
    FORCE_SUB_PIC = os.environ.get("FORCE_SUB_PIC", "https://graph.org/file/15e82d7e665eccc8bd9c5.jpg")
    
    # Shortener Configuration
    SHORTLINK_URL = os.environ.get("SHORTLINK_URL", "reel2earn.com")
    SHORTLINK_API = os.environ.get("SHORTLINK_API", "74508ee9f003899307cca7addf6013053e1f567e")
    VERIFY_EXPIRE = int(os.environ.get('VERIFY_EXPIRE', "86400"))  # 24 hours in seconds
    TUT_VID = os.environ.get("TUT_VID", "https://t.me/+yReU8NWVB-s3YzNl")

    # wes response configuration     
    WEBHOOK = bool(os.environ.get("WEBHOOK", True))
    PORT = int(os.environ.get("PORT", "3731"))

    caption = """
**File Name**: {0}

**Original File Size:** {1}
**Encoded File Size:** {2}
**Compression Percentage:** {3}

__Downloaded in {4}__
__Encoded in {5}__
__Uploaded in {6}__
"""
