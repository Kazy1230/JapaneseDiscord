from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Render / Railway などの環境変数からDB URLを取得
DATABASE_URL = os.environ.get("DATABASE_URL")

# DBエンジン作成
engine = create_engine(
    DATABASE_URL,
    echo=False,          # SQLログ出したければ True
    future=True
)

# セッション生成クラス
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

# モデルの基底クラス（これを全モデルで使う）
Base = declarative_base()
