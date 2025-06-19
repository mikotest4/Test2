import os, time, re

id_pattern = re.compile(r'^.\d+$') 

class Config(object):
    # pyro client config
    API_ID    = os.environ.get("API_ID", "20071888")  # ⚠️ Required
    API_HASH  = os.environ.get("API_HASH", "1c4cb9d94b23282abd9ae2a87a521b53") # ⚠️ Required
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "7540338860:AAGuZGaIVQ8lXn8dPy9LGTvviCRwfzyxifc") # ⚠️ Required
    FORCE_SUB = os.environ.get('FORCE_SUB', '-1002669902570') # ⚠️ Required
    AUTH_CHANNEL = int(FORCE_SUB) if FORCE_SUB and id_pattern.search(FORCE_SUB) else None
   
    # database config
    DB_URI  = os.environ.get("DB_URI", "mongodb+srv://rani828719:sVyRWZOrUzIWNfHp@cluster0.zodktob.mongodb.net/?retryWrites=true&w=majority")  # ⚠️ Required
    DB_NAME  = os.environ.get("DB_NAME","SnowEncoderBot") 

    # Other Configs 
    ADMIN = int(os.environ.get("ADMIN", "7970350353")) # ⚠️ Required
    LOG_CHANNEL = int(os.environ.get('LOG_CHANNEL', '-1002669902570')) # ⚠️ Required
    BOT_UPTIME = BOT_UPTIME  = time.time()
    START_PIC = os.environ.get("START_PIC", "https://graph.org/file/15e82d7e665eccc8bd9c5.jpg")

    # Shortener Configuration
    SHORTLINK_URL = os.environ.get("SHORTLINK_URL", "shortner.in")
    SHORTLINK_API = os.environ.get("SHORTLINK_API", "your_api_key_here")
    VERIFY_EXPIRE = int(os.environ.get('VERIFY_EXPIRE', "86400"))  # 24 hours in seconds
    TUT_VID = os.environ.get("TUT_VID", "https://t.me/+yReU8NWVB-s3YzNl")

    # Premium Configuration
    PREMIUM_ENABLED = True  # Enable premium features
    MAX_CONCURRENT_NON_PREMIUM = 1  # Non-premium users can encode only 1 file at a time
    MAX_CONCURRENT_PREMIUM = 10  # Premium users can encode up to 10 files simultaneously

    # wes response configuration     
    WEBHOOK = bool(os.environ.get("WEBHOOK", True))
    PORT = int(os.environ.get("PORT", "3730"))

    caption = """
**File Name**: {0}

**Original File Size:** {1}
**Encoded File Size:** {2}
**Compression Percentage:** {3}

__Downloaded in {4}__
__Encoded in {5}__
__Uploaded in {6}__
"""
