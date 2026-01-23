import os
import re
import discord
from discord.ext import commands
from dotenv import load_dotenv

from database import engine, SessionLocal
from models import Base, User, StudyLog

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

def extract_number(text: str):
    match = re.search(r'\d+', text)
    if match:
        return int(match.group())
    return None

bot = commands.Bot(command_prefix="!", intents=intents)

# DB初期化
Base.metadata.create_all(bind=engine)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    value = extract_number(message.content)
    if value is None:
        return

    session = SessionLocal()
    discord_id = str(message.author.id)

    user = session.query(User).filter_by(discord_id=discord_id).first()
    if not user:
        user = User(discord_id=discord_id, username=str(message.author))
        session.add(user)
        session.commit()

    stat = session.query(UserStat).filter_by(user_id=user.id).first()
    if not stat:
        stat = UserStat(user_id=user.id, total_value=0)
        session.add(stat)

    stat.total_value += value
    session.commit()
    session.close()

    # 🔽 ここがポイント
    await message.add_reaction("✅")

    await bot.process_commands(message)


bot.run(TOKEN)
