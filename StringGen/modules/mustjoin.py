from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden
from StringGen import Anony
import logging

# Configure logging
logger = logging.getLogger(__name__)

MUST_JOIN = "SFW_Community_Official"  # Can be username or chat ID

@Anony.on_message(filters.incoming & filters.private, group=-1)
async def must_join_channel(app: Client, msg: Message):
    if not MUST_JOIN:
        return
    
    try:
        # Check if user is in the channel
        try:
            await app.get_chat_member(MUST_JOIN, msg.from_user.id)
            return  # User is member, allow to proceed
        except UserNotParticipant:
            pass  # Will handle below
        except Exception as e:
            logger.error(f"Error checking chat member: {e}")
            return
            
        # Generate proper invite link
        try:
            if MUST_JOIN.startswith("@"):
                link = f"https://t.me/{MUST_JOIN[1:]}"
            elif MUST_JOIN.startswith("-100"):
                chat = await app.get_chat(MUST_JOIN)
                link = chat.invite_link or f"https://t.me/+{chat.invite_link.split('/')[-1]}"
            else:
                link = f"https://t.me/{MUST_JOIN}"
        except Exception as e:
            logger.error(f"Error generating invite link: {e}")
            return

        # Send join message
        try:
            await msg.reply_photo(
                photo="https://files.catbox.moe/t8tz2a.jpg", 
                caption=(
                    "๏ ᴀᴄᴄᴏʀᴅɪɴɢ ᴛᴏ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ ʏᴏᴜ'ᴠᴇ ɴᴏᴛ ᴊᴏɪɴᴇᴅ [๏sᴜᴘᴘᴏʀᴛ๏]({link}) ʏᴇᴛ.\n\n"
                    "ɪғ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴜsᴇ ᴍᴇ ᴛʜᴇɴ ᴊᴏɪɴ [๏sᴜᴘᴘᴏʀᴛ๏]({link}) "
                    "**ᴀɴᴅ sᴛᴀʀᴛ ᴍᴇ ᴀɢᴀɪɴ /start !**"
                ),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "๏Jᴏɪɴ๏", 
                                url=link
                            )
                        ]
                    ]
                ),
                disable_web_page_preview=True
            )
            await msg.stop_propagation()
            
        except ChatWriteForbidden:
            logger.warning(f"Can't write to chat with {msg.from_user.id}")
        except Exception as e:
            logger.error(f"Error sending join message: {e}")

    except ChatAdminRequired:
        logger.error(f"Promote me as admin in {MUST_JOIN} to check members!")
    except Exception as e:
        logger.error(f"Unexpected error in must_join_channel: {e}", exc_info=True)
