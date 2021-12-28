# owner @bazigarYT
start  20/dec/2021
end    28/dec/2021

import os
import logging
from pytube import YouTube
from youtube_search import YoutubeSearch
from pytgcalls import PyTgCalls, idle
from pytgcalls.types import AudioPiped, AudioVideoPiped, GroupCall
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery


@bot.on_message(filters.command("play") & filters.group)
async def music_play(_, message):
    await message.delete()
    user_id = message.from_user.id
    if user_id != OWNER_ID:
        return
    try:
        query = message.text.split(None, 1)[1]
    except:
        return await message.reply_text("<b>Usage:</b> <code>/play [query]</code>")
    chat_id = message.chat.id
    m = await message.reply_text("🔄 Processing...")
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        thumb = results[0]["thumbnails"][0]
        duration = results[0]["duration"]
        yt = YouTube(link)
        cap = f"🎵 <b>Playing:</b> [{yt.title}]({link}) \n\n⏳ <b>Duration:</b> {duration} \n⚙TAP BUTTON FOR SETUP "
        aud = yt.streams.get_by_itag(140).download()
    except Exception as e:
        if "Too Many Requests" in str(e):
            await m.edit("❗️<i>Please wait at least 30 seconds to use me.</i>")
            os.system(f"kill -9 {os.getpid()} && python3 app.py")
        else:
            return await m.edit(str(e))
    
    try:
        if str(chat_id) in CHATS:
            await app.change_stream(
                chat_id,
                AudioPiped(aud)
            )
            await message.reply_photo(thumb, caption=cap, reply_markup=BUTTONS)
            await m.delete()
            os.remove(aud)
        else:            
            await app.join_group_call(
                chat_id,
                AudioPiped(aud)
            )
            CHATS.append(str(chat_id))
            await message.reply_photo(thumb, caption=cap, reply_markup=BUTTONS)
            await m.delete()
            os.remove(aud)
    except Exception as e:
        return await m.edit(str(e))
