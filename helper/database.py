import aiohttp
import string
import random
import time
import asyncio
from config import Config

# Import premium functions
try:
    from database.db_premium import is_premium_user, check_user_plan
except ImportError:
    # Fallback if premium module not available
    async def is_premium_user(user_id):
        return False
    async def check_user_plan(user_id):
        return None

# Global queue management
USER_QUEUES = {}  # {user_id: [{'file': file_obj, 'message': msg_obj, 'status': 'waiting/processing/completed'}]}
ACTIVE_PROCESSES = {}  # {user_id: count_of_active_processes}

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
    # Premium users and admins skip verification
    if user_id == Config.ADMIN or await is_premium_user(user_id):
        return True
        
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

# QUEUE MANAGEMENT FUNCTIONS
async def can_process_file(user_id):
    """
    Check if user can process a new file based on their limits
    """
    is_premium = await is_premium_user(user_id)
    is_admin = user_id == Config.ADMIN
    
    if is_admin:
        return True, "Admin - Unlimited access"
    
    current_active = ACTIVE_PROCESSES.get(user_id, 0)
    
    if is_premium:
        max_allowed = Config.MAX_CONCURRENT_PREMIUM
        if current_active < max_allowed:
            return True, f"Premium user - {current_active}/{max_allowed} slots used"
        else:
            return False, f"Premium limit reached - {current_active}/{max_allowed} files processing"
    else:
        max_allowed = Config.MAX_CONCURRENT_NON_PREMIUM
        if current_active < max_allowed:
            return True, f"Free user - {current_active}/{max_allowed} slots used"
        else:
            return False, f"Free user limit reached - {current_active}/{max_allowed} files processing"

async def add_to_queue(user_id, file_obj, message_obj, operation_type="encode"):
    """
    Add file to user's processing queue
    """
    if user_id not in USER_QUEUES:
        USER_QUEUES[user_id] = []
    
    queue_item = {
        'file': file_obj,
        'message': message_obj,
        'operation': operation_type,
        'status': 'waiting',
        'added_time': time.time(),
        'queue_position': len(USER_QUEUES[user_id]) + 1
    }
    
    USER_QUEUES[user_id].append(queue_item)
    return queue_item['queue_position']

async def start_processing(user_id):
    """
    Start processing next file in queue if possible
    """
    if user_id not in USER_QUEUES or not USER_QUEUES[user_id]:
        return False
    
    can_process, reason = await can_process_file(user_id)
    if not can_process:
        return False
    
    # Find next waiting item
    for item in USER_QUEUES[user_id]:
        if item['status'] == 'waiting':
            item['status'] = 'processing'
            ACTIVE_PROCESSES[user_id] = ACTIVE_PROCESSES.get(user_id, 0) + 1
            return True
    
    return False

async def finish_processing(user_id, success=True):
    """
    Mark processing as finished and start next in queue
    """
    if user_id in ACTIVE_PROCESSES:
        ACTIVE_PROCESSES[user_id] = max(0, ACTIVE_PROCESSES[user_id] - 1)
    
    # Remove completed items from queue
    if user_id in USER_QUEUES:
        USER_QUEUES[user_id] = [item for item in USER_QUEUES[user_id] if item['status'] != 'processing']
        
        # Update queue positions
        for i, item in enumerate(USER_QUEUES[user_id]):
            item['queue_position'] = i + 1
    
    # Start next file if any waiting
    await start_processing(user_id)

async def get_queue_status(user_id):
    """
    Get user's queue status
    """
    if user_id not in USER_QUEUES:
        return {
            'total_queued': 0,
            'processing': 0,
            'waiting': 0,
            'queue_items': []
        }
    
    queue = USER_QUEUES[user_id]
    processing = len([item for item in queue if item['status'] == 'processing'])
    waiting = len([item for item in queue if item['status'] == 'waiting'])
    
    return {
        'total_queued': len(queue),
        'processing': processing,
        'waiting': waiting,
        'queue_items': queue
    }

async def clear_user_queue(user_id):
    """
    Clear all items from user's queue
    """
    if user_id in USER_QUEUES:
        del USER_QUEUES[user_id]
    if user_id in ACTIVE_PROCESSES:
        del ACTIVE_PROCESSES[user_id]

def format_queue_display(queue_status, is_premium, is_admin):
    """
    Format queue status for display
    """
    if queue_status['total_queued'] == 0:
        return "📭 **Queue is empty**\n\nNo files in processing queue."
    
    text = f"📊 **Queue Status**\n\n"
    text += f"🔄 **Processing:** {queue_status['processing']}\n"
    text += f"⏳ **Waiting:** {queue_status['waiting']}\n"
    text += f"📁 **Total:** {queue_status['total_queued']}\n\n"
    
    if is_admin:
        text += f"👑 **Admin:** Unlimited concurrent processing\n\n"
    elif is_premium:
        text += f"⭐ **Premium:** Up to {Config.MAX_CONCURRENT_PREMIUM} concurrent files\n\n"
    else:
        text += f"🆓 **Free:** Up to {Config.MAX_CONCURRENT_NON_PREMIUM} concurrent file\n\n"
    
    if queue_status['queue_items']:
        text += "📋 **Queue Items:**\n"
        for i, item in enumerate(queue_status['queue_items'][:5], 1):
            status_emoji = "🔄" if item['status'] == 'processing' else "⏳"
            file_name = getattr(item['file'], 'file_name', 'Unknown file')[:30]
            text += f"{status_emoji} {i}. {file_name}...\n"
        
        if len(queue_status['queue_items']) > 5:
            text += f"... and {len(queue_status['queue_items']) - 5} more files\n"
    
    return text

async def check_queue_and_process(user_id, file_obj, message_obj, operation_type="encode"):
    """
    Check if user can process file immediately or add to queue
    """
    can_process, reason = await can_process_file(user_id)
    
    if can_process:
        # Start processing immediately
        ACTIVE_PROCESSES[user_id] = ACTIVE_PROCESSES.get(user_id, 0) + 1
        return True, f"✅ Processing started - {reason}"
    else:
        # Add to queue
        is_premium = await is_premium_user(user_id)
        is_admin = user_id == Config.ADMIN
        
        if not is_premium and not is_admin:
            return False, f"❌ {reason}\n\nUpgrade to premium for queue management!"
        
        queue_position = await add_to_queue(user_id, file_obj, message_obj, operation_type)
        return False, f"📋 Added to queue at position {queue_position}\n{reason}"
