from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from database.db_premium import add_premium, remove_premium, list_premium_users, check_user_plan, is_premium_user, get_premium_stats
from helper_func import get_queue_status, format_queue_display, clear_user_queue
from config import Config
import re

# Admin command to add premium
@Client.on_message(filters.command("addpremium") & filters.user(Config.ADMIN))
async def add_premium_cmd(client: Client, message: Message):
    try:
        if len(message.command) < 4:
            return await message.reply_text(
                "**Usage:** `/addpremium <user_id> <time_value> <time_unit>`\n\n"
                "**Time units:**\n"
                "• `s` = seconds\n"
                "• `m` = minutes\n" 
                "• `h` = hours\n"
                "• `d` = days\n"
                "• `y` = years\n\n"
                "**Examples:**\n"
                "• `/addpremium 5732678985 30 d` (30 days)\n"
                "• `/addpremium 5732678985 30 m` (30 minutes)\n"
                "• `/addpremium 5732678985 1 y` (1 year)"
            )
        
        user_id = int(message.command[1])
        time_value = int(message.command[2])
        time_unit = message.command[3].lower()
        
        if time_unit not in ['s', 'm', 'h', 'd', 'y']:
            return await message.reply_text("❌ Invalid time unit. Use: s, m, h, d, or y")
        
        if time_value <= 0:
            return await message.reply_text("❌ Time value must be positive")
        
        expiration_time = await add_premium(user_id, time_value, time_unit)
        
        # Send notification to user
        try:
            await client.send_message(
                user_id,
                f"🎉 **Premium Access Granted!**\n\n"
                f"⭐ You now have premium access\n"
                f"📅 **Expires:** {expiration_time}\n\n"
                f"**Premium Benefits:**\n"
                f"• ✅ No verification required\n"
                f"• 🚀 Up to {Config.MAX_CONCURRENT_PREMIUM} concurrent encodings\n"
                f"• ⚡ Priority processing\n"
                f"• 📊 Queue management with /queue\n\n"
                f"Enjoy your premium experience! 🎬"
            )
        except:
            pass
        
        await message.reply_text(
            f"✅ **Premium Added Successfully**\n\n"
            f"👤 **User ID:** `{user_id}`\n"
            f"⏰ **Duration:** {time_value} {time_unit}\n"
            f"📅 **Expires:** {expiration_time}\n\n"
            f"User has been notified about their premium access."
        )
        
    except ValueError:
        await message.reply_text("❌ Invalid user ID or time value. Please use numbers only.")
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

# Admin command to remove premium
@Client.on_message(filters.command("removepremium") & filters.user(Config.ADMIN))
async def remove_premium_cmd(client: Client, message: Message):
    try:
        if len(message.command) < 2:
            return await message.reply_text(
                "**Usage:** `/removepremium <user_id>`\n\n"
                "**Example:** `/removepremium 5732678985`"
            )
        
        user_id = int(message.command[1])
        
        if await remove_premium(user_id):
            # Clear user's queue
            await clear_user_queue(user_id)
            
            # Notify user
            try:
                await client.send_message(
                    user_id,
                    "❌ **Premium Access Removed**\n\n"
                    "Your premium access has been revoked by an admin.\n"
                    "You now have free user limitations.\n\n"
                    "Contact support if you think this is an error."
                )
            except:
                pass
            
            await message.reply_text(
                f"✅ **Premium Removed**\n\n"
                f"👤 **User ID:** `{user_id}`\n"
                f"🗑️ **Queue:** Cleared\n\n"
                f"User has been notified."
            )
        else:
            await message.reply_text(f"❌ User `{user_id}` was not a premium user.")
            
    except ValueError:
        await message.reply_text("❌ Invalid user ID. Please use numbers only.")
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

# Admin command to list premium users
@Client.on_message(filters.command("premiumlist") & filters.user(Config.ADMIN))
async def premium_list_cmd(client: Client, message: Message):
    try:
        premium_users = await list_premium_users()
        stats = await get_premium_stats()
        
        if not premium_users:
            return await message.reply_text(
                "📭 **No Premium Users**\n\n"
                f"📊 **Stats:** {stats['total']} total, {stats['active']} active, {stats['expired']} expired"
            )
        
        text = f"⭐ **Premium Users List**\n\n"
        text += f"📊 **Stats:** {stats['active']} active, {stats['expired']} expired\n\n"
        
        for user_info in premium_users[:20]:  # Limit to 20 users
            text += f"• {user_info}\n"
        
        if len(premium_users) > 20:
            text += f"\n... and {len(premium_users) - 20} more users"
        
        if len(text) > 4096:
            with open('premium_users.txt', 'w') as f:
                f.write(text)
            await message.reply_document('premium_users.txt', caption="📋 Premium Users List")
            import os
            os.remove('premium_users.txt')
        else:
            await message.reply_text(text)
            
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

