import logging
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from Config import ADMINS
import os
from LuciferMoringstar_Robot.Utils import save_file
import pyromod.listen
logger = logging.getLogger(__name__)
lock = asyncio.Lock()


@Client.on_message(filters.command(['index', 'indexfiles']) & filters.user(ADMINS))
async def index_files(bot, message):
    """Save channel or group files"""
    if lock.locked():
        await message.reply('Wait until previous process complete.')
    else:
        while True:
            last_msg = await bot.ask(text = "Forward me last message of a channel which I should save to my database.\n\nYou can forward posts from any public channel, but for private channels bot should be an admin in the channel.\n\nMake sure to forward with quotes (Not as a copy)", chat_id = message.from_user.id)
            try:
                last_msg_id = last_msg.forward_from_message_id
                if last_msg.forward_from_chat.username:
                    chat_id = last_msg.forward_from_chat.username
                else:
                    chat_id=last_msg.forward_from_chat.id
                await bot.get_messages(chat_id, last_msg_id)
                break
            except Exception as e:
                await last_msg.reply_text(f"This Is An Invalid Message, Either the channel is private and bot is not an admin in the forwarded chat, or you forwarded message as copy.\nError caused Due to <code>{e}</code>")
                continue

        msg = await message.reply('Processing...⏳')
        total_files = 0
        async with lock:
            try:
                total=last_msg_id + 1
                current=int(os.environ.get("SKIP", 2))
                nyav=0
                while True:
                    try:
                        message = await bot.get_messages(chat_id=chat_id, message_ids=current, replies=0)
                    except FloodWait as e:
                        await asyncio.sleep(e.x)
                        message = await bot.get_messages(
                            chat_id,
                            current,
                            replies=0
                            )
                    except Exception as e:
                        print(e)
                        pass
                    try:
                        for file_type in ("document", "video", "audio"):
                            media = getattr(message, file_type, None)
                            if media is not None:
                                break
                            else:
                                continue
                        media.file_type = file_type
                        media.caption = message.caption
                        await save_file(media)
                        total_files += 1
                    except Exception as e:
                        print(e)
                        pass
                    current+=1
                    nyav+=1
                    if nyav == 20:
                        await msg.edit(f"Total messages fetched: {current}\nTotal messages saved: {total_files}")
                        nyav -= 20
                    if current == total:
                        break
                    else:
                        continue
            except Exception as e:
                logger.exception(e)
                await msg.edit(f'Error: {e}')
            else:
                await msg.edit(f'Total {total_files} Saved To DataBase!')

RATING = ["5.1 | IMDB", "6.2 | IMDB", "7.3 | IMDB", "8.4 | IMDB", "9.5 | IMDB", "10.6 | IMDB", ]
GENRES = ["fun, fact",
         "Thriller, Comedy",
         "Drama, Comedy",
         "Family, Drama",
         "Action, Adventure",
         "Film Noir",
         "Documentary"]
RELEASE_INFO = ["1901, 1902, 1903, 1904, 1905",
               "1906, 1907, 1908, 1909, 1910",
               "1911, 1912, 1913, 1914, 1915",
               "1916, 1917, 1918, 1919, 1920",
               "1921, 1922, 1923, 1924, 1925",
               "1926, 1927, 1928, 1929, 1930",
               "1931, 1932, 1933, 1934, 1935",
               "1936, 1937, 1938, 1939, 1940",
               "1941, 1942, 1943, 1944, 1945",
               "1946, 1947, 1948, 1949, 1950",
               "1951, 1952, 1953, 1954, 1955",
               "1956, 1957, 1958, 1959, 1960",
               "1961, 1962, 1963, 1964, 1965",
               "1966, 1967, 1968, 1969, 1970",
               "1971, 1972, 1973, 1974, 1975",
               "1976, 1977, 1978, 1979, 1980",
               "1981, 1982, 1983, 1984, 1985",
               "1986, 1987, 1988, 1989, 1990",
               "1991, 1992, 1993, 1994, 1995",
               "1996, 1997, 1998, 1999, 2000",
               "2001, 2002, 2003, 2004, 2005",
               "2006, 2007, 2008, 2009, 2010",
               "2011, 2012, 2013, 2014, 2015",
               "2016, 2017, 2018, 2019, 2020",
               "2021, 2022, 2023, 2024, 2025",
               "2026, 2027, 2028, 2029, 2030"]
