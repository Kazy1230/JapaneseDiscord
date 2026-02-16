import re
import discord
from discord.ext import commands

from database import SessionLocal
from models import UserStat
from database import engine
from models import Base
from sqlalchemy import desc



# -------- Discord Bot 設定 --------
intents = discord.Intents.default()
intents.message_content = True  # ← これ必須

bot = commands.Bot(command_prefix="!", intents=intents)


# -------- 数字抽出関数 --------
def extract_number(text: str) -> int | None:
    """
    メッセージから最初の整数を取り出す
    例: "今日は30分勉強した" -> 30
    """
    match = re.search(r"\d+", text)
    if match:
        return int(match.group())
    return None


# -------- Bot 起動確認 --------
@bot.event
async def on_ready():
    Base.metadata.create_all(bind=engine)
    print(f"Logged in as {bot.user}")


# -------- メッセージ監視 --------
@bot.event
async def on_message(message: discord.Message):
    # Bot自身の発言は無視
    if message.author.bot:
        return

    value = extract_number(message.content)

    # 数字がなければ何もしない
    if value is None:
        return

    session = SessionLocal()

    discord_id = str(message.author.id)

    # ユーザー取得 or 作成
    stat = session.query(UserStat).filter_by(discord_id=discord_id).first()
    if not stat:
        stat = UserStat(
            discord_id=discord_id,
            total_minutes=0
        )
        session.add(stat)
        session.commit()

    # 累積
    stat.total_minutes += value
    session.commit()
    session.close()

    # ✅ メッセージは返さず、リアクションだけ
    await message.add_reaction("✅")
    await bot.process_commands(message)


@bot.command()
async def ranking(ctx):
    print("test")
    db = SessionLocal()
    try:
        users = (
            db.query(UserStat)
            .order_by(desc(UserStat.total_minutes))
            .limit(10)
            .all()
        )
        if not users:
            await ctx.send("まだ学習記録がありません。")
            return

        message ="🏆 学習時間ランキング 🏆\n\n"

        for i, user in enumerate(users, start=1):
            message += f"{i}. {user.username} - {user.total_minutes} 分\n"

        await ctx.send(message)
    finally:
        db.close()

# -------- Bot 起動 --------
import os
bot.run(os.environ["DISCORD_TOKEN"])
