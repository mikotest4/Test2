import datetime
import motor.motor_asyncio
from config import Config
from .utils import send_log

class Database:

    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users

    def new_user(self, id):
        return dict(
            id=int(id),
            join_date=datetime.date.today().isoformat(),
            caption=None,
            thumbnail=None,
            ffmpegcode=None,
            metadata=""" -map 0 -c:s copy -c:a copy -c:v copy -metadata title="Powered By:- @Kdramaland" -metadata author="@Snowball_Official" -metadata:s:s title="Subtitled By :- @Kdramaland" -metadata:s:a title="By :- @Kdramaland" -metadata:s:v title="By:- @Snowball_Official" """,
            encoding_settings=dict(
                crf_480p=28,
                crf_720p=26,
                crf_1080p=24,
                crf_4k=22,
                vcodec='libx264',
                preset='veryfast'
            ),
            premium_status=dict(
                is_premium=False,
                premium_expires=0,
                added_by=None,
                added_on=None
            ),
            verify_status=dict(
                is_verified=False,
                verified_time=0,
                verify_token="",
                link=""
            ),
            ban_status=dict(
                is_banned=False,
                ban_duration=0,
                banned_on=datetime.date.max.isoformat(),
                ban_reason=''
            )
        )

    # PREMIUM USER METHODS
    async def add_premium_user(self, user_id, duration_seconds, added_by):
        """Add premium access to user"""
        expiry_time = datetime.datetime.now().timestamp() + duration_seconds
        premium_status = dict(
            is_premium=True,
            premium_expires=expiry_time,
            added_by=added_by,
            added_on=datetime.datetime.now().isoformat()
        )
        await self.col.update_one({'id': int(user_id)}, {'$set': {'premium_status': premium_status}}, upsert=True)

    async def remove_premium_user(self, user_id):
        """Remove premium access from user"""
        premium_status = dict(
            is_premium=False,
            premium_expires=0,
            added_by=None,
            added_on=None
        )
        await self.col.update_one({'id': int(user_id)}, {'$set': {'premium_status': premium_status}})

    async def get_premium_status(self, user_id):
        """Get premium status of user"""
        user = await self.col.find_one({'id': int(user_id)})
        if user:
            premium_status = user.get('premium_status', {
                'is_premium': False,
                'premium_expires': 0,
                'added_by': None,
                'added_on': None
            })
            
            # Check if premium has expired
            if premium_status['is_premium'] and premium_status['premium_expires'] < datetime.datetime.now().timestamp():
                await self.remove_premium_user(user_id)
                return {
                    'is_premium': False,
                    'premium_expires': 0,
                    'added_by': None,
                    'added_on': None
                }
            
            return premium_status
        return {
            'is_premium': False,
            'premium_expires': 0,
            'added_by': None,
            'added_on': None
        }

    async def get_all_premium_users(self):
        """Get all premium users"""
        premium_users = self.col.find({'premium_status.is_premium': True})
        return premium_users

    async def is_premium_user(self, user_id):
        """Check if user is premium"""
        premium_status = await self.get_premium_status(user_id)
        return premium_status['is_premium']

    # ENCODING SETTINGS METHODS
    async def set_encoding_settings(self, user_id, settings_type, value):
        """Set encoding settings for user"""
        await self.col.update_one(
            {'id': int(user_id)}, 
            {'$set': {f'encoding_settings.{settings_type}': value}}, 
            upsert=True
        )

    async def get_encoding_settings(self, user_id):
        """Get all encoding settings for user"""
        user = await self.col.find_one({'id': int(user_id)})
        if user:
            return user.get('encoding_settings', {
                'crf_480p': 28,
                'crf_720p': 26,
                'crf_1080p': 24,
                'crf_4k': 22,
                'vcodec': 'libx264',
                'preset': 'veryfast'
            })
        return {
            'crf_480p': 28,
            'crf_720p': 26,
            'crf_1080p': 24,
            'crf_4k': 22,
            'vcodec': 'libx264',
            'preset': 'veryfast'
        }

    async def get_encoding_setting(self, user_id, setting_type):
        """Get specific encoding setting"""
        settings = await self.get_encoding_settings(user_id)
        return settings.get(setting_type)

    # VERIFICATION METHODS
    async def get_verify_status(self, user_id):
        user = await self.col.find_one({'id': int(user_id)})
        if user:
            return user.get('verify_status', {
                'is_verified': False,
                'verified_time': 0,
                'verify_token': "",
                'link': ""
            })
        return {
            'is_verified': False,
            'verified_time': 0,
            'verify_token': "",
            'link': ""
        }

    async def update_verify_status(self, user_id, verify_token="", is_verified=False, verified_time=0, link=""):
        current = await self.get_verify_status(user_id)
        current['verify_token'] = verify_token
        current['is_verified'] = is_verified
        current['verified_time'] = verified_time
        current['link'] = link
        await self.col.update_one({'id': int(user_id)}, {'$set': {'verify_status': current}}, upsert=True)

    # EXISTING METHODS
    async def set_caption(self, user_id, caption):
        await self.col.update_one({'id': int(user_id)}, {'$set': {'caption': caption}})

    async def get_caption(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('caption', None)
    
    async def set_thumbnail(self, user_id, thumbnail):
        await self.col.update_one({'id': int(user_id)}, {'$set': {'thumbnail': thumbnail}})

    async def get_thumbnail(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('thumbnail', None)
    
    async def set_ffmpegcode(self, user_id, ffmpegcode):
        await self.col.update_one({'id': int(user_id)}, {'$set': {'ffmpegcode': ffmpegcode}})

    async def get_ffmpegcode(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('ffmpegcode', None)
    
    async def set_metadata(self, user_id, metadata):
        await self.col.update_one({'id': int(user_id)}, {'$set': {'metadata': metadata}})

    async def get_metadata(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('metadata', None)

    async def add_user(self, b, m):
        u = m.from_user
        if not await self.is_user_exist(u.id):
            user = self.new_user(u.id)
            await self.col.insert_one(user)
            await send_log(b, u)

    async def is_user_exist(self, id):
        user = await self.col.find_one({'id': int(id)})
        return bool(user)

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users

    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})

    async def remove_ban(self, id):
        ban_status = dict(
            is_banned=False,
            ban_duration=0,
            banned_on=datetime.date.max.isoformat(),
            ban_reason=''
        )
        await self.col.update_one({'id': id}, {'$set': {'ban_status': ban_status}})

    async def ban_user(self, user_id, ban_duration, ban_reason):
        ban_status = dict(
            is_banned=True,
            ban_duration=ban_duration,
            banned_on=datetime.date.today().isoformat(),
            ban_reason=ban_reason
        )
        await self.col.update_one({'id': user_id}, {'$set': {'ban_status': ban_status}})

    async def get_ban_status(self, id):
        default = dict(
            is_banned=False,
            ban_duration=0,
            banned_on=datetime.date.max.isoformat(),
            ban_reason=''
        )
        user = await self.col.find_one({'id': int(id)})
        return user.get('ban_status', default)

    async def get_all_banned_users(self):
        banned_users = self.col.find({'ban_status.is_banned': True})
        return banned_users

db = Database(Config.DB_URL, Config.DB_NAME)