# User command to check premium plan
@Client.on_message(filters.command("myplan") & filters.private)
async def check_plan_cmd(client: Client, message: Message):
    try:
        user_id = message.from_user.id
        plan = await check_user_plan(user_id)
        
        if not plan:
            return await message.reply_text(
                "🆓 **Free User**\n\n"
                f"You are currently using the free plan.\n\n"
                f"**Current Limitations:**\n"
                f"• 🔒 Verification required every 24 hours\n"
                f"• 📁 Only {Config.MAX_CONCURRENT_NON_PREMIUM} file at a time\n"
                f"• ⏳ No queue management\n\n"
                f"**Upgrade to Premium for:**\n"
                f"• ✅ No verification needed\n"
                f"• 🚀 Up to {Config.MAX_CONCURRENT_PREMIUM} concurrent files\n"
                f"• ⚡ Priority processing\n"
                f"• 📊 Queue management\n\n"
                f"Contact admin for premium access!",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("💎 Get Premium", url=f"t.me/{Config.ADMIN}")]
                ])
            )
        
        if plan.get("active"):
            await message.reply_text(
                f"⭐ **Premium User**\n\n"
                f"✅ **Status:** Active\n"
                f"⏰ **Time Left:** {plan['time_left']}\n"
                f"📅 **Expires On:** {plan['expires_on']}\n\n"
                f"**Your Benefits:**\n"
                f"• ✅ No verification required\n"
                f"• 🚀 Up to {Config.MAX_CONCURRENT_PREMIUM} concurrent encodings\n"
                f"• ⚡ Priority processing\n"
                f"• 📊 Queue management with /queue\n\n"
                f"Enjoy your premium experience! 🎬"
            )
        else:
            await message.reply_text(
                f"❌ **Premium Expired**\n\n"
                f"Your premium plan expired on {plan.get('expired_on', 'Unknown')}\n\n"
                f"Contact admin to renew your premium access!",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("💎 Renew Premium", url=f"t.me/{Config.ADMIN}")]
                ])
            )
            
    except Exception as e:
        await message.reply_text(f"❌ Error checking plan: {str(e)}")

# Queue management command
@Client.on_message(filters.command("queue") & filters.private)
async def queue_cmd(client: Client, message: Message):
    try:
        user_id = message.from_user.id
        
        # Check if user has access to queue command
        is_premium = await is_premium_user(user_id)
        is_admin = user_id == Config.ADMIN
        
        if not is_premium and not is_admin:
            return await message.reply_text(
                "🔒 **Premium Feature**\n\n"
                "Queue management is only available for premium users.\n\n"
                "**Upgrade to Premium for:**\n"
                f"• 📊 Queue management\n"
                f"• 🚀 Up to {Config.MAX_CONCURRENT_PREMIUM} concurrent files\n"
                f"• ⚡ Priority processing\n"
                f"• ✅ No verification needed\n\n"
                "Contact admin for premium access!",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("💎 Get Premium", url=f"t.me/{Config.ADMIN}")]
                ])
            )
        
        queue_status = await get_queue_status(user_id)
        formatted_queue = format_queue_display(queue_status, is_premium, is_admin)
        
        buttons = []
        if queue_status['total_queued'] > 0:
            buttons.append([InlineKeyboardButton("🗑️ Clear Queue", callback_data=f"clear_queue_{user_id}")])
        
        buttons.append([InlineKeyboardButton("🔄 Refresh", callback_data=f"refresh_queue_{user_id}")])
        
        await message.reply_text(
            formatted_queue,
            reply_markup=InlineKeyboardMarkup(buttons) if buttons else None
        )
        
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

# Queue callback handlers
@Client.on_callback_query(filters.regex(r"clear_queue_(\d+)"))
async def clear_queue_callback(client: Client, callback_query):
    try:
        user_id = int(callback_query.matches[0].group(1))
        
        if callback_query.from_user.id != user_id and callback_query.from_user.id != Config.ADMIN:
            return await callback_query.answer("❌ You can only manage your own queue!", show_alert=True)
        
        await clear_user_queue(user_id)
        
        await callback_query.edit_message_text(
            "✅ **Queue Cleared**\n\n"
            "All files have been removed from your queue.\n"
            "Active processing will continue until completion."
        )
        
    except Exception as e:
        await callback_query.answer(f"Error: {str(e)}", show_alert=True)

@Client.on_callback_query(filters.regex(r"refresh_queue_(\d+)"))
async def refresh_queue_callback(client: Client, callback_query):
    try:
        user_id = int(callback_query.matches[0].group(1))
        
        if callback_query.from_user.id != user_id and callback_query.from_user.id != Config.ADMIN:
            return await callback_query.answer("❌ You can only view your own queue!", show_alert=True)
        
        is_premium = await is_premium_user(user_id)
        is_admin = user_id == Config.ADMIN
        
        queue_status = await get_queue_status(user_id)
        formatted_queue = format_queue_display(queue_status, is_premium, is_admin)
        
        buttons = []
        if queue_status['total_queued'] > 0:
            buttons.append([InlineKeyboardButton("🗑️ Clear Queue", callback_data=f"clear_queue_{user_id}")])
        
        buttons.append([InlineKeyboardButton("🔄 Refresh", callback_data=f"refresh_queue_{user_id}")])
        
        await callback_query.edit_message_text(
            formatted_queue,
            reply_markup=InlineKeyboardMarkup(buttons) if buttons else None
        )
        
    except Exception as e:
        await callback_query.answer(f"Error: {str(e)}", show_alert=True)

# Premium stats command for admin
@Client.on_message(filters.command("premiumstats") & filters.user(Config.ADMIN))
async def premium_stats_cmd(client: Client, message: Message):
    try:
        stats = await get_premium_stats()
        
        text = f"📊 **Premium Statistics**\n\n"
        text += f"👥 **Total Premium Users:** {stats['total']}\n"
        text += f"✅ **Active Users:** {stats['active']}\n"
        text += f"❌ **Expired Users:** {stats['expired']}\n\n"
        
        if stats['active'] > 0:
            percentage = (stats['active'] / stats['total']) * 100 if stats['total'] > 0 else 0
            text += f"📈 **Active Percentage:** {percentage:.1f}%\n"
        
        text += f"\n**Queue Configuration:**\n"
        text += f"🆓 **Free Users:** {Config.MAX_CONCURRENT_NON_PREMIUM} concurrent file\n"
        text += f"⭐ **Premium Users:** {Config.MAX_CONCURRENT_PREMIUM} concurrent files\n"
        text += f"👑 **Admins:** Unlimited\n"
        
        await message.reply_text(text)
        
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")
