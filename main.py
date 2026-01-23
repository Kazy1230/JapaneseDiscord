import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

from database import engine, SessionLocal
from models import Base, User, StudyLog

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# DB初期化
Base.metadata.create_all(bind=engine)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def log(ctx, category: str, *, content: str):
    """
    使い方:
    !log grammar I have went to school
    """
    session = SessionLocal()

    discord_id = str(ctx.author.id)

    user = session.query(User).filter_by(discord_id=discord_id).first()
    if not user:
        user = User(
            discord_id=discord_id,
            username=str(ctx.author)
        )
        session.add(user)
        session.commit()

    log = StudyLog(
        user_id=user.id,
        category=category,
        content=content,
        is_correct=False  # ←後でAIや手動で更新
    )

    session.add(log)
    session.commit()
    session.close()

    await ctx.send("✅ 学習ログを記録したよ！")

bot.run(TOKEN)
