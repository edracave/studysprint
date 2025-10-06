
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, Boolean, Date, DateTime, JSON, func
from app.config import DB_URL

engine = create_async_engine(DB_URL, echo=False, future=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_user_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    locale: Mapped[str] = mapped_column(String, default="es-ES")
    timezone: Mapped[str] = mapped_column(String, default="Europe/Madrid")
    premium: Mapped[bool] = mapped_column(Boolean, default=False)
    msg_quota_today: Mapped[int] = mapped_column(Integer, default=20)
    last_reset_quota: Mapped[Date] = mapped_column(Date, default=func.date(func.now()))
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

class Plan(Base):
    __tablename__ = "plans"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, index=True)
    exam_name: Mapped[str] = mapped_column(String)
    deadline_date: Mapped[str] = mapped_column(String)
    daily_hours: Mapped[float] = mapped_column()
    topics_total: Mapped[int] = mapped_column(Integer)
    difficulty_self: Mapped[str] = mapped_column(String)
    topics_labels: Mapped[dict | None] = mapped_column(JSON, default=None)
    topics_plan: Mapped[dict | None] = mapped_column(JSON, default=None)
    generated_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

class Event(Base):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, index=True)
    type: Mapped[str] = mapped_column(String)
    payload: Mapped[dict | None] = mapped_column(JSON, default=None)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
