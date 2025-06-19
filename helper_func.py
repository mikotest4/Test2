import aiohttp
import string
import random
import time
import asyncio
from config import Config

async def get_shortlink(url, api, original_link):
    """
    Generate shortened link using shortener service
    """
    if not url or not api:
        return original_link
    
    try:
        async with aiohttp.ClientSession() as session:
            # Different APIs have different formats, adjust as needed
            api_url = f'https://{url}/api?api={api}&url={original_link}'
            
            async with session.get(api_url, timeout=10) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    # Adjust this based on your shortener's response format
                    if 'shortenedUrl' in data:
                        return data['shortenedUrl']
                    elif 'short_url' in data:
                        return data['short_url']
                    elif 'result' in data:
                        return data['result']
                    else:
                        return original_link
                else:
                    return original_link
    except Exception as e:
        print(f"Shortlink generation failed: {e}")
        return original_link

def get_exp_time(seconds):
    """
    Convert seconds to human readable time format
    """
    if seconds == 0:
        return "0 seconds"
    
    periods = [
        ('day', 86400),
        ('hour', 3600), 
        ('minute', 60),
        ('second', 1)
    ]
    
    result = []
    for period_name, period_seconds in periods:
        if seconds >= period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            result.append(f"{period_value} {period_name}{'s' if period_value > 1 else ''}")
    
    return ', '.join(result) if result else '0 seconds'

def generate_verification_token(length=10):
    """
    Generate random verification token
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

async def is_user_verified(user_id, db):
    """
    Check if user verification is valid and not expired
    """
    verify_status = await db.get_verify_status(user_id)
    
    # Check if token expired
    verified_time = verify_status.get('verified_time', 0)
    try:
        verified_time = float(verified_time) if verified_time else 0
    except (ValueError, TypeError):
        verified_time = 0
    
    # If verified but expired, mark as unverified
    if verify_status['is_verified'] and Config.VERIFY_EXPIRE < (time.time() - verified_time):
        await db.update_verify_status(user_id, is_verified=False)
        return False
    
    return verify_status['is_verified']

async def create_verification_link(user_id, bot_username, db):
    """
    Create verification link with token
    """
    token = generate_verification_token()
    await db.update_verify_status(user_id, verify_token=token, link="")
    
    bot_link = f'https://telegram.dog/{bot_username}?start=verify_{token}'
    
    if Config.SHORTLINK_URL and Config.SHORTLINK_API:
        shortened_link = await get_shortlink(Config.SHORTLINK_URL, Config.SHORTLINK_API, bot_link)
        return shortened_link
    else:
        return bot_link
