from pyrogram import filters
from pyrogram.types import CallbackQuery
from StringGen import Anony
from StringGen.modules.gen import gen_session
from StringGen.utils import gen_key  # Make sure this contains the buttons for session generation

@Anony.on_callback_query(filters.regex(pattern=r"^(gensession|pyrogram|pyrogram1|telethon)$"))
async def cb_choose(_, cq: CallbackQuery):
    await cq.answer()
    query = cq.data  # Directly access callback data

    # If user clicked on "gensession", show the next set of options for Pyrogram or Telethon
    if query == "gensession":
        return await cq.message.reply_text(
            text="<b>» ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ ғᴏʀ ɢᴇɴᴇʀᴀᴛɪɴɢ ʏᴏᴜʀ sᴇssɪᴏɴ :</b>",
            reply_markup=gen_key,  # This should contain buttons like pyrogram, telethon, etc.
        )
    
    # When a user selects either pyrogram or telethon, generate the session
    elif query.startswith("pyrogram") or query.startswith("telethon"):
        try:
            if query == "pyrogram":
                await gen_session(cq.message, cq.from_user.id)  # Default Pyrogram v2
            elif query == "pyrogram1":
                await gen_session(cq.message, cq.from_user.id, old_pyro=True)  # Old Pyrogram v1
            elif query == "telethon":
                await gen_session(cq.message, cq.from_user.id, telethon=True)  # Telethon
            
            # Send a success message or indicate something else is in progress if needed
        except Exception as e:
            await cq.edit_message_text(
                f"» Session generate karte waqt error aaya: {str(e)}",
                disable_web_page_preview=True
            )
